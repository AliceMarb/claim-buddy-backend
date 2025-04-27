# ClaimBuddy Infrastructure

This directory contains the AWS CDK infrastructure code for ClaimBuddy's backend services.

## Prerequisites

- Python 3.x
- Node.js (v18.x, v20.x, or v22.x recommended)
- AWS CLI configured
- AWS CDK CLI installed (`npm install -g aws-cdk`)

## Setup

1. Create a virtual environment and install dependencies:
```bash
python -m venv .venv-cdk
source .venv-cdk/bin/activate
pip install -r cdk-requirements.txt
```

2. Set up required environment variables:
```bash
# AWS Credentials
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_ACCOUNT_ID=your_aws_account_id
export AWS_DEFAULT_REGION=us-east-1  # or your preferred region

# Optional: Silence Node.js version warning if using v23+
export JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=true
```

## Deployment

To deploy the infrastructure:

```bash
cdk deploy
```

This will create:
- An S3 bucket for document storage with versioning enabled
- CORS configuration for frontend access
- IAM permissions for presigned URL uploads

After deployment, the S3 bucket name will be output to the console. Add this to your backend's `.env` file as `AWS_S3_BUCKET_NAME`.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
