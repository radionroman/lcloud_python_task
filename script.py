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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List files in the bucket or upload a file to the bucket')
    parser.add_argument('operation', type=str, help='list or upload')
    parser.add_argument('--file_name', type=str, help='Name of the file to upload')
    args = parser.parse_args()
    if args.operation == 'list':
        list_files(bucket_name, prefix)
    elif args.operation == 'upload':
        if args.file_name:
            object_name = prefix + os.path.basename(args.file_name)
            upload_file(args.file_name, bucket_name, object_name)
        else:
            print("Please provide the name of the file to upload.")
    else:
        print("Invalid operation. Please use 'list' or 'upload'.")
