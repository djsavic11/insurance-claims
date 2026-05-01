import json
import re
from pathlib import Path, PurePosixPath


_PDF_TEXT_PATTERN = re.compile(r"\((.*?)(?<!\\)\)\s*Tj")


def load_document_bytes(bucket_name, object_key, *, s3_client=None, local_input_root=None):
    local_path = _resolve_local_document_path(object_key, local_input_root)
    if local_path:
        return local_path.read_bytes()

    if s3_client is None:
        raise ValueError("An S3 client is required when local input is not configured")

    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    return response["Body"].read()


def extract_pdf_text(document_bytes):
    raw_pdf = document_bytes.decode("latin-1", errors="ignore")
    lines = [_decode_pdf_string(match) for match in _PDF_TEXT_PATTERN.findall(raw_pdf)]
    text = "\n".join(line.strip() for line in lines if line.strip())
    if not text:
        raise ValueError("No readable text content could be extracted from the PDF")
    return text


def store_claim_output(
    output,
    *,
    claim_id,
    output_bucket_name=None,
    output_prefix="processed",
    s3_client=None,
    local_output_root=None,
):
    output_key = build_output_key(claim_id, output_prefix=output_prefix)
    payload = json.dumps(output, indent=2).encode("utf-8")

    if local_output_root:
        destination = Path(local_output_root) / PurePosixPath(output_key)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        return destination

    if not output_bucket_name or s3_client is None:
        raise ValueError("Output bucket and S3 client are required for persisted output")

    s3_client.put_object(
        Bucket=output_bucket_name,
        Key=output_key,
        Body=payload,
        ContentType="application/json",
    )
    return output_key


def build_output_key(claim_id, *, output_prefix="processed"):
    normalized_prefix = output_prefix.strip("/")
    filename = f"{claim_id}.json"
    if not normalized_prefix:
        return filename
    return f"{normalized_prefix}/{filename}"


def _resolve_local_document_path(object_key, local_input_root):
    if not local_input_root:
        return None

    candidate = Path(local_input_root) / PurePosixPath(object_key).name
    if candidate.exists():
        return candidate

    return None


def _decode_pdf_string(value):
    return (
        value.replace(r"\(", "(")
        .replace(r"\)", ")")
        .replace(r"\\", "\\")
        .replace(r"\n", "\n")
        .replace(r"\r", "\r")
        .replace(r"\t", "\t")
    )
