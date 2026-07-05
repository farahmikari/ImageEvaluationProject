def trapmf(x: float, a: float, b: float, c: float, d: float) -> float:
    eps = 1e-9
    rising  = (x - a) / (b - a + eps)
    falling = (d - x) / (d - c + eps)
    return max(0.0, min(1.0, rising, falling))

MF_PARAMS = {
    "low":    (0,   0, 25, 45),
    "medium": (30, 45, 60, 75),
    "high":   (55, 75, 100, 100),
}
def compute_memberships(value: float) -> dict:
    x = max(0.0, min(100.0, value))
    return {label: round(trapmf(x, *params), 4) for label, params in MF_PARAMS.items()}
## return  {
  #  "low":0.0,
  #  "medium":0.47,
  #  "high":0.65
#}