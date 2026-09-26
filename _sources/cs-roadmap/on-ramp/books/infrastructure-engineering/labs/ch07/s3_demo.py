"""Use object storage the way an app would: with a limited access key."""
import os

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id=os.environ["S3_ACCESS_KEY"],
    aws_secret_access_key=os.environ["S3_SECRET_KEY"],
    region_name="us-east-1",
)


def read(bucket, key):
    return s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode()


def attempt(label, action):
    try:
        result = action()
    except ClientError as error:
        print(f"DENIED  {label}: {error.response['Error']['Code']}")
        return
    print(f"OK      {label}", result if isinstance(result, (str, list)) else "")


attempt("upload uploads/hello.txt",
        lambda: s3.put_object(Bucket="uploads", Key="hello.txt", Body=b"hi!"))
attempt("read uploads/hello.txt", lambda: read("uploads", "hello.txt"))
attempt("read billing/report.csv", lambda: read("billing", "report.csv"))
attempt("delete uploads/hello.txt",
        lambda: s3.delete_object(Bucket="uploads", Key="hello.txt"))
attempt("list all buckets",
        lambda: [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]])
