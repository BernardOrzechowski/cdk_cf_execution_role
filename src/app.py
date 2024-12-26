#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from hello_cdk.hello_cdk_stack import (
#     StackImportingBucket,  # noqa: E501
#     StackWithBucketExport,
# )

app = cdk.App()

env = (
    cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

# stack_with_bucket_export = StackWithBucketExport(
#     app,
#     "StackWithBucketExport",
#     env=cdk.Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"),
#         region=os.getenv("CDK_DEFAULT_REGION"),
#     ),
# )
# stack_importing_bucket = StackImportingBucket(
#     app,
#     "StackImportingBucket",
#     imported_bucket=stack_with_bucket_export.bucket,
#     env=cdk.Environment(
#         account=os.getenv("CDK_DEFAULT_ACCOUNT"),
#         region=os.getenv("CDK_DEFAULT_REGION"),
#     ),
# )

app.synth()
