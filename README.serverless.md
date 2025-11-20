# Django CRM - Serverless Edition

This is the **serverless** version of the original Django CRM application, redesigned to leverage AWS services like Lambda, API Gateway, and DynamoDB using AWS CDK.

## Overview

This version refactors the traditional Django CRUD app by outsourcing backend data operations to **AWS Lambda functions**, triggered through **API Gateway**. Infrastructure is defined and managed using **AWS CDK**.

## Architecture

- **Frontend**: Django with Bootstrap templates.
- **Authentication**: Handled entirely by Django using session-based login.
- **Backend Logic**: CRUD operations are offloaded to:
  - `save_record.py` → Create records
  - `get_records.py` → List records
  - `record_by_id.py` → Retrieve a single record
- **Infrastructure**:
  - Defined in `crm-cdk/` using AWS CDK (Python)
  - Deploys API Gateway, Lambda functions, DynamoDB table

## Record Format

Example payload expected by `save_record.py`:

```json
{
  "first_name": "Ana",
  "last_name": "Marin",
  "email": "ana@example.com",
  "phone": "0912345678",
  "address": "Some Street, Split",
  "city": "Split",
  "zipcode": "21000"
}
```

---

## How We Set It Up

### 1. Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version  # should show installed CLI version
```

### 2. Install Node.js and AWS CDK

```bash
sudo apt install -y nodejs npm # if not already installed
npm install -g aws-cdk
cdk --version  # show CDK version
```

### 3. Initialize CDK App (in project root)

```bash
mkdir crm-cdk && cd crm-cdk
cdk init app --language python
```

### 4. Set up Python environment (separate from the Django one)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt  # if requirements.txt exists

# Or install manually
pip install aws-cdk-lib constructs
```

### 5. Bootstrap AWS environment

```bash
aws configure  # set up credentials (access key, region, etc.)
aws sts get-caller-identity  # verify connection
cdk bootstrap aws://<account-id>/<region>
```

### 6. Define resources in `crm-cdk/crm_cdk_stack.py`

- DynamoDB table for records
- Three Lambda functions:
  - save_record.py
  - get_records.py
  - record_by_id.py
- API Gateway to expose these

### 7. Deploy infrastructure

```bash
cdk deploy
```

> You should get an API Gateway URL like:  
> `https://<your-api-id>.execute-api.<region>.amazonaws.com/prod/`


## 8. Teardown (if needed)

To remove all AWS resources created:

```bash
cd crm-cdk/
cdk destroy
```

---

## Other Info

- The previous README still exists in [`README.md`](README.md)
- This one is `README.serverless.md` and documents the newer AWS-based architecture
