import argparse
import json
import os
from pathlib import Path

if __package__ in (None, ""):
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from lib.claim_output import build_claim_output
    from lib.claim_document import extract_pdf_text, load_document_bytes, store_claim_output
    from lib.bedrock_extraction import extract_claim_output_with_bedrock
    from lib.local_extraction import extract_claim_output_locally
    from lib.s3_event import extract_first_s3_object, fallback_claim_id
else:
    from ..lib.claim_output import build_claim_output
    from ..lib.claim_document import extract_pdf_text, load_document_bytes, store_claim_output
    from ..lib.bedrock_extraction import extract_claim_output_with_bedrock
    from ..lib.local_extraction import extract_claim_output_locally
    from ..lib.s3_event import extract_first_s3_object, fallback_claim_id

try:
    import boto3
except ImportError:  # pragma: no cover - boto3 is available in Lambda, optional locally.
    boto3 = None


_LOCAL_INPUT_ROOT = Path(__file__).resolve().parents[2] / "data" / "input"
_LOCAL_OUTPUT_ROOT = Path(__file__).resolve().parents[2] / "data" / "output"


def lambda_handler(event, context):
    local_input_root = os.getenv("CLAIMS_LOCAL_INPUT_ROOT")
    local_output_root = os.getenv("CLAIMS_LOCAL_OUTPUT_ROOT")
    output_bucket_name = os.getenv("OUTPUT_BUCKET_NAME")
    output_prefix = os.getenv("OUTPUT_PREFIX", "processed")
    model_id = os.getenv("BEDROCK_MODEL_ID", "").strip()

    try:
        object_ref = extract_first_s3_object(event)
        fallback_id = fallback_claim_id(object_ref["key"])
        s3_client = _aws_client("s3")
        document_bytes = load_document_bytes(
            object_ref["bucket"],
            object_ref["key"],
            s3_client=s3_client,
            local_input_root=local_input_root,
        )
        document_text = extract_pdf_text(document_bytes)

        if model_id:
            extracted_output = extract_claim_output_with_bedrock(
                document_text,
                bedrock_client=_aws_client("bedrock-runtime"),
                model_id=model_id,
            )
        else:
            extracted_output = extract_claim_output_locally(
                document_text,
                fallback_claim_id=fallback_id,
            )

        claim_output = build_claim_output(
            claim_id=extracted_output.get("claim_id") or fallback_id,
            amount=extracted_output.get("amount"),
            summary=extracted_output.get("summary")
            or f"Claim document received from s3://{object_ref['bucket']}/{object_ref['key']}",
        )
    except ValueError as exc:
        claim_output = build_claim_output(
            claim_id="unknown",
            amount=None,
            summary=str(exc),
        )
    except Exception as exc:
        claim_output = build_claim_output(
            claim_id=fallback_claim_id(_safe_object_key(event)),
            amount=None,
            summary=f"Processing failed: {exc}",
        )

    try:
        store_claim_output(
            claim_output,
            claim_id=claim_output["claim_id"],
            output_bucket_name=output_bucket_name,
            output_prefix=output_prefix,
            s3_client=_aws_client("s3"),
            local_output_root=local_output_root,
        )
    except Exception as exc:
        claim_output = build_claim_output(
            claim_id=claim_output["claim_id"],
            amount=claim_output["amount"],
            summary=f"{claim_output['summary']} Output storage failed: {exc}",
        )

    return claim_output


def _default_event():
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "demo-claims-bucket"},
                    "object": {"key": "claims/claim-001.pdf"},
                }
            }
        ]
    }


def _load_event(event_path):
    if not event_path:
        return _default_event()

    with Path(event_path).open("r", encoding="utf-8") as event_file:
        return json.load(event_file)


def main():
    parser = argparse.ArgumentParser(
        description="Run the claims processor locally with a sample or provided S3 event."
    )
    parser.add_argument(
        "--event",
        help="Path to a JSON file containing an S3 event payload.",
    )
    args = parser.parse_args()

    os.environ.setdefault("CLAIMS_LOCAL_INPUT_ROOT", str(_LOCAL_INPUT_ROOT))
    os.environ.setdefault("CLAIMS_LOCAL_OUTPUT_ROOT", str(_LOCAL_OUTPUT_ROOT))

    response = lambda_handler(_load_event(args.event), None)
    print(json.dumps(response, indent=2))


def _aws_client(service_name):
    if boto3 is None:
        return None
    return boto3.client(service_name)


def _safe_object_key(event):
    records = event.get("Records") or []
    if not records:
        return "unknown"

    s3_data = (records[0] or {}).get("s3") or {}
    object_data = s3_data.get("object") or {}
    return object_data.get("key") or "unknown"


if __name__ == "__main__":
    main()
