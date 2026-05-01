import json
import re


_JSON_BLOCK_PATTERN = re.compile(r"\{.*\}", re.DOTALL)

_SYSTEM_PROMPT = (
    "You extract structured insurance claim data from claim documents. "
    "Return only valid JSON with the keys claim_id, amount, and summary. "
    "Use null for amount if it cannot be determined. "
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
                            "Return JSON with claim_id, amount, and summary only.\n\n"
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
    return {
        "claim_id": payload.get("claim_id"),
        "amount": payload.get("amount"),
        "summary": payload.get("summary"),
    }
