import boto3
import os

# S3 Client setup
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

def upload_file_to_s3(file_object, file_name):
    bucket_name = os.getenv('echomatelite-project')
    try:
        # S3 par file upload karna
        s3.upload_fileobj(
            file_object,
            bucket_name,
            file_name,
            # ContentType set karna zaroori hai taaki browser file ko download karne ki jagah view kar sake
            ExtraArgs={'ContentType': file_object.content_type} 
        )
        
        # File ka public S3 URL banakar return karna
        file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        return file_url
        
    except Exception as e:
        print(f"AWS S3 Upload failed: {e}")
        return None