from numbers import Real


CLAIM_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "claim_id": {"type": "string", "minLength": 1},
        "amount": {"type": ["number", "null"], "minimum": 0},
        "summary": {"type": "string", "minLength": 1},
    },
    "required": ["claim_id", "amount", "summary"],
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

    amount = output["amount"]
    if amount is not None:
        if not isinstance(amount, Real) or isinstance(amount, bool):
            raise ValueError("amount must be a number or null")
        if amount < 0:
            raise ValueError("amount must be greater than or equal to 0")
        amount = float(amount)

    summary = output["summary"]
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("summary must be a non-empty string")

    return {
        "claim_id": claim_id.strip(),
        "amount": amount,
        "summary": summary.strip(),
    }


def build_claim_output(claim_id, amount, summary):
    return validate_claim_output(
        {
            "claim_id": claim_id,
            "amount": amount,
            "summary": summary,
        }
    )
