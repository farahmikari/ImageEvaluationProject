import _compat_patch  # noqa: F401  (لازم قبل أي شي تاني)
from experta import KnowledgeEngine
import csv
from experta import KnowledgeEngine
from Facts import Score, Quality, Explanation
from EngineInference import EngineRules

CSV_COLUMN_TO_CRITERION = {
    "lighting_score": "lighting",
    "clarity_score": "blur",
    "pose_score": "pose",
    "eye_score": "eye_open",
}


def _to_float_or_none(raw: str):
    raw = (raw or "").strip()
    return float(raw) if raw else None


def load_rows(csv_path: str):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run_one_image(row: dict) :
    """Declares Score facts only for criteria that HAVE a value; missing
    ones are simply never declared, which is what makes the
    NOT(Score(name=...)) undetected-rules fire."""
    engine = EngineRules()
    engine.reset()

    for column, criterion in CSV_COLUMN_TO_CRITERION.items():
        value = _to_float_or_none(row.get(column))
        if value is not None:
            engine.declare(Score(name=criterion, value=value))
        # else: no Score declared for this criterion -> "undetected" path

    engine.run()

    quality_facts = [f for f in engine.facts.values() if isinstance(f, Quality)]
    explanation_facts = [f for f in engine.facts.values() if isinstance(f, Explanation)]
    return quality_facts, explanation_facts
def run_all(csv_path: str):
    results = []
    for row in load_rows(csv_path):
        image = row["image"]
        quality_facts, explanation_facts = run_one_image(row)   # ← فك التوبل صح
        quality = quality_facts[0] if quality_facts else None
        reasons = [e["reason"] for e in explanation_facts]
        results.append((image, quality, reasons))
    return results


if __name__ == "__main__":
    for image, quality, reasons in run_all(               # ← ثلاث عناصر مو اثنين
        "C:/Users/XPRISTO/Desktop/Four/KPS/project/ImageEvaluationProject/Results/final_scores.csv"
    ):
        print("-" * 60)
        if quality is None:
            print(f"{image}: NO QUALITY FACT PRODUCED (check rule coverage)")
        else:
            print(f"{image}: label={quality['label']:6s} value={quality['value']:.2f}")
        for reason in reasons:
            print(f"reason: {reason}")