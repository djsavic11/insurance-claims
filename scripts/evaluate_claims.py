import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    import boto3
except ImportError:  # pragma: no cover - optional for local-only evaluation runs.
    boto3 = None

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.lib.bedrock_extraction import extract_claim_output_with_bedrock
from src.lib.claim_document import extract_pdf_text
from src.lib.claim_output import build_claim_output
from src.lib.local_extraction import extract_claim_output_locally


DEFAULT_INPUT_DIR = REPO_ROOT / "data" / "evaluation" / "input"
DEFAULT_EXPECTED_DIR = REPO_ROOT / "data" / "evaluation" / "expected"
DEFAULT_RESULTS_DIR = REPO_ROOT / "data" / "evaluation" / "results"
DEFAULT_BEDROCK_DIR = REPO_ROOT / "data" / "evaluation" / "bedrock-evaluation"
DEFAULT_METRICS = [
    "Builtin.Correctness",
    "Builtin.Completeness",
    "Builtin.Faithfulness",
    "Builtin.Coherence",
    "Builtin.Helpfulness",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run local-first evaluation across claim documents, compare up to 2 models, "
            "and optionally submit an Amazon Bedrock Evaluation job."
        )
    )
    parser.add_argument(
        "--models",
        nargs="+",
        help=(
            "One or two model identifiers. Use 'local-fallback' to run regex extraction. "
            "If omitted, defaults to BEDROCK_MODEL_ID or local-fallback."
        ),
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Evaluation input PDF directory (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--expected-dir",
        type=Path,
        default=DEFAULT_EXPECTED_DIR,
        help=f"Expected answer JSON directory (default: {DEFAULT_EXPECTED_DIR})",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=DEFAULT_RESULTS_DIR,
        help=f"Evaluation results directory (default: {DEFAULT_RESULTS_DIR})",
    )
    parser.add_argument(
        "--bedrock-artifacts-dir",
        type=Path,
        default=DEFAULT_BEDROCK_DIR,
        help=f"Bedrock evaluation artifact directory (default: {DEFAULT_BEDROCK_DIR})",
    )
    parser.add_argument(
        "--max-docs",
        type=int,
        default=0,
        help="Optional cap for number of documents to evaluate (0 = all).",
    )
    parser.add_argument(
        "--amount-tolerance",
        type=float,
        default=0.01,
        help="Numeric tolerance for claim_amount comparison.",
    )
    parser.add_argument(
        "--bedrock-region",
        default=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        help="AWS region for Bedrock and S3 clients (defaults from environment).",
    )
    parser.add_argument(
        "--bedrock-eval-s3-input-uri",
        help="S3 URI for uploading Bedrock evaluation prompt dataset JSONL.",
    )
    parser.add_argument(
        "--bedrock-eval-s3-output-uri",
        help="S3 URI where Bedrock evaluation job writes results.",
    )
    parser.add_argument(
        "--bedrock-eval-role-arn",
        help="IAM role ARN Bedrock assumes for evaluation jobs.",
    )
    parser.add_argument(
        "--bedrock-eval-evaluator-model",
        help="Evaluator model identifier for Bedrock model-as-judge jobs.",
    )
    parser.add_argument(
        "--bedrock-eval-task-type",
        default="General",
        help="Bedrock evaluation task type (default: General).",
    )
    parser.add_argument(
        "--bedrock-eval-metrics",
        nargs="+",
        default=DEFAULT_METRICS,
        help="Bedrock evaluation metric names.",
    )
    parser.add_argument(
        "--start-bedrock-eval-job",
        action="store_true",
        help=(
            "If set, call CreateEvaluationJob for a model-as-judge workflow "
            "using precomputed inference responses."
        ),
    )
    parser.add_argument(
        "--enable-console-cors",
        action="store_true",
        help=(
            "Document-only flag to tag the run when Bedrock evaluation S3 CORS is needed "
            "(console-created jobs)."
        ),
    )
    return parser.parse_args()


def ensure_dirs(*directories):
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def determine_models(args):
    configured = args.models or []
    if not configured:
        env_model = os.getenv("BEDROCK_MODEL_ID", "").strip()
        configured = [env_model] if env_model else ["local-fallback"]

    if len(configured) > 2:
        raise ValueError("Evaluation supports at most 2 models per run")
    return configured


def list_documents(input_dir, max_docs):
    docs = sorted(input_dir.glob("*.pdf"))
    if max_docs and max_docs > 0:
        return docs[:max_docs]
    return docs


def load_expected(expected_dir, stem):
    path = expected_dir / f"{stem}.json"
    if not path.exists():
        raise ValueError(f"Missing expected-answer file: {path}")
    with path.open("r", encoding="utf-8") as expected_file:
        return json.load(expected_file)


def run_evaluation(args):
    models = determine_models(args)
    ensure_dirs(args.results_dir, args.bedrock_artifacts_dir)
    documents = list_documents(args.input_dir, args.max_docs)
    if not documents:
        raise ValueError(f"No PDF files found in {args.input_dir}")

    bedrock_client = None
    if any(model != "local-fallback" for model in models):
        if not args.bedrock_region:
            raise ValueError(
                "AWS region is required when using Bedrock models. Set --bedrock-region or AWS_REGION."
            )
        if boto3 is None:
            raise ValueError("boto3 is required to call Bedrock models.")
        bedrock_client = boto3.client("bedrock-runtime", region_name=args.bedrock_region)

    run_started_at = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    results = []

    for document_path in documents:
        document_bytes = document_path.read_bytes()
        parse_start = time.perf_counter()
        document_text = extract_pdf_text(document_bytes)
        parse_ms = elapsed_ms(parse_start)
        expected = load_expected(args.expected_dir, document_path.stem)

        for model_id in models:
            result = evaluate_document_with_model(
                document_path=document_path,
                document_text=document_text,
                expected=expected,
                model_id=model_id,
                bedrock_client=bedrock_client,
                amount_tolerance=args.amount_tolerance,
                parse_ms=parse_ms,
            )
            results.append(result)

    summary = build_summary(results)
    result_payload = {
        "run_started_at_utc": run_started_at,
        "models": models,
        "input_dir": str(args.input_dir),
        "expected_dir": str(args.expected_dir),
        "document_count": len(documents),
        "record_count": len(results),
        "results": results,
        "summary": summary,
        "notes": {
            "latency_interpretation": "Directional metric for PoC comparison; not a production benchmark.",
            "console_cors_mode": bool(args.enable_console_cors),
        },
    }

    results_path = args.results_dir / f"evaluation-run-{run_started_at}.json"
    with results_path.open("w", encoding="utf-8") as output_file:
        json.dump(result_payload, output_file, indent=2)

    bedrock_dataset_path = args.bedrock_artifacts_dir / f"bedrock-eval-input-{run_started_at}.jsonl"
    dataset_records = create_bedrock_dataset_records(results)
    write_jsonl(bedrock_dataset_path, dataset_records)

    bedrock_reference = {
        "dataset_local_path": str(bedrock_dataset_path),
        "dataset_record_count": len(dataset_records),
        "dataset_format": (
            "Model-as-judge BYOI prompt dataset with precomputed responses. "
            "Each record includes prompt, category, optional referenceResponse, and modelResponses."
        ),
        "s3_input_uri": None,
        "evaluation_jobs": [],
    }

    if args.bedrock_eval_s3_input_uri:
        bedrock_reference["s3_input_uri"] = upload_to_s3(
            local_path=bedrock_dataset_path,
            destination_uri=args.bedrock_eval_s3_input_uri,
            region=args.bedrock_region,
        )

    if args.start_bedrock_eval_job:
        if not args.bedrock_eval_s3_input_uri:
            raise ValueError(
                "Bedrock evaluation job start requires --bedrock-eval-s3-input-uri."
            )
        for model_identifier, model_records in group_records_by_model_identifier(
            dataset_records
        ).items():
            model_dataset_path = (
                args.bedrock_artifacts_dir
                / f"bedrock-eval-input-{run_started_at}-{model_identifier}.jsonl"
            )
            write_jsonl(model_dataset_path, model_records)
            model_dataset_s3_uri = upload_to_s3(
                local_path=model_dataset_path,
                destination_uri=args.bedrock_eval_s3_input_uri,
                region=args.bedrock_region,
            )
            job_arn, request_path, response_path = start_bedrock_evaluation_job(
                args=args,
                dataset_s3_uri=model_dataset_s3_uri,
                model_identifier=model_identifier,
                run_timestamp=run_started_at,
            )
            bedrock_reference["evaluation_jobs"].append(
                {
                    "model_identifier": model_identifier,
                    "dataset_local_path": str(model_dataset_path),
                    "dataset_s3_uri": model_dataset_s3_uri,
                    "evaluation_job_arn": job_arn,
                    "evaluation_job_request_path": str(request_path),
                    "evaluation_job_response_path": str(response_path),
                }
            )

    bedrock_reference_path = (
        args.bedrock_artifacts_dir / f"bedrock-eval-reference-{run_started_at}.json"
    )
    with bedrock_reference_path.open("w", encoding="utf-8") as reference_file:
        json.dump(bedrock_reference, reference_file, indent=2)

    print(json.dumps({"results_path": str(results_path), "bedrock_reference": bedrock_reference}, indent=2))


def evaluate_document_with_model(
    *,
    document_path,
    document_text,
    expected,
    model_id,
    bedrock_client,
    amount_tolerance,
    parse_ms,
):
    fallback_claim_id = document_path.stem
    extract_start = time.perf_counter()
    extraction_error = None
    schema_error = None

    try:
        if model_id == "local-fallback":
            raw_output = extract_claim_output_locally(
                document_text, fallback_claim_id=fallback_claim_id
            )
        else:
            raw_output = extract_claim_output_with_bedrock(
                document_text,
                bedrock_client=bedrock_client,
                model_id=model_id,
            )
    except Exception as exc:  # pragma: no cover - network/model failures expected in integration runs.
        raw_output = {}
        extraction_error = str(exc)

    extract_ms = elapsed_ms(extract_start)

    validate_start = time.perf_counter()
    validated_output = None
    if not extraction_error:
        try:
            validated_output = build_claim_output(
                claim_id=raw_output.get("claim_id") or fallback_claim_id,
                claimant_name=raw_output.get("claimant_name"),
                policy_number=raw_output.get("policy_number"),
                incident_date=raw_output.get("incident_date"),
                claim_amount=raw_output.get("claim_amount", raw_output.get("amount")),
                incident_description=raw_output.get("incident_description"),
                summary=raw_output.get("summary")
                or f"Claim document received from {document_path.name}",
            )
        except Exception as exc:
            schema_error = str(exc)
    validate_ms = elapsed_ms(validate_start)

    total_ms = parse_ms + extract_ms + validate_ms
    scoring = score_structured_fields(
        expected=expected,
        actual=validated_output or {},
        amount_tolerance=amount_tolerance,
    )

    return {
        "document": document_path.name,
        "document_stem": document_path.stem,
        "model_identifier": model_id,
        "schema_valid": validated_output is not None,
        "extraction_error": extraction_error,
        "schema_error": schema_error,
        "output": validated_output,
        "field_results": scoring["field_results"],
        "structured_field_accuracy": scoring["accuracy"],
        "structured_fields_scored": scoring["scored_fields"],
        "summary_quality_reference": {
            "mode": "amazon-bedrock-evaluation",
            "status": "pending",
        },
        "timing_ms": {
            "parse": parse_ms,
            "extract": extract_ms,
            "validate": validate_ms,
            "total_processing": total_ms,
        },
    }


def score_structured_fields(*, expected, actual, amount_tolerance):
    field_results = {}
    scored = 0
    passed = 0

    checks = {
        "claim_id": compare_string(expected.get("claim_id"), actual.get("claim_id"), normalize=True),
        "claimant_name": compare_string(
            expected.get("claimant_name"), actual.get("claimant_name"), normalize=True
        ),
        "policy_number": compare_string(
            expected.get("policy_number"), actual.get("policy_number"), normalize=True
        ),
        "incident_date": compare_dates(expected.get("incident_date"), actual.get("incident_date")),
        "claim_amount": compare_amounts(
            expected.get("claim_amount"), actual.get("claim_amount"), amount_tolerance
        ),
    }

    if expected.get("incident_description") is not None:
        checks["incident_description"] = compare_string(
            expected.get("incident_description"),
            actual.get("incident_description"),
            normalize=True,
        )

    for field_name, is_match in checks.items():
        field_results[field_name] = is_match
        scored += 1
        if is_match:
            passed += 1

    accuracy = round(passed / scored, 4) if scored else 0.0
    return {"field_results": field_results, "scored_fields": scored, "accuracy": accuracy}


def build_summary(results):
    aggregate = {}
    for row in results:
        model = row["model_identifier"]
        aggregate.setdefault(
            model,
            {
                "records": 0,
                "schema_valid_count": 0,
                "total_accuracy": 0.0,
                "total_processing_ms": 0.0,
            },
        )
        bucket = aggregate[model]
        bucket["records"] += 1
        bucket["total_accuracy"] += row["structured_field_accuracy"]
        bucket["total_processing_ms"] += row["timing_ms"]["total_processing"]
        if row["schema_valid"]:
            bucket["schema_valid_count"] += 1

    summary = {}
    for model, bucket in aggregate.items():
        count = bucket["records"] or 1
        summary[model] = {
            "records": bucket["records"],
            "schema_valid_rate": round(bucket["schema_valid_count"] / count, 4),
            "average_structured_field_accuracy": round(bucket["total_accuracy"] / count, 4),
            "average_total_processing_ms": round(bucket["total_processing_ms"] / count, 2),
        }
    return summary


def create_bedrock_dataset_records(results):
    records = []
    for row in results:
        if not row["schema_valid"] or not row.get("output"):
            continue
        summary = row["output"].get("summary")
        if not summary:
            continue

        prompt = (
            "Summarize this insurance claim in a concise and accurate way. "
            "Include claimant, policy, incident date, claim amount, and incident context when available.\n\n"
            f"Document ID: {row['document_stem']}\n"
            f"Extracted data:\n{json.dumps(row['output'], ensure_ascii=True)}"
        )

        record = {
            "prompt": prompt,
            "category": row["document_stem"],
            "modelResponses": [
                {
                    "response": summary,
                    "modelIdentifier": sanitize_identifier(row["model_identifier"]),
                }
            ],
        }
        records.append(record)

    return records


def group_records_by_model_identifier(records):
    grouped = {}
    for record in records:
        model_responses = record.get("modelResponses") or []
        if len(model_responses) != 1:
            raise ValueError("Each Bedrock Evaluation BYOI record must have one model response")
        model_identifier = model_responses[0].get("modelIdentifier")
        if not model_identifier:
            raise ValueError("Each Bedrock Evaluation BYOI record needs a modelIdentifier")
        grouped.setdefault(model_identifier, []).append(record)
    return grouped


def write_jsonl(path, records):
    with path.open("w", encoding="utf-8") as dataset_file:
        for record in records:
            dataset_file.write(json.dumps(record, ensure_ascii=True))
            dataset_file.write("\n")


def upload_to_s3(*, local_path, destination_uri, region):
    if not region:
        raise ValueError("AWS region is required to upload dataset to S3")
    if boto3 is None:
        raise ValueError("boto3 is required to upload datasets to S3.")
    bucket, key_prefix = parse_s3_uri(destination_uri)
    key_prefix = key_prefix.rstrip("/")
    destination_key = (
        f"{key_prefix}/{local_path.name}" if key_prefix else local_path.name
    )
    s3_client = boto3.client("s3", region_name=region)
    s3_client.upload_file(str(local_path), bucket, destination_key)
    return f"s3://{bucket}/{destination_key}"


def start_bedrock_evaluation_job(*, args, dataset_s3_uri, model_identifier, run_timestamp):
    if not dataset_s3_uri:
        raise ValueError(
            "Bedrock evaluation job start requires --bedrock-eval-s3-input-uri (upload target)."
        )
    required = {
        "bedrock_eval_s3_output_uri": args.bedrock_eval_s3_output_uri,
        "bedrock_eval_role_arn": args.bedrock_eval_role_arn,
        "bedrock_eval_evaluator_model": args.bedrock_eval_evaluator_model,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise ValueError(
            "Missing required arguments for CreateEvaluationJob: "
            + ", ".join(f"--{name.replace('_', '-')}" for name in missing)
        )
    if not args.bedrock_region:
        raise ValueError("AWS region is required to start Bedrock evaluation jobs")
    if boto3 is None:
        raise ValueError("boto3 is required to create Bedrock evaluation jobs.")
    if not model_identifier:
        raise ValueError("No model identifiers available for precomputed inference source")

    client = boto3.client("bedrock", region_name=args.bedrock_region)
    job_name = create_evaluation_job_name(run_timestamp, model_identifier)

    request_body = {
        "jobName": job_name,
        "jobDescription": "Insurance claims summary quality evaluation (model-as-judge)",
        "applicationType": "ModelEvaluation",
        "roleArn": args.bedrock_eval_role_arn,
        "evaluationConfig": {
            "automated": {
                "datasetMetricConfigs": [
                    {
                        "taskType": args.bedrock_eval_task_type,
                        "dataset": {
                            "name": "claims_summary_dataset",
                            "datasetLocation": {"s3Uri": dataset_s3_uri},
                        },
                        "metricNames": args.bedrock_eval_metrics,
                    }
                ],
                "evaluatorModelConfig": {
                    "bedrockEvaluatorModels": [
                        {"modelIdentifier": args.bedrock_eval_evaluator_model}
                    ]
                },
            }
        },
        "inferenceConfig": {
            "models": [
                {
                    "precomputedInferenceSource": {
                        "inferenceSourceIdentifier": model_identifier
                    }
                }
            ]
        },
        "outputDataConfig": {"s3Uri": args.bedrock_eval_s3_output_uri},
    }

    request_path = args.bedrock_artifacts_dir / f"bedrock-eval-request-{run_timestamp}.json"
    with request_path.open("w", encoding="utf-8") as request_file:
        json.dump(request_body, request_file, indent=2)

    response = client.create_evaluation_job(**request_body)
    response_path = args.bedrock_artifacts_dir / f"bedrock-eval-response-{run_timestamp}.json"
    with response_path.open("w", encoding="utf-8") as response_file:
        json.dump(response, response_file, indent=2)

    return response.get("jobArn"), request_path, response_path


def parse_s3_uri(uri):
    parsed = urlparse(uri)
    if parsed.scheme != "s3" or not parsed.netloc:
        raise ValueError(f"Invalid S3 URI: {uri}")
    return parsed.netloc, parsed.path.lstrip("/")


def compare_string(expected, actual, *, normalize):
    if expected is None and actual is None:
        return True
    if expected is None or actual is None:
        return False
    expected_text = normalize_text(expected) if normalize else str(expected)
    actual_text = normalize_text(actual) if normalize else str(actual)
    return expected_text == actual_text


def compare_dates(expected, actual):
    if expected is None and actual is None:
        return True
    if expected is None or actual is None:
        return False
    return normalize_date(expected) == normalize_date(actual)


def compare_amounts(expected, actual, tolerance):
    if expected is None and actual is None:
        return True
    if expected is None or actual is None:
        return False
    try:
        expected_value = float(expected)
        actual_value = float(actual)
    except (TypeError, ValueError):
        return False
    return abs(expected_value - actual_value) <= tolerance


def normalize_text(value):
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_date(value):
    value = str(value).strip()
    return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")


def sanitize_identifier(value):
    sanitized = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-")
    return sanitized[:256] if sanitized else "model"


def create_evaluation_job_name(run_timestamp, model_identifier):
    timestamp = run_timestamp.lower().replace("t", "-").replace("z", "")
    model_part = re.sub(r"[^a-z0-9-]+", "-", model_identifier.lower()).strip("-")
    model_part = model_part[:24].strip("-") or "model"
    return f"claims-eval-{timestamp}-{model_part}"[:63].strip("-")


def elapsed_ms(start):
    return round((time.perf_counter() - start) * 1000, 2)


def main():
    args = parse_args()
    run_evaluation(args)


if __name__ == "__main__":
    main()
