import os 
import random 
import time 
from dataclasses import dataclass 
from typing import Dict, List, Optional, Sequence, Tuple 
 
import cv2 
import numpy as np 
import torch 
import torch.nn as nn 
from torch.utils.data import DataLoader, Dataset 
from torchvision import models 
 
 
@dataclass(frozen=True) 
class Config: 
    TRAIN_DIR: str = "./blur_score_assessment/DIV2K_train_HR" 
    TEST_DIR: str = "./blur_score_assessment/DIV2K_test_HR" 
    MODEL_SAVE_PATH: str = "./blur_score_assessment/best_blur_model_efficientnet.pth" 
 
    CROP_SIZE: int = 256 
    INPUT_SIZE: int = 224 
    BATCH_SIZE: int = 32 
    EPOCHS: int = 10
    LEARNING_RATE: float = 1e-4 
    WEIGHT_DECAY: float = 1e-4 
    DROPOUT: float = 0.3 
    TRAIN_VAL_SPLIT: float = 0.9 
    SAMPLES_PER_IMAGE_TRAIN: int = 4 
    SAMPLES_PER_IMAGE_EVAL: int = 1 
    NUM_WORKERS: int = 2 
    SMART_CROP_CANDIDATES: int = 4 
    RANDOM_CROP_PROB: float = 0.40 
    JPEG_PROB_TRAIN: float = 0.70 
    PRINT_EVERY_N_BATCHES: int = 10 
    SEED: int = 42 
 
    # Label curve. sigma=20 -> 0.982, so the model finally sees near-1 targets. 
    LABEL_TAU: float = 5.0 
 
    # Balanced severity sampling. The severe bucket is intentionally explicit. 
    # Format: (bucket_name, sigma_min, sigma_max, probability) 
    SEVERITY_BUCKETS: Tuple[Tuple[str, float, float, float], ...] = ( 
        ("clear", 0.0, 0.0, 0.12), 
        ("very_light", 0.25, 1.25, 0.18), 
        ("light", 1.25, 2.75, 0.20), 
        ("medium", 2.75, 5.50, 0.22), 
        ("heavy", 5.50, 10.00, 0.14), 
        ("extreme", 10.00, 20.00, 0.14), 
    ) 
 
    # Deterministic validation/test sigmas, including the previously missing top end. 
    EVAL_SIGMAS: Tuple[float, ...] = ( 
        0.0, 0.5, 1.0, 1.75, 2.5, 3.5, 5.0, 7.5, 10.0, 14.0, 20.0 
    ) 
 
    DEVICE: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
 
 
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32) 
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32) 
CFG = Config() 
 
 
def seed_everything(seed: int) -> None: 
    random.seed(seed) 
    np.random.seed(seed) 
    torch.manual_seed(seed) 
    torch.cuda.manual_seed_all(seed) 
    torch.backends.cudnn.benchmark = True 
 
 
def log_step(message: str) -> None: 
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True) 
 
 
def sigma_to_target(sigma: float) -> float: 
    return float(1.0 - np.exp(-sigma / CFG.LABEL_TAU)) 
 
 
def target_to_percent(target: np.ndarray) -> np.ndarray: 
    return np.clip(target, 0.0, 1.0) * 100.0 
 
 
def list_images(root_dir: str) -> List[str]: 
    if not os.path.exists(root_dir): 
        raise FileNotFoundError(f"Image folder not found: {root_dir}") 
 
    files = [ 
        f for f in os.listdir(root_dir) 
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")) 
    ] 
    files.sort() 
    if not files: 
        raise RuntimeError(f"No valid images found in: {root_dir}") 
    return files 
 
 
def split_filenames(files: Sequence[str], train_ratio: float, seed: int) -> Tuple[List[str], List[str]]: 
    files = list(files) 
    rng = random.Random(seed) 
    rng.shuffle(files) 
    train_size = max(1, int(len(files) * train_ratio)) 
    train_files = sorted(files[:train_size]) 
    val_files = sorted(files[train_size:]) 
    if not val_files: 
        val_files = train_files[-1:] 
        train_files = train_files[:-1] or val_files 
    return train_files, val_files 
 
 
