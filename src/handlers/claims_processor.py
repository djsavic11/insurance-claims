import argparse
import json
from pathlib import Path

if __package__ in (None, ""):
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from lib.s3_event import extract_first_s3_object, fallback_claim_id
else:
    from ..lib.s3_event import extract_first_s3_object, fallback_claim_id


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

    response = lambda_handler(_load_event(args.event), None)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
