import cv2
import numpy as np
import os

# تأكدي من وضع مسار صورتكِ الواضحة هنا
IMAGE_PATH = "C:/Users/asus/Pictures/test images/image_test.jpg"
OUTPUT_DIR = "./blur_score_assessment/test/blur_samples_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. قراءة الصورة الأصلية (الواضحة)
img = cv2.imread(IMAGE_PATH)
if img is None:
    print(f"❌ لم يتم العثور على الصورة في المسار: {IMAGE_PATH}")
    exit()

cv2.imwrite(f"{OUTPUT_DIR}/1_clear.jpg", img)

# 2. غباش جواسيان
gaussian = cv2.GaussianBlur(img, (29, 29), sigmaX=4.5)
cv2.imwrite(f"{OUTPUT_DIR}/2_gaussian.jpg", gaussian)

# 3. غباش حركي (خفيف)
kernel_light = np.zeros((15, 15), dtype=np.float32)
kernel_light[7, :] = 1.0
matrix_light = cv2.getRotationMatrix2D((7, 7), 45, 1.0)
kernel_light = cv2.warpAffine(kernel_light, matrix_light, (15, 15))
kernel_light /= kernel_light.sum()
motion_light = cv2.filter2D(img, -1, kernel_light)
cv2.imwrite(f"{OUTPUT_DIR}/3_motion_light.jpg", motion_light)

# 4. غباش حركي (قوي)
kernel_heavy = np.zeros((45, 45), dtype=np.float32)
kernel_heavy[22, :] = 1.0
matrix_heavy = cv2.getRotationMatrix2D((22, 22), 45, 1.0)
kernel_heavy = cv2.warpAffine(kernel_heavy, matrix_heavy, (45, 45))
kernel_heavy /= kernel_heavy.sum()
motion_heavy = cv2.filter2D(img, -1, kernel_heavy)
cv2.imwrite(f"{OUTPUT_DIR}/4_motion_heavy.jpg", motion_heavy)

# 5. غباش عدم تركيز (خفيف)
radius_light = 5
size_l = radius_light * 2 + 1
y_l, x_l = np.ogrid[-radius_light:radius_light +
                    1, -radius_light:radius_light + 1]
mask_l = (x_l * x_l + y_l * y_l) <= radius_light * radius_light
kernel_defocus_l = np.zeros((size_l, size_l), dtype=np.float32)
kernel_defocus_l[mask_l] = 1.0
kernel_defocus_l /= kernel_defocus_l.sum()
defocus_light = cv2.filter2D(img, -1, kernel_defocus_l)
cv2.imwrite(f"{OUTPUT_DIR}/5_defocus_light.jpg", defocus_light)

# 6. غباش عدم تركيز (قوي)
radius_heavy = 25
size_h = radius_heavy * 2 + 1
y_h, x_h = np.ogrid[-radius_heavy:radius_heavy +
                    1, -radius_heavy:radius_heavy + 1]
mask_h = (x_h * x_h + y_h * y_h) <= radius_heavy * radius_heavy
kernel_defocus_h = np.zeros((size_h, size_h), dtype=np.float32)
kernel_defocus_h[mask_h] = 1.0
kernel_defocus_h /= kernel_defocus_h.sum()
defocus_heavy = cv2.filter2D(img, -1, kernel_defocus_h)
cv2.imwrite(f"{OUTPUT_DIR}/6_defocus_heavy.jpg", defocus_heavy)

print(f"🎯 تم توليد الصور الست وحفظها بنجاح في المجلد: {OUTPUT_DIR}")
