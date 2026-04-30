from pathlib import PurePosixPath
from urllib.parse import unquote_plus


def extract_first_s3_object(event):
    records = event.get("Records") or []
    if not records:
        raise ValueError("No S3 records found in event")

    first_record = records[0]
    s3_data = first_record.get("s3") or {}
    bucket_name = (s3_data.get("bucket") or {}).get("name")
    object_key = (s3_data.get("object") or {}).get("key")

    if not bucket_name or not object_key:
        raise ValueError("S3 event is missing bucket name or object key")

    return {
        "bucket": bucket_name,
        "key": unquote_plus(object_key),
    }


def fallback_claim_id(object_key):
    claim_id = PurePosixPath(object_key).stem.strip()
    return claim_id or "unknown"
