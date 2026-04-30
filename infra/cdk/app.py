#!/usr/bin/env python3

import aws_cdk as cdk

from stacks.claims_processing_stack import ClaimsProcessingStack


app = cdk.App()

ClaimsProcessingStack(app, "InsuranceClaimsProcessingStack")

app.synth()
