from audit.detectors import (
    find_hallucination_signals,
    find_bias_signals,
    extract_factual_claims,
)

SEVERITY_PENALTIES = {
    "low": 3,
    "medium": 8,
    "high": 15,
}

def compute_trust_score(text: str) -> dict:
    all_findings = []

    all_findings += find_hallucination_signals(text)
    all_findings += find_bias_signals(text)
    all_findings += extract_factual_claims(text)

    score = 100

    for finding in all_findings:
        score -= SEVERITY_PENALTIES.get(finding["severity"], 0)

    score = max(0, min(100, score))

    if score >= 85:
        label = "Trustworthy"
    elif score >= 60:
        label = "Use With Caution"
    elif score >= 35:
        label = "Significant Concerns"
    else:
        label = "High Risk"

    explanation = build_explanation(score, label, all_findings)

    return {
        "trust_score": score,
        "label": label,
        "flags": all_findings,
        "explanation": explanation,
    }

def build_explanation(score: int, label: str, findings: list[dict]) -> str:
    if not findings:
        return (
            f"Trust score: {score}/100 ({label}). No hallucination signals, "
            f"loaded language, or flagged numeric claims were detected. This "
            f"does not guarantee factual accuracy — only that no automated "
            f"warning signs were present."
        )

    categories = {}

    for f in findings:
        categories[f["category"]] = categories.get(f["category"], 0) + 1

    parts = [
        f"{count} {category.replace('_', ' ')} issue(s)"
        for category, count in categories.items()
    ]

    summary = ", ".join(parts)

    return (
        f"Trust score: {score}/100 ({label}). Detected: {summary}. "
        f"See the flags list for full detail on each specific issue and where it occurs."
    )