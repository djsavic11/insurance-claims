import re


_CLAIM_ID_PATTERN = re.compile(r"Claim ID:\s*(.+)")
_CLAIMANT_NAME_PATTERN = re.compile(r"Claimant Name:\s*(.+)")
_POLICY_NUMBER_PATTERN = re.compile(r"Policy Number:\s*(.+)")
_INCIDENT_DATE_PATTERN = re.compile(r"Incident Date:\s*(\d{4}-\d{2}-\d{2})")
_CLAIM_AMOUNT_PATTERN = re.compile(r"Claim Amount:\s*([0-9]+(?:\.[0-9]+)?)")
_INCIDENT_DESCRIPTION_PATTERN = re.compile(r"Incident Description:\s*(.+)")
_SUMMARY_PATTERN = re.compile(r"Summary:\s*(.+)")


def extract_claim_output_locally(document_text, *, fallback_claim_id):
    claim_id = _match_group(_CLAIM_ID_PATTERN, document_text) or fallback_claim_id
    claimant_name = _match_group(_CLAIMANT_NAME_PATTERN, document_text)
    policy_number = _match_group(_POLICY_NUMBER_PATTERN, document_text)
    incident_date = _match_group(_INCIDENT_DATE_PATTERN, document_text)
    claim_amount_text = _match_group(_CLAIM_AMOUNT_PATTERN, document_text)
    incident_description = _match_group(_INCIDENT_DESCRIPTION_PATTERN, document_text)
    summary = _match_group(_SUMMARY_PATTERN, document_text)

    return {
        "claim_id": claim_id,
        "claimant_name": claimant_name,
        "policy_number": policy_number,
        "incident_date": incident_date,
        "claim_amount": float(claim_amount_text) if claim_amount_text else None,
        "incident_description": incident_description,
        "summary": summary or "Claim document received but no summary could be extracted.",
    }


def _match_group(pattern, text):
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1).strip()
