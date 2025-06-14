import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id = os.getenv('aws_public_key'),
    aws_secret_access_key = os.getenv('aws_secret_key'),
)

s3_bucket_name = 'card-prices-data-lake'

s3 = session.resource('s3')
bucket = s3.Bucket(s3_bucket_name)

print("Downloading files from S3")
for obj in bucket.objects.filter(Prefix="mtg-daily-prices/"):
    target = os.path.join(s3_bucket_name, obj.key)
    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))
    if obj.key[-1] == '/':
        continue
    if not os.path.exists(target):
        print("downloading {} to {}".format(obj.key, target))
        bucket.download_file(obj.key, target)
print("Download complete")