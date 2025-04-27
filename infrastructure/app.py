#!/usr/bin/env python3
import os
from aws_cdk import App, Environment

from infrastructure.infrastructure_stack import InfrastructureStack

app = App()
InfrastructureStack(app, "ClaimBuddyInfrastructure",
    env=Environment(
        account=os.getenv('AWS_ACCOUNT_ID'),
        region=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
)

app.synth()
