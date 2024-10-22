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

if __name__ == '__main__':
    print(f"Listing files in bucket {bucket_name} with prefix {prefix}")
    print(f"")
    list_files(bucket_name, "y_wing/")
