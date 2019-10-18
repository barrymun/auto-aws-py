import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")


class VPCScenario2():
    def __init__(self):
        self.set_ec2_client()
        self.set_ec2_resource()

    prefix = "auto_aws_py_"
    ec2_client = None
    ec2_resource = None

    def get_ec2_client(self):
        return self.ec2_client

    def set_ec2_client(self):
        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )
        self.ec2_client = ec2_client

    def get_ec2_resource(self):
        return self.ec2_resource

    def set_ec2_resource(self):
        ec2_resource = boto3.resource(
            'ec2',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )
        self.ec2_resource = ec2_resource

    def describe_addresses(self) -> dict:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-elastic-ip-addresses.html#describe-elastic-ip-addresses
        """
        filters = [
            {'Name': 'domain', 'Values': ['vpc']}
        ]
        response = self.get_ec2_client().describe_addresses(
            Filters=filters,
        )
        return response

    def allocate_address(self) -> dict:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-elastic-ip-addresses.html#allocate-and-associate-an-elastic-ip-address-with-an-amazon-ec2-instance
        """
        try:
            return self.get_ec2_client().allocate_address(Domain='vpc')
        except ClientError as e:
            print(e)
            return {}

    def release_address(self, allocation_id: str) -> dict:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-elastic-ip-addresses.html#release-an-elastic-ip-address
        """
        try:
            return self.get_ec2_client().release_address(AllocationId=allocation_id)
        except ClientError as e:
            print(e)
            return {}

    def create_vpc(self) -> dict:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_vpc
        """
        vpc = self.get_ec2_resource().create_vpc(
            CidrBlock='10.0.0.0/16',
        )
        vpc.create_tags(
            Tags=[
                {
                    "Key": "Name",
                    "Value": "{}vpc".format(self.prefix),
                }
            ],
        )
        vpc.wait_until_available()
        return vpc


if __name__ == "__main__":
    instance = VPCScenario2()

    # r = instance.allocate_address()
    # print(r)
    # print("")

    # r = instance.describe_addresses()
    # print(r)
    # print("")

    r = instance.create_vpc()
    print(r)
    print("")
