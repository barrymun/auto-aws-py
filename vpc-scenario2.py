import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

if __name__ == "__main__":
    print(AWS_ACCESS_KEY_ID)

    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    filters = [
        {'Name': 'domain', 'Values': ['vpc']}
    ]
    response = ec2.describe_addresses(
        Filters=filters
    )
    print(response)
