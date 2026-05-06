from pathlib import Path

from aws_cdk import Aws, CfnOutput, Duration, RemovalPolicy, Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as aws_lambda
from aws_cdk import aws_logs as logs
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_notifications as s3_notifications
from aws_cdk import custom_resources as cr
from constructs import Construct


class ClaimsProcessingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo_root = Path(__file__).resolve().parents[3]
        bedrock_model_id = (
            self.node.try_get_context("bedrockModelId")
            or "anthropic.claude-3-haiku-20240307-v1:0"
        )
        bedrock_log_prefix = "bedrock-invocation-logs"

        claims_bucket = s3.Bucket(
            self,
            "ClaimsBucket",
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
                "CLAIMS_BUCKET_NAME": claims_bucket.bucket_name,
                "OUTPUT_PREFIX": "processed",
                "BEDROCK_MODEL_ID": bedrock_model_id,
            },
        )

        claims_bucket.grant_read_write(claims_processor)
        claims_processor.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
                resources=["*"],
            )
        )

        bedrock_invocation_log_group = logs.LogGroup(
            self,
            "BedrockInvocationLogGroup",
            log_group_name=f"/aws/bedrock/modelinvocations/{self.stack_name}",
            removal_policy=RemovalPolicy.DESTROY,
        )
        # CloudFormation returns the log group ARN with a trailing :*, which produces
        # an invalid log-stream resource if we append :log-stream to it directly.
        bedrock_invocation_log_group_resource_arn = (
            f"arn:{Aws.PARTITION}:logs:{Aws.REGION}:{Aws.ACCOUNT_ID}:"
            f"log-group:{bedrock_invocation_log_group.log_group_name}"
        )

        bedrock_invocation_logs_role = iam.Role(
            self,
            "BedrockInvocationLogsRole",
            assumed_by=iam.ServicePrincipal(
                "bedrock.amazonaws.com",
                conditions={
                    "StringEquals": {"aws:SourceAccount": Aws.ACCOUNT_ID},
                    "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock:{Aws.REGION}:{Aws.ACCOUNT_ID}:*"},
                },
            ),
        )
        bedrock_invocation_logs_role.add_to_policy(
            iam.PolicyStatement(
                actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                resources=[
                    (
                        f"{bedrock_invocation_log_group_resource_arn}:"
                        "log-stream:aws/bedrock/modelinvocations"
                    )
                ],
            )
        )

        claims_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                sid="AllowBedrockInvocationLogsWrite",
                effect=iam.Effect.ALLOW,
                principals=[iam.ServicePrincipal("bedrock.amazonaws.com")],
                actions=["s3:PutObject"],
                resources=[claims_bucket.arn_for_objects(f"{bedrock_log_prefix}/*")],
                conditions={
                    "StringEquals": {"aws:SourceAccount": Aws.ACCOUNT_ID},
                    "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock:{Aws.REGION}:{Aws.ACCOUNT_ID}:*"},
                },
            )
        )

        bedrock_logging_configuration = {
            "cloudWatchConfig": {
                "logGroupName": bedrock_invocation_log_group.log_group_name,
                "roleArn": bedrock_invocation_logs_role.role_arn,
                "largeDataDeliveryS3Config": {
                    "bucketName": claims_bucket.bucket_name,
                    "keyPrefix": bedrock_log_prefix,
                },
            },
            "s3Config": {
                "bucketName": claims_bucket.bucket_name,
                "keyPrefix": bedrock_log_prefix,
            },
            "textDataDeliveryEnabled": True,
        }

        bedrock_invocation_logging = cr.AwsCustomResource(
            self,
            "BedrockInvocationLogging",
            install_latest_aws_sdk=True,
            on_create=cr.AwsSdkCall(
                service="Bedrock",
                action="putModelInvocationLoggingConfiguration",
                parameters={"loggingConfig": bedrock_logging_configuration},
                physical_resource_id=cr.PhysicalResourceId.of(
                    f"{self.stack_name}-bedrock-invocation-logging"
                ),
            ),
            on_update=cr.AwsSdkCall(
                service="Bedrock",
                action="putModelInvocationLoggingConfiguration",
                parameters={"loggingConfig": bedrock_logging_configuration},
                physical_resource_id=cr.PhysicalResourceId.of(
                    f"{self.stack_name}-bedrock-invocation-logging"
                ),
            ),
            on_delete=cr.AwsSdkCall(
                service="Bedrock",
                action="deleteModelInvocationLoggingConfiguration",
            ),
            policy=cr.AwsCustomResourcePolicy.from_statements(
                [
                    iam.PolicyStatement(
                        actions=[
                            "bedrock:PutModelInvocationLoggingConfiguration",
                            "bedrock:DeleteModelInvocationLoggingConfiguration",
                        ],
                        resources=["*"],
                    ),
                    iam.PolicyStatement(
                        actions=["iam:PassRole"],
                        resources=[bedrock_invocation_logs_role.role_arn],
                        conditions={
                            "StringEquals": {
                                "iam:PassedToService": "bedrock.amazonaws.com"
                            }
                        },
                    ),
                ]
            ),
        )
        bedrock_invocation_logging.node.add_dependency(bedrock_invocation_log_group)
        bedrock_invocation_logging.node.add_dependency(bedrock_invocation_logs_role)
        bedrock_invocation_logging.node.add_dependency(claims_bucket)

        claims_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(claims_processor),
            s3.NotificationKeyFilter(prefix="claims/"),
        )

        CfnOutput(
            self,
            "ClaimsBucketName",
            value=claims_bucket.bucket_name,
        )
        CfnOutput(
            self,
            "ClaimsProcessorFunctionName",
            value=claims_processor.function_name,
        )
        CfnOutput(
            self,
            "BedrockInvocationLogsPrefix",
            value=bedrock_log_prefix,
        )
        CfnOutput(
            self,
            "BedrockInvocationLogGroupName",
            value=bedrock_invocation_log_group.log_group_name,
        )
        CfnOutput(
            self,
            "BedrockInvocationLogsRoleArn",
            value=bedrock_invocation_logs_role.role_arn,
        )
