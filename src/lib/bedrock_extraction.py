import json
import re

from .prompt_templates import PromptTemplateManager


_JSON_BLOCK_PATTERN = re.compile(r"\{.*\}", re.DOTALL)
_PROMPTS = PromptTemplateManager()
_CLAIM_EXTRACTION_PROMPT = "bedrock/claim_extraction.md"


def extract_claim_output_with_bedrock(document_text, *, bedrock_client, model_id):
    prompt = _PROMPTS.render_chat(_CLAIM_EXTRACTION_PROMPT, document_text=document_text)

    response = bedrock_client.converse(
        modelId=model_id,
        system=[{"text": prompt.system}],
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt.user}],
            }
        ],
        inferenceConfig=prompt.inference_config,
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
