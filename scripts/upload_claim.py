import argparse
from pathlib import Path

DEFAULT_FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "input" / "claim-001.pdf"
DEFAULT_OBJECT_KEY = "claims/claim-001.pdf"


def upload_claim(file_path, bucket_name, object_key, *, region_name=None):
    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError(
            "boto3 is required for uploads. Install the project dependencies first."
        ) from exc

    client = boto3.client("s3", region_name=region_name)
    client.upload_file(str(file_path), bucket_name, object_key)
    return f"s3://{bucket_name}/{object_key}"


def main():
    parser = argparse.ArgumentParser(
        description="Upload the sample insurance claim PDF to the configured S3 input bucket."
    )
    parser.add_argument(
        "--bucket",
        required=True,
        help="Name of the S3 input bucket.",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_FILE_PATH,
        help=f"Path to the claim PDF to upload. Defaults to {DEFAULT_FILE_PATH}.",
    )
    parser.add_argument(
        "--key",
        default=DEFAULT_OBJECT_KEY,
        help=f"S3 object key to use. Defaults to {DEFAULT_OBJECT_KEY}.",
    )
    parser.add_argument(
        "--region",
        help="Optional AWS region override for the S3 client.",
    )
    args = parser.parse_args()

    if not args.file.exists():
        raise FileNotFoundError(f"Claim file not found: {args.file}")

    destination = upload_claim(
        args.file,
        args.bucket,
        args.key,
        region_name=args.region,
    )
    print(destination)


if __name__ == "__main__":
    main()