def sample_training_sigma() -> Tuple[str, float]: 
    names = [bucket[0] for bucket in CFG.SEVERITY_BUCKETS] 
    probs = [bucket[3] for bucket in CFG.SEVERITY_BUCKETS] 
    selected = random.choices(CFG.SEVERITY_BUCKETS, weights=probs, k=1)[0] 
    name, lo, hi, _ = selected 
    if lo == hi: 
        return name, lo 
    return name, random.uniform(lo, hi)

def add_sensor_noise_rgb(image_rgb: np.ndarray, noise_level: float) -> np.ndarray: 
    image = image_rgb.astype(np.float32) / 255.0 
    shot_noise = np.random.normal(0.0, noise_level, image.shape).astype(np.float32) * np.sqrt(np.maximum(image, 0.02)) 
    read_noise = np.random.normal(0.0, noise_level * 0.35, image.shape).astype(np.float32) 
    noisy = np.clip(image + shot_noise + read_noise, 0.0, 1.0) 
    return (noisy * 255.0).astype(np.uint8) 
 
 
def simulate_mobile_jpeg_rgb(image_rgb: np.ndarray, quality_range: Tuple[int, int]) -> np.ndarray: 
    quality = random.randint(quality_range[0], quality_range[1]) 
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR) 
    ok, encoded = cv2.imencode(".jpg", image_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), quality]) 
    if not ok: 
        return image_rgb 
    decoded_bgr = cv2.imdecode(encoded, cv2.IMREAD_COLOR) 
    return cv2.cvtColor(decoded_bgr, cv2.COLOR_BGR2RGB) 
 
 
def gaussian_blur_rgb(image_rgb: np.ndarray, sigma: float) -> np.ndarray: 
    if sigma <= 0: 
        return image_rgb 
    kernel_size = int(2 * round(3 * sigma) + 1) 
    kernel_size = max(3, kernel_size | 1) 
    return cv2.GaussianBlur(image_rgb, (kernel_size, kernel_size), sigmaX=sigma, sigmaY=sigma) 
 
 
def motion_blur_rgb(image_rgb: np.ndarray, sigma: float) -> np.ndarray: 
    if sigma <= 0: 
        return image_rgb 
    # Calibrated so the motion kernel has the SAME effective standard 
    # deviation as a Gaussian kernel with this sigma. A uniform line kernel 
    # of length L has std = L / sqrt(12), so L = sigma * sqrt(12). 
    # This keeps the sigma->label mapping consistent regardless of which 
    # blur type gets sampled (previously motion/defocus were much weaker 
    # than Gaussian at the same nominal sigma, which corrupted the labels). 
    length = int(np.clip(round(sigma * np.sqrt(12.0)), 3, 69)) 
    length = length | 1 
    kernel = np.zeros((length, length), dtype=np.float32) 
    kernel[length // 2, :] = 1.0 
 
    angle = random.uniform(0.0, 180.0) 
    matrix = cv2.getRotationMatrix2D((length / 2.0 - 0.5, length / 2.0 - 0.5), angle, 1.0) 
    kernel = cv2.warpAffine(kernel, matrix, (length, length)) 
    kernel_sum = kernel.sum() 
    if kernel_sum <= 0: 
        return gaussian_blur_rgb(image_rgb, sigma) 
    kernel /= kernel_sum 
    return cv2.filter2D(image_rgb, -1, kernel) 
 
 
def defocus_blur_rgb(image_rgb: np.ndarray, sigma: float) -> np.ndarray: 
    if sigma <= 0: 
        return image_rgb 
    # Calibrated so the disc kernel has the SAME effective standard 
    # deviation as a Gaussian kernel with this sigma. A uniform disc of 
    # radius R has std = R / 2, so R = 2 * sigma. See motion_blur_rgb for 
    # why this matters for label consistency. 
    radius = int(np.clip(round(2.0 * sigma), 1, 40)) 
    size = radius * 2 + 1 
    y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1] 
    mask = (x * x + y * y) <= radius * radius 
    kernel = np.zeros((size, size), dtype=np.float32) 
    kernel[mask] = 1.0 
    kernel /= kernel.sum() 
    return cv2.filter2D(image_rgb, -1, kernel) 
 
 
