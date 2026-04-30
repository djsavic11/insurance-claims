CLAIM_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "claim_id": {"type": "string"},
        "amount": {"type": ["number", "null"]},
        "summary": {"type": "string"},
    },
    "required": ["claim_id", "amount", "summary"],
    "additionalProperties": False,
}


def build_claim_output(claim_id, amount, summary):
    return {
        "claim_id": claim_id,
        "amount": amount,
        "summary": summary,
    }
