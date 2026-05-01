import re


_CLAIM_ID_PATTERN = re.compile(r"Claim ID:\s*(.+)")
_AMOUNT_PATTERN = re.compile(r"Claim Amount:\s*([0-9]+(?:\.[0-9]+)?)")
_SUMMARY_PATTERN = re.compile(r"Summary:\s*(.+)")


def extract_claim_output_locally(document_text, *, fallback_claim_id):
    claim_id = _match_group(_CLAIM_ID_PATTERN, document_text) or fallback_claim_id
    amount_text = _match_group(_AMOUNT_PATTERN, document_text)
    summary = _match_group(_SUMMARY_PATTERN, document_text)

    return {
        "claim_id": claim_id,
        "amount": float(amount_text) if amount_text else None,
        "summary": summary or "Claim document received but no summary could be extracted.",
    }


def _match_group(pattern, text):
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1).strip()
