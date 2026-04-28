# S3 Lambda Pipeline 🚀

In h
A serverless pipeline that automatically processes files uploaded to an Amazon S3 bucket using AWS Lambda running inside a Docker container hosted on Amazon ECR.

---

## Architecture

```
File Upload
    ↓
Amazon S3 Bucket
    ↓  (ObjectCreated event)
AWS Lambda Function
    ↓  (container image pulled from)
Amazon ECR
    ↓  (reads file metadata via)
Amazon S3 (head_object)
    ↓
CloudWatch Logs
```

---

## What It Does

Every time a file is uploaded to the S3 bucket, Lambda is triggered automatically and logs:

- 📦 The bucket name
- 📄 The file name
- 📏 The file size
- 🔍 The file content type

---

## Project Structure

```
s3-lambda-pipeline/
├── app.py               ← Lambda handler
├── requirements.txt     ← Python dependencies
├── Dockerfile           ← Container definition
├── .dockerignore        ← Files excluded from the Docker image
└── README.md            ← You are here
```

---

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- An AWS account

> **Important:** In Docker Desktop go to Settings → General and **uncheck** `Use containerd for pulling and storing images`. Without this Docker will produce manifest lists that Lambda rejects.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/jackonshiundu/s3-lambda-project.git
cd s3-lambda-project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure the AWS CLI

```bash
aws configure
```

Fill in the prompts with your IAM credentials:

```
AWS Access Key ID:     [your key]
AWS Secret Access Key: [your secret]
Default region name:   us-east-1
Default output format: json
```

Verify with:

```bash
aws sts get-caller-identity
```

---

## Deployment

### 1. Build the Docker Image

```bash
docker buildx build --platform linux/amd64 --provenance=false --load -t s3-lambda-function:latest .
```

### 2. Test Locally

```bash
docker run --platform linux/amd64 -p 9000:8080 s3-lambda-function app.lambda_handler
```

In a second terminal:

```bash
curl.exe -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -H "Content-Type: application/json" -d "{\"Records\":[{\"s3\":{\"bucket\":{\"name\":\"my-test-bucket\"},\"object\":{\"key\":\"hello.txt\",\"size\":1024}}}]}"
```

Expected response:

```json
{ "statusCode": 200, "body": "\"S3 event processed successfully\"" }
```

### 3. Push to ECR

Authenticate:

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR-ACCOUNT-ID>.dkr.ecr.us-east-1.amazonaws.com
```

Tag and push:

```bash
docker tag s3-lambda-function:latest <YOUR-ACCOUNT-ID>.dkr.ecr.us-east-1.amazonaws.com/s3-lambda-function:latest

docker push <YOUR-ACCOUNT-ID>.dkr.ecr.us-east-1.amazonaws.com/s3-lambda-function:latest
```

> Replace `<YOUR-ACCOUNT-ID>` with your AWS account ID. Find it with: `aws sts get-caller-identity --query "Account" --output text`

---

## AWS Setup (Console)

### IAM Role

Create a role named `lambda-s3-execution-role` with these policies attached:

- `AWSLambdaBasicExecutionRole`
- `AmazonS3ReadOnlyAccess`

### Lambda Function

- **Name:** `s3-event-processor`
- **Type:** Container image
- **Image:** `<YOUR-ACCOUNT-ID>.dkr.ecr.us-east-1.amazonaws.com/s3-lambda-function:latest`
- **Memory:** 256 MB
- **Timeout:** 30 seconds
- **Role:** `lambda-s3-execution-role`

### S3 Bucket

Create a bucket named `s3-lambda-trigger-yourname-2026` in `us-east-1`.

### S3 Trigger

Go to Lambda → s3-event-processor → Add trigger → S3 → select your bucket → All object create events.

---

## Updating the Function

After making changes to `app.py`:

```bash
docker buildx build --platform linux/amd64 --provenance=false --load -t s3-lambda-function:latest .
docker tag s3-lambda-function:latest <YOUR-ACCOUNT-ID>.dkr.ecr.us-east-1.amazonaws.com/s3-lambda-function:latest
docker push <YOUR-ACCOUNT-ID>.dkr.ecr.us-east-1.amazonaws.com/s3-lambda-function:latest
```

Then in the Lambda console go to **Image → Deploy new image** and select the latest digest.

---

## Viewing Logs

1. Go to **Lambda → s3-event-processor → Monitor**
2. Click **View CloudWatch logs**
3. Click the most recent log stream

---

## Clean Up

To avoid unnecessary AWS charges, delete these resources when done:

| Resource             | Where                                     |
| -------------------- | ----------------------------------------- |
| S3 Bucket            | https://console.aws.amazon.com/s3         |
| Lambda Function      | https://console.aws.amazon.com/lambda     |
| ECR Repository       | https://console.aws.amazon.com/ecr        |
| IAM Role             | https://console.aws.amazon.com/iam        |
| CloudWatch Log Group | https://console.aws.amazon.com/cloudwatch |

---

## Tech Stack

- **Python 3.11**
- **Docker**
- **Amazon ECR**
- **AWS Lambda**
- **Amazon S3**
- **Amazon CloudWatch**

---

_Built with ❤️ — happy coding! 🚀_
