def trapmf(x: float, a: float, b: float, c: float, d: float) -> float:
    eps = 1e-9
    rising = 1.0 if x >= b else max(0.0, (x - a) / (b - a + eps))
    falling = 1.0 if x <= c else max(0.0, (d - x) / (d - c + eps))
    return min(1.0, rising, falling)

MF_PARAMS = {
    "low":    (0,   0, 25, 45),
    "medium": (30, 45, 60, 75),
    "high":   (55, 75, 100, 100),
}
def compute_memberships(value: float) -> dict:
    x = max(0.0, min(100.0, value))
    return {label: round(trapmf(x, *params), 4) for label, params in MF_PARAMS.items()}
