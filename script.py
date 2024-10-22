import boto3
import os
import re
import argparse
from botocore.exceptions import NoCredentialsError, ClientError
#load the environment variables
from dotenv import load_dotenv
load_dotenv()

# get the access key and secret key from the .env file
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = 'developer-task'
prefix = 'y-wing/'

s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def list_files(bucket_name, prefix):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print("No files found.")
    except ClientError as e:
        print(f"Error: {e}")

def upload_file(file_name, bucket_name, object_name):
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded successfully to {object_name}.")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
        
def list_files_with_regex(bucket_name, prefix, pattern):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                if re.search(pattern, obj['Key']):
                    print(obj['Key'])
        else:
            print("No files found.")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="S3 CLI using boto3")
    parser.add_argument('action', choices=['list', 'upload', 'list_regex'], help='Action to perform')
    parser.add_argument('--file', help='File to upload')
    parser.add_argument('--object', help='S3 object key for upload')
    parser.add_argument('--pattern', help='Regex pattern to filter files')

    args = parser.parse_args()

    if args.action == 'list':
        list_files(bucket_name, prefix)
    elif args.action == 'upload':
        if args.file and args.object:
            upload_file(args.file, bucket_name, f"{prefix}{args.object}")
        else:
            print("Please provide --file and --object for uploading.")
    elif args.action == 'list_regex':
        if args.pattern:
            list_files_with_regex(bucket_name, prefix, args.pattern)
        else:
            print("Please provide --pattern for listing files with regex.")
