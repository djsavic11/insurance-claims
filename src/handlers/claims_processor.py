from src.lib.s3_event import extract_first_s3_object, fallback_claim_id


def lambda_handler(event, context):
    try:
        object_ref = extract_first_s3_object(event)
        claim_id = fallback_claim_id(object_ref["key"])
        summary = f"Received claim document from s3://{object_ref['bucket']}/{object_ref['key']}"
    except ValueError as exc:
        claim_id = "unknown"
        summary = str(exc)

    return {
        "claim_id": claim_id,
        "amount": None,
        "summary": summary,
    }
