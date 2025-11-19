#!/usr/bin/env python3
import os

import aws_cdk as cdk

from crm_cdk.crm_cdk_stack import CrmCdkStack


app = cdk.App()
CrmCdkStack(app, "CrmCdkStack",
    env=cdk.Environment(
        account=os.getenv("AWS_ACCOUNT_ID"),
        region=os.getenv("AWS_REGION")
    )
)

app.synth()
