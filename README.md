# smart-photo-album

A serverless AI-powered photo album that allows users to upload and search photos using natural language text (i.e. "Show me pictures of dogs and cats").

## System Architecture

### Frontend & API Management
- **API Gateway**: Exposes `PUT /upload` and `GET /search` endpoints secured with an API key.
    - `PUT /upload`: Uses S3 service integration to upload photos and attach custom labels as metadata.
    - `GET /search`: Uses Lambda proxy integration to search for photos.
- **Frontend**: Built with HTML, JavaScript, and Bootstrap, and connected to API Gateway via generated SDK.
- **S3**: Hosts and serves static frontend application.

### Photo Storage & Indexing
- **S3**: Stores uploaded photos along with associated metadata (including custom labels).
- **OpenSearch**: Indexes photo metadata including labels for fast lookups based on user queries.

## Event Processing Flow

### Photo Upload
- User uploads a photo along with optional custom labels through the frontend.
- The frontend calls the `PUT /upload` endpoint in **API Gateway**.
- The request is forwarded to **S3**, which stores the uploaded photo along with metadata in the storage bucket.
- **S3** triggers **Lambda (LF1)** on the photo upload, which:
    - Extracts the user-defined labels from object metadata.
    - Detects additional labels using **Rekognition**.
    - Indexes the photo metadata and these labels in **OpenSearch**.

### Photo Search
- User searches for photos using natural language text through the frontend.
- The frontend calls the `GET /search` endpoint in **API Gateway**.
- The request is forwarded to **Lambda (LF2)**, which:
    - Extracts keywords (labels) from the natural language text using **Lex**.
    - Queries **OpenSearch** for photos matching the extracted labels.
    - Returns the matching photos along with their associated labels (for demonstration purposes).

## CloudFormation Deployment

### Prerequisites

#### Environment Variables

Create file `config/.env`:

```env
OPENSEARCH_USERNAME=<master username for OpenSearch>
OPENSEARCH_PASSWORD=<master password for OpenSearch>
```

#### S3 Artifacts Bucket

- Create an S3 bucket named `cs-gy-9223-smart-photo-album-artifacts`
- Package and upload the following artifacts:
    - `lambdas/index_photos.zip`: LF1 Lambda function files
    - `lambdas/search_photos.zip`: LF2 Lambda function files
    - `layers/requests.zip`: Python requests library
    - `layers/python-dotenv.zip`: Python dotenv library

### Deployment Steps

#### 1. OpenSearch Stack

```bash
source config/.env
aws cloudformation create-stack \
  --stack-name smart-photo-album-opensearch \
  --template-body file://cloudformation/opensearch.yml \
  --parameters ParameterKey=MasterUsername,ParameterValue=$OPENSEARCH_USERNAME ParameterKey=MasterPassword,ParameterValue=$OPENSEARCH_PASSWORD \
  --capabilities CAPABILITY_NAMED_IAM
```

#### 2. Lambda Stack

```bash
source config/.env
aws cloudformation create-stack \
  --stack-name smart-photo-album-lambda \
  --template-body file://cloudformation/lambda.yml \
  --parameters ParameterKey=OpenSearchUsername,ParameterValue=$OPENSEARCH_USERNAME ParameterKey=OpenSearchPassword,ParameterValue=$OPENSEARCH_PASSWORD \
  --capabilities CAPABILITY_NAMED_IAM
```

#### 3. S3 Buckets Stack

```bash
aws cloudformation create-stack \
  --stack-name smart-photo-album-s3 \
  --template-body file://cloudformation/s3.yml \
  --capabilities CAPABILITY_NAMED_IAM
```

**Cleanup Note**: S3 buckets `cs-gy-9223-smart-photo-album` and `cs-gy-9223-smart-photo-album-storage` must be emptied manually before deleting this stack.

#### 4. API Gateway Stack

```bash
aws cloudformation create-stack \
  --stack-name smart-photo-album-apigateway \
  --template-body file://cloudformation/apigateway.yml \
  --capabilities CAPABILITY_NAMED_IAM
```

### Post Deployment Steps

#### Create OpenSearch Index

```bash
python -m opensearch.create_index
```

#### Update Frontend Configuration

Create file `frontend/config.js`:

```javascript
const CONFIG = {
    API_GATEWAY_URL: <ApiUrl from API Gateway stack output>,
    API_KEY: <Key value of ApiKeyId from API Gateway stack output>
}
```

#### Upload Frontend Files

Upload all contents from the `frontend/` directory to the S3 bucket `cs-gy-9223-smart-photo-album` (frontend hosting bucket).

## CodePipeline CI/CD

This project also includes two CI/CD pipelines to automate build and deployment. These pipelines were manually created and configured through the AWS Console and are not currently deployed via CloudFormation templates.

### Lambda Pipeline

**Source**: **GitHub App** (triggers on `main` branch pushes).

**Build**: **CodeBuild** using `codepipeline/lambda/buildspec.yml`.

**Deploy**: **CodeDeploy** (two actions) for **LF1** and **LF2**, using dynamically generated `appspec.yml` files during build.

### Frontend Pipeline

**Source**: **GitHub App** (triggers on `main` branch pushes).

**Build**: **CodeBuild** using `codepipeline/frontend/buildspec.yml`.

**Deploy**: **Amazon S3** for direct upload into the `cs-gy-9223-smart-photo-album` bucket.

## Future Improvements

The following are planned for future versions of this project:

### CloudFormation

- Add support for deploying remaining resources (Lex bot, CodePipeline pipelines).
- Create a parent stack to automate deployment of all resources in the correct order.

### Automation Scripts

- Automate full deployment, including prerequisite and post-deployment manual steps.
- Automate full teardown, including manual cleanup (i.e. emptying S3 buckets before stack deletion).