import re

OVERCONFIDENT_PHRASES = [
    "always",
    "never",
    "guaranteed",
    "100% certain",
    "undeniably",
    "without question",
    "impossible to dispute",
    "everyone knows",
]

FAKE_CITATION_PATTERN = re.compile(
    r"\(?\b(?:study|research|paper|report)\b[^.]{0,40}\b(?:shows|proves|confirms|found)\b",
    re.IGNORECASE,
)

def find_hallucination_signals(text: str) -> list[dict]:
    findings = []
    lowered = text.lower()

    for phrase in OVERCONFIDENT_PHRASES:
        if phrase in lowered:
            findings.append({
                "category": "hallucination_risk",
                "detail": (
                    f'Overconfident absolute language detected: "{phrase}". '
                    f"Claims stated with total certainty deserve extra scrutiny."
                ),
                "severity": "medium",
            })

    if FAKE_CITATION_PATTERN.search(text):
        findings.append({
            "category": "hallucination_risk",
            "detail": (
                "Text references a study/research/report making a claim, "
                "but no verifiable source, author, or publication is named. "
                "Unsourced citations are a common hallucination pattern."
            ),
            "severity": "high",
        })

    return findings


LOADED_TERMS = {
    "obviously": "Implies a claim requires no justification, discouraging scrutiny.",
    "clearly superior": "Asserts superiority without supporting evidence.",
    "everyone agrees": "Falsely implies unanimous consensus.",
    "real men": "Gendered framing that can unfairly exclude or stereotype.",
    "real women": "Gendered framing that can unfairly exclude or stereotype.",
    "those people": "Vague out-group framing that can imply unfair othering.",
    "naturally better": "Implies inherent superiority without evidence, a common bias pattern.",
}

def find_bias_signals(text: str) -> list[dict]:
    findings = []
    lowered = text.lower()

    for term, reason in LOADED_TERMS.items():
        if term in lowered:
            findings.append({
                "category": "bias",
                "detail": f'Loaded phrase "{term}" detected. {reason}',
                "severity": "medium",
            })

    return findings


NUMERIC_CLAIM_PATTERN = re.compile(
    r"\d+(\.\d+)?\s*(%|percent|million|billion|times)"
)

def extract_factual_claims(text: str) -> list[dict]:
    findings = []
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    for sentence in sentences:
        if NUMERIC_CLAIM_PATTERN.search(sentence):
            findings.append({
                "category": "factual_claim",
                "detail": (
                    f'Specific numeric claim detected and flagged for verification: '
                    f'"{sentence.strip()}"'
                ),
                "severity": "low",
            })

    return findings