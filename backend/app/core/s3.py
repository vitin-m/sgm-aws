import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.core import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

def upload_file_to_s3(file_obj, filename):
    try:
        response = s3_client.upload_fileobj(
            file_obj,
            settings.AWS_S3_BUCKET_NAME,
            filename,
            ExtraArgs={"ACL": "public-read"},
        )
        file_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
        return file_url
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to upload file to S3: {e}")

def delete_file_from_s3(filename):
    try:
        s3_client.delete_object(
            Bucket=settings.AWS_S3_BUCKET_NAME,
            Key=filename,
        )
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to delete file from S3: {e}")
    
