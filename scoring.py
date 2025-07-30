def compute_lead_score(row, weights=None):
    """
    Compute a weighted linear lead score.
    Normalizes certain features against assumed maxima.
    """
    if weights is None:
        weights = {
            "funding_million_usd": 0.30,
            "employee_count":      0.25,
            "revenue_million_usd": 0.20,
            "tech_score":          0.15,
            "email_validity":      0.10
        }

    # Define assumed max values for normalization
    max_vals = {
        "funding_million_usd": 100,
        "employee_count":      1000,
        "revenue_million_usd": 500
    }

    score = 0.0
    for feature, weight in weights.items():
        val = row.get(feature, 0) or 0
        if feature in max_vals:
            val = min(val / max_vals[feature], 1.0)
        score += weight * val

    return round(score, 3)