def apply_synthetic_blur( 
    image_rgb: np.ndarray, sigma: float, training: bool, blur_type_override: Optional[str] = None 
) -> Tuple[np.ndarray, str]: 
    if sigma <= 0: 
        return image_rgb, "none" 
 
    if blur_type_override is not None: 
        blur_type = blur_type_override 
    elif not training: 
        # Deterministic fallback (only used if no override is supplied). 
        blur_type = "gaussian" 
    else: 
        # Real phone photos are blurred by motion or defocus at least as 
        # often as by a symmetric Gaussian-like blur, even at light/medium 
        # severity (hand shake, autofocus misses). Skewing gaussian this 
        # heavily at low sigma (previous 0.82/0.10/0.08) meant the model
        # mostly learned the Gaussian PSF signature and could misjudge real 
        # motion/defocus blur at everyday severities, not just extreme ones. 
        if sigma >= 5.5: 
            blur_type = random.choices( 
                ["gaussian", "motion", "defocus"], 
                weights=[0.45, 0.30, 0.25], 
                k=1, 
            )[0] 
        else: 
            blur_type = random.choices( 
                ["gaussian", "motion", "defocus"], 
                weights=[0.55, 0.24, 0.21], 
                k=1, 
            )[0] 
 
    if blur_type == "motion": 
        return motion_blur_rgb(image_rgb, sigma), blur_type 
    if blur_type == "defocus": 
        return defocus_blur_rgb(image_rgb, sigma), blur_type 
    return gaussian_blur_rgb(image_rgb, sigma), blur_type 
 
 
def normalize_patch(image_rgb: np.ndarray, input_size: int) -> torch.Tensor: 
    patch = cv2.resize(image_rgb, (input_size, input_size), interpolation=cv2.INTER_AREA) 
    patch = patch.astype(np.float32) / 255.0 
    patch = (patch - IMAGENET_MEAN) / IMAGENET_STD 
    patch = np.transpose(patch, (2, 0, 1)) 
    return torch.tensor(patch, dtype=torch.float32) 
 
 
