from pathlib import Path

from aws_cdk import CfnOutput, Duration, RemovalPolicy, Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as aws_lambda
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_notifications as s3_notifications
from constructs import Construct


class ClaimsProcessingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo_root = Path(__file__).resolve().parents[3]
        bedrock_model_id = (
            self.node.try_get_context("bedrockModelId")
            or "anthropic.claude-3-haiku-20240307-v1:0"
        )

        input_bucket = s3.Bucket(
            self,
            "ClaimsInputBucket",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
            enforce_ssl=True,
        )

        output_bucket = s3.Bucket(
            self,
            "ClaimsOutputBucket",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
            enforce_ssl=True,
        )

        claims_processor = aws_lambda.Function(
            self,
            "ClaimsProcessorFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="src.handlers.claims_processor.lambda_handler",
            code=aws_lambda.Code.from_asset(
                str(repo_root),
                exclude=[
                    ".git",
                    ".venv",
                    "infra/cdk/cdk.out",
                    "**/__pycache__",
                ],
            ),
            timeout=Duration.seconds(60),
            memory_size=512,
            environment={
                "INPUT_BUCKET_NAME": input_bucket.bucket_name,
                "OUTPUT_BUCKET_NAME": output_bucket.bucket_name,
                "OUTPUT_PREFIX": "processed",
                "BEDROCK_MODEL_ID": bedrock_model_id,
            },
        )

        input_bucket.grant_read(claims_processor)
        output_bucket.grant_put(claims_processor)
        claims_processor.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
                resources=["*"],
            )
        )

        input_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(claims_processor),
            s3.NotificationKeyFilter(prefix="claims/"),
        )

        CfnOutput(
            self,
            "ClaimsInputBucketName",
            value=input_bucket.bucket_name,
        )
        CfnOutput(
            self,
            "ClaimsOutputBucketName",
            value=output_bucket.bucket_name,
        )
        CfnOutput(
            self,
            "ClaimsProcessorFunctionName",
            value=claims_processor.function_name,
        )
