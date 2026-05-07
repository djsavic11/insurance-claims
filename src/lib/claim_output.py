from numbers import Real
from datetime import datetime


CLAIM_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "claim_id": {"type": "string", "minLength": 1},
        "claimant_name": {"type": ["string", "null"], "minLength": 1},
        "policy_number": {"type": ["string", "null"], "minLength": 1},
        "incident_date": {"type": ["string", "null"], "format": "date"},
        "claim_amount": {"type": ["number", "null"], "minimum": 0},
        "incident_description": {"type": ["string", "null"], "minLength": 1},
        "summary": {"type": "string", "minLength": 1},
    },
    "required": [
        "claim_id",
        "claimant_name",
        "policy_number",
        "incident_date",
        "claim_amount",
        "incident_description",
        "summary",
    ],
    "additionalProperties": False,
}

_REQUIRED_FIELDS = tuple(CLAIM_OUTPUT_SCHEMA["required"])
_ALLOWED_FIELDS = frozenset(CLAIM_OUTPUT_SCHEMA["properties"])


def validate_claim_output(output):
    if not isinstance(output, dict):
        raise ValueError("Claim output must be an object")

    missing_fields = [field for field in _REQUIRED_FIELDS if field not in output]
    if missing_fields:
        raise ValueError(f"Claim output is missing required fields: {', '.join(missing_fields)}")

    unexpected_fields = sorted(set(output) - _ALLOWED_FIELDS)
    if unexpected_fields:
        raise ValueError(
            f"Claim output contains unsupported fields: {', '.join(unexpected_fields)}"
        )

    claim_id = output["claim_id"]
    if not isinstance(claim_id, str) or not claim_id.strip():
        raise ValueError("claim_id must be a non-empty string")

    claimant_name = _validate_nullable_string(output["claimant_name"], "claimant_name")
    policy_number = _validate_nullable_string(output["policy_number"], "policy_number")
    incident_date = _validate_nullable_date(output["incident_date"])
    claim_amount = _validate_nullable_amount(output["claim_amount"])
    incident_description = _validate_nullable_string(
        output["incident_description"], "incident_description"
    )

    summary = output["summary"]
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("summary must be a non-empty string")

    return {
        "claim_id": claim_id.strip(),
        "claimant_name": claimant_name,
        "policy_number": policy_number,
        "incident_date": incident_date,
        "claim_amount": claim_amount,
        "incident_description": incident_description,
        "summary": summary.strip(),
    }


def build_claim_output(
    claim_id,
    *,
    claimant_name=None,
    policy_number=None,
    incident_date=None,
    claim_amount=None,
    incident_description=None,
    summary,
):
    return validate_claim_output(
        {
            "claim_id": claim_id,
            "claimant_name": claimant_name,
            "policy_number": policy_number,
            "incident_date": incident_date,
            "claim_amount": claim_amount,
            "incident_description": incident_description,
            "summary": summary,
        }
    )


def _validate_nullable_string(value, field_name):
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string or null")
    return value.strip()


def _validate_nullable_date(value):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("incident_date must be a YYYY-MM-DD string or null")
    value = value.strip()
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("incident_date must be a valid YYYY-MM-DD date or null") from exc
    return value


def _validate_nullable_amount(value):
    if value is None:
        return None
    if not isinstance(value, Real) or isinstance(value, bool):
        raise ValueError("claim_amount must be a number or null")
    if value < 0:
        raise ValueError("claim_amount must be greater than or equal to 0")
    return float(value)
