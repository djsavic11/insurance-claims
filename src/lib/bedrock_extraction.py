import json
import re


_JSON_BLOCK_PATTERN = re.compile(r"\{.*\}", re.DOTALL)

_SYSTEM_PROMPT = (
    "You extract structured insurance claim data from claim documents. "
    "Return only valid JSON with the keys claim_id, claimant_name, policy_number, "
    "incident_date, claim_amount, incident_description, and summary. "
    "Use null for any field that cannot be determined except summary. "
    "incident_date must be in YYYY-MM-DD format when available. "
    "claim_amount must be a number or null. "
    "Do not include markdown or extra commentary."
)


def extract_claim_output_with_bedrock(document_text, *, bedrock_client, model_id):
    response = bedrock_client.converse(
        modelId=model_id,
        system=[{"text": _SYSTEM_PROMPT}],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": (
                            "Extract the insurance claim data from the document text below.\n"
                            "Return JSON with claim_id, claimant_name, policy_number, "
                            "incident_date, claim_amount, incident_description, and summary only.\n"
                            "If a field is missing, return it as null.\n\n"
                            f"{document_text}"
                        )
                    }
                ],
            }
        ],
        inferenceConfig={
            "temperature": 0,
            "maxTokens": 300,
        },
    )

    return _parse_model_output(_collect_text_output(response))


def _collect_text_output(response):
    content_blocks = ((response.get("output") or {}).get("message") or {}).get("content") or []
    text_parts = [block.get("text", "") for block in content_blocks if block.get("text")]
    if not text_parts:
        raise ValueError("Bedrock returned no text content")
    return "\n".join(text_parts)


def _parse_model_output(text):
    match = _JSON_BLOCK_PATTERN.search(text)
    if not match:
        raise ValueError("Bedrock response did not contain a JSON object")

    payload = json.loads(match.group(0))
    claim_amount = payload.get("claim_amount")
    if claim_amount is None and "amount" in payload:
        claim_amount = payload.get("amount")

    return {
        "claim_id": payload.get("claim_id"),
        "claimant_name": payload.get("claimant_name"),
        "policy_number": payload.get("policy_number"),
        "incident_date": payload.get("incident_date"),
        "claim_amount": claim_amount,
        "incident_description": payload.get("incident_description"),
        "summary": payload.get("summary"),
    }