class SmartBlurDataset(Dataset): 
    def __init__( 
        self, 
        root_dir: str, 
        image_files: Optional[Sequence[str]] = None, 
        samples_per_image: int = 1, 
        training: bool = True, 
        crop_size: int = CFG.CROP_SIZE, 
        input_size: int = CFG.INPUT_SIZE, 
    ): 
        self.root_dir = root_dir 
        self.image_files = list(image_files) if image_files is not None else list_images(root_dir) 
        self.samples_per_image = max(1, samples_per_image) 
        self.training = training 
        self.crop_size = crop_size 
        self.input_size = input_size 
 
    def __len__(self) -> int: 
        if self.training: 
            return len(self.image_files) * self.samples_per_image 
        return len(self.image_files) * len(CFG.EVAL_SIGMAS) * self.samples_per_image 
 
    def _load_rgb(self, file_index: int) -> np.ndarray: 
        img_path = os.path.join(self.root_dir, self.image_files[file_index]) 
        img_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR) 
        if img_bgr is None: 
            raise FileNotFoundError(f"Could not read image: {img_path}") 
        return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) 
 
    def _pad_if_needed(self, img: np.ndarray) -> np.ndarray: 
        h, w = img.shape[:2] 
        if h >= self.crop_size and w >= self.crop_size: 
            return img 
        new_w = max(w, self.crop_size) 
        new_h = max(h, self.crop_size) 
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC) 
 
    def _laplacian_var(self, patch_rgb: np.ndarray) -> float: 
        gray = cv2.cvtColor(patch_rgb, cv2.COLOR_RGB2GRAY) 
        return float(cv2.Laplacian(gray, cv2.CV_64F).var()) 
 
    def _candidate_patch(self, img: np.ndarray, top: int, left: int) -> np.ndarray: 
        return img[top:top + self.crop_size, left:left + self.crop_size] 
 
    def _get_patch(self, img: np.ndarray) -> np.ndarray: 
        img = self._pad_if_needed(img) 
        h, w = img.shape[:2] 
 
        if not self.training: 
            # Fixed (deterministic, reproducible across runs) candidate 
            # positions instead of a single blind center crop. DIV2K photos 
            # are professional shots and often have shallow depth of field 
            # (natural background bokeh) even in an otherwise "sharp" image. 
            # A blind center crop can land on a naturally soft region while 
            # the label still says sigma=0 (perfectly sharp), which corrupts 
            # the eval/test labels at the low end. We deterministically pick 
            # the sharpest of 5 fixed positions instead, matching what the 
            # (sharpness-aware) training crops actually look like. 
            max_top = h - self.crop_size 
            max_left = w - self.crop_size 
            candidates = [ 
                (max_top // 2, max_left // 2),          # center 
                (0, 0),                                  # top-left 
                (0, max_left),                            # top-right 
                (max_top, 0),                              # bottom-left 
                (max_top, max_left),                        # bottom-right 
            ] 
            best_patch, best_score = None, -1.0 
            for top, left in candidates: 
                patch = self._candidate_patch(img, top, left) 
                score = self._laplacian_var(patch) 
                if score > best_score: 
                    best_score = score 
                    best_patch = patch 
            return best_patch 
 
        if random.random() < CFG.RANDOM_CROP_PROB: 
            top = random.randint(0, h - self.crop_size) 
            left = random.randint(0, w - self.crop_size) 
            return self._candidate_patch(img, top, left) 
 
        best_patch = None 
        best_score = -1.0 
        for _ in range(CFG.SMART_CROP_CANDIDATES): 
            top = random.randint(0, h - self.crop_size) 
            left = random.randint(0, w - self.crop_size) 
            patch = self._candidate_patch(img, top, left) 
            score = self._laplacian_var(patch) 
            if score > best_score: 
                best_score = score 
                best_patch = patch 
        return best_patch 
 
    def _sigma_for_index(self, idx: int) -> Tuple[str, float]: 
        if self.training: 
            return sample_training_sigma() 
        sigma_index = (idx // len(self.image_files)) % len(CFG.EVAL_SIGMAS) 
        sigma = CFG.EVAL_SIGMAS[sigma_index] 
        return f"eval_sigma_{sigma:g}", sigma 
 
    def _eval_blur_type(self, file_index: int, idx: int) -> str: 
        # Deterministic (reproducible) round-robin across blur types so 
        # validation/test measure generalization to motion and defocus 
        # blur too, not only Gaussian. Previously ALL eval/val examples 
        # used Gaussian blur only, so best-model selection (best_val_mae) 
        # never actually rewarded good motion/defocus performance even 
        # though the model was trained on all three types. 
        sigma_index = (idx // len(self.image_files)) % len(CFG.EVAL_SIGMAS) 
        return ["gaussian", "motion", "defocus"][(file_index + sigma_index) % 3] 
 
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]: 
        file_index = idx % len(self.image_files) 
        img = self._load_rgb(file_index) 
        patch = self._get_patch(img) 
 
        _, sigma = self._sigma_for_index(idx) 
        label = sigma_to_target(sigma) 
 
        blur_type_override = None if self.training else self._eval_blur_type(file_index, idx) 
        patch, _ = apply_synthetic_blur( 
            patch, sigma, training=self.training, blur_type_override=blur_type_override 
        ) 
 
        if self.training: 
            if random.random() < 0.5: 
                patch = cv2.flip(patch, 1) 
            if random.random() < 0.25: 
                patch = cv2.flip(patch, 0) 
            if random.random() < 0.35: 
                gain = random.uniform(0.9, 1.1) 
                bias = random.uniform(-6.0, 6.0) 
                patch = np.clip(patch.astype(np.float32) * gain + bias, 0, 255).astype(np.uint8) 
 
        noise_level = random.uniform(0.004, 0.018) if self.training else 0.010 
        jpeg_range = (70, 95) if self.training else (82, 88) 
        patch = add_sensor_noise_rgb(patch, noise_level=noise_level) 
        if (not self.training) or random.random() < CFG.JPEG_PROB_TRAIN:  
            patch = simulate_mobile_jpeg_rgb(patch, quality_range=jpeg_range) 
 
        tensor = normalize_patch(patch, self.input_size) 
        return tensor, torch.tensor(label, dtype=torch.float32) 
 
 
def build_model(pretrained: bool = True) -> nn.Module: 
    weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None 
    model = models.efficientnet_b0(weights=weights) 
 
    for param in model.parameters(): 
        param.requires_grad = False 
    for param in model.features[-3:].parameters(): 
        param.requires_grad = True 
 
    in_features = model.classifier[1].in_features 
    model.classifier = nn.Sequential( 
        nn.Linear(in_features, 256), 
        nn.ReLU(inplace=True), 
        nn.Dropout(CFG.DROPOUT), 
        nn.Linear(256, 1), 
    ) 
    return model 
 
 
class HighBlurAwareLoss(nn.Module): 
    def __init__(self): 
        super().__init__() 
        self.bce = nn.BCEWithLogitsLoss(reduction="none") 
 
    def forward(self, logits: torch.Tensor, target: torch.Tensor) -> torch.Tensor: 
        pred = torch.sigmoid(logits) 
 
        # The old mid-focused weight becomes small near target=1. This extra 
        # term makes severe examples expensive to underpredict. 
        mid_weight = 1.0 + 1.5 * (target * (1.0 - target)) 
        high_weight = 1.0 + 3.0 * torch.clamp((target - 0.70) / 0.30, min=0.0, max=1.0) 
        weights = mid_weight * high_weight 
 
        bce_loss = self.bce(logits, target) 
        l1_loss = nn.functional.smooth_l1_loss(pred, target, beta=0.035, reduction="none") 
        loss = 0.65 * bce_loss + 0.35 * l1_loss 
        return (weights * loss).mean() 
 
 
def prediction_from_logits(logits: torch.Tensor) -> torch.Tensor: 
    return torch.sigmoid(logits) 
 
 
def bin_name(value: float) -> str: 
    if value < 0.20: 
        return "00-20" 
    if value < 0.45: 
        return "20-45" 
    if value < 0.70: 
        return "45-70" 
    if value < 0.90: 
        return "70-90" 
    return "90-100" 
 
 
def evaluate_model(model: nn.Module, loader: DataLoader, name: str, print_samples: bool = False) -> Tuple[float, float]: 
    model.eval() 
    all_preds: List[float] = [] 
    all_labels: List[float] = [] 
    start_time = time.time() 
    log_step(f"Starting {name} evaluation on {len(loader.dataset)} samples...") 
 
    with torch.no_grad(): 
        for batch_idx, (images, labels) in enumerate(loader, start=1): 
            images = images.to(CFG.DEVICE, non_blocking=True) 
            logits = model(images).squeeze(1) 
            preds = prediction_from_logits(logits).cpu().numpy() 
            all_preds.extend(preds.tolist()) 
            all_labels.extend(labels.numpy().tolist()) 
            if batch_idx == 1 or batch_idx % CFG.PRINT_EVERY_N_BATCHES == 0 or batch_idx == len(loader): 
                log_step(f"{name} batch {batch_idx}/{len(loader)} done") 
 
    preds_np = np.clip(np.array(all_preds, dtype=np.float32), 0.0, 1.0) 
    labels_np = np.array(all_labels, dtype=np.float32) 
    mae = float(np.mean(np.abs(preds_np - labels_np))) 
    rmse = float(np.sqrt(np.mean((preds_np - labels_np) ** 2))) 
 
    elapsed = time.time() - start_time 
    print(f"{name}: MAE={mae:.4f} ({mae * 100:.2f}%) | RMSE={rmse:.4f} ({rmse * 100:.2f}%) | time={elapsed:.1f}s") 
 
    bins: Dict[str, List[float]] = {"00-20": [], "20-45": [], "45-70": [], "70-90": [], "90-100": []} 
    for pred, label in zip(preds_np, labels_np): 
        bins[bin_name(float(label))].append(abs(float(pred) - float(label))) 
    bin_report = [] 
    for key, values in bins.items(): 
        if values: 
            bin_report.append(f"{key}: {np.mean(values) * 100:.2f}% n={len(values)}") 
    print("  MAE by target bin -> " + " | ".join(bin_report)) 
 
    if print_samples: 
        # Sample 10 indices spread across the ENTIRE evaluated set with a 
        # fixed seed (reproducible, not cherry-picked). Just taking the 
        # first N would be biased: the dataset is grouped by sigma 
        # (sigma_index = idx // len(image_files)), so the first N samples 
        # would always be the sigma=0 / clear-only block. 
        rng = np.random.default_rng(CFG.SEED) 
        n_show = min(10, len(preds_np)) 
        sample_idx = rng.choice(len(preds_np), size=n_show, replace=False) 
        sample_idx.sort() 
        print(f"  Random sample of {n_show} test predictions vs true labels:") 
        for i in sample_idx: 
            pred_pct = float(np.clip(preds_np[i], 0.0, 1.0)) * 100.0 
            label_pct = float(labels_np[i]) * 100.0 
            print(f"    idx={i:5d} | true_label={label_pct:6.2f}% | predicted={pred_pct:6.2f}% | abs_error={abs(pred_pct - label_pct):5.2f}%") 
 
    return mae, rmse 
 
 
def train_model() -> None: 
    seed_everything(CFG.SEED) 
    log_step("Starting high-blur calibrated training script...") 
    log_step(f"Device: {CFG.DEVICE}") 
    log_step( 
        "Settings: " 
        f"epochs={CFG.EPOCHS}, batch_size={CFG.BATCH_SIZE}, " 
        f"samples_per_image_train={CFG.SAMPLES_PER_IMAGE_TRAIN}, " 
        f"max_eval_sigma={max(CFG.EVAL_SIGMAS)}, workers={CFG.NUM_WORKERS}" 
    ) 
 
    log_step(f"Scanning training folder: {CFG.TRAIN_DIR}") 
    all_train_files = list_images(CFG.TRAIN_DIR) 
    train_files, val_files = split_filenames(all_train_files, CFG.TRAIN_VAL_SPLIT, CFG.SEED) 
    log_step(f"Train images: {len(train_files)} | Validation images: {len(val_files)}") 
 
    log_step("Building datasets...") 
    train_dataset = SmartBlurDataset( 
        CFG.TRAIN_DIR, 
        image_files=train_files, 
        samples_per_image=CFG.SAMPLES_PER_IMAGE_TRAIN, 
        training=True, 
    ) 
    val_dataset = SmartBlurDataset( 
        CFG.TRAIN_DIR, 
        image_files=val_files, 
        samples_per_image=CFG.SAMPLES_PER_IMAGE_EVAL, 
        training=False, 
    ) 
    log_step(f"Train samples per epoch: {len(train_dataset)}") 
    log_step(f"Validation samples: {len(val_dataset)}") 
    log_step("Severity buckets: " + ", ".join( 
        f"{name}[{lo:g},{hi:g}] p={prob:.2f}" for name, lo, hi, prob in CFG.SEVERITY_BUCKETS 
    )) 
    log_step("Eval sigmas: " + ", ".join(f"{s:g}->{sigma_to_target(s) * 100:.1f}%" for s in CFG.EVAL_SIGMAS)) 
 
    generator = torch.Generator().manual_seed(CFG.SEED) 
    loader_kwargs = { 
        "num_workers": CFG.NUM_WORKERS, 
        "pin_memory": torch.cuda.is_available(), 
        "persistent_workers": CFG.NUM_WORKERS > 0, 
    } 
    log_step("Building data loaders...") 
    train_loader = DataLoader( 
        train_dataset, 
        batch_size=CFG.BATCH_SIZE, 
        shuffle=True, 
        drop_last=True, 
        generator=generator, 
        **loader_kwargs, 
    ) 
    val_loader = DataLoader( 
        val_dataset, 
        batch_size=CFG.BATCH_SIZE, 
        shuffle=False, 
        **loader_kwargs, 
    ) 
 
    log_step("Building EfficientNet-B0 model...") 
    model = build_model(pretrained=True).to(CFG.DEVICE) 
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad) 
    total_params = sum(p.numel() for p in model.parameters()) 
    log_step(f"Trainable parameters: {trainable_params:,} / {total_params:,}") 
 
    criterion = HighBlurAwareLoss() 
    optimizer = torch.optim.AdamW( 
        filter(lambda p: p.requires_grad, model.parameters()), 
        lr=CFG.LEARNING_RATE, 
        weight_decay=CFG.WEIGHT_DECAY, 
    ) 
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=CFG.EPOCHS) 
 
    best_val_mae = float("inf") 
    for epoch in range(CFG.EPOCHS): 
        epoch_start = time.time() 
        model.train() 
        running_loss = 0.0 
        log_step(f"Epoch {epoch + 1}/{CFG.EPOCHS} started")
         
        for batch_idx, (images, labels) in enumerate(train_loader, start=1): 
            batch_start = time.time() 
            images = images.to(CFG.DEVICE, non_blocking=True) 
            labels = labels.to(CFG.DEVICE, non_blocking=True) 
 
            optimizer.zero_grad(set_to_none=True) 
            logits = model(images).squeeze(1) 
            loss = criterion(logits, labels)  
            loss.backward() 
            torch.nn.utils.clip_grad_norm_(filter(lambda p: p.requires_grad, model.parameters()), max_norm=2.0) 
            optimizer.step() 
            running_loss += loss.item() * images.size(0) 
 
            if batch_idx == 1 or batch_idx % CFG.PRINT_EVERY_N_BATCHES == 0 or batch_idx == len(train_loader): 
                seen = batch_idx * CFG.BATCH_SIZE 
                avg_loss = running_loss / max(1, min(seen, len(train_loader.dataset))) 
                with torch.no_grad(): 
                    batch_pred_mean = prediction_from_logits(logits).mean().item() 
                    batch_label_mean = labels.mean().item() 
                    high_ratio = (labels >= 0.70).float().mean().item() 
                log_step( 
                    f"Epoch {epoch + 1}/{CFG.EPOCHS} | " 
                    f"batch {batch_idx}/{len(train_loader)} | " 
                    f"loss={loss.item():.4f} | avg_loss={avg_loss:.4f} | " 
                    f"pred_mean={batch_pred_mean:.3f} | label_mean={batch_label_mean:.3f} | " 
                    f"high_labels={high_ratio * 100:.1f}% | batch_time={time.time() - batch_start:.2f}s" 
                ) 
 
        scheduler.step() 
        train_loss = running_loss / len(train_loader.dataset) 
        log_step(f"Epoch {epoch + 1}/{CFG.EPOCHS} training done in {time.time() - epoch_start:.1f}s | Train loss: {train_loss:.4f}") 
        val_mae, _ = evaluate_model(model, val_loader, "Validation", print_samples=False) 
 
        if val_mae < best_val_mae: 
            best_val_mae = val_mae 
            torch.save(model.state_dict(), CFG.MODEL_SAVE_PATH) 
            log_step(f"Saved best model: {CFG.MODEL_SAVE_PATH} | best_val_mae={best_val_mae:.4f}") 
        else: 
            log_step(f"No improvement. Best validation MAE remains {best_val_mae:.4f}") 
 
    log_step("Training complete.") 
 
    if os.path.exists(CFG.TEST_DIR): 
        log_step(f"Final test evaluation using folder: {CFG.TEST_DIR}") 
        test_dataset = SmartBlurDataset( 
            CFG.TEST_DIR, 
            samples_per_image=CFG.SAMPLES_PER_IMAGE_EVAL, 
            training=False, 
        ) 
        test_loader = DataLoader( 
            test_dataset, 
            batch_size=CFG.BATCH_SIZE, 
            shuffle=False, 
            **loader_kwargs, 
        ) 
        model.load_state_dict(torch.load(CFG.MODEL_SAVE_PATH, map_location=CFG.DEVICE)) 
        evaluate_model(model, test_loader, "Test", print_samples=True) 
    else: 
        log_step(f"Test folder not found, skipped final test: {CFG.TEST_DIR}") 
 
 
if __name__ == "__main__": 
    train_model()