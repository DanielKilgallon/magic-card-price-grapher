import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id = os.getenv('aws_public_key'),
    aws_secret_access_key = os.getenv('aws_secret_key'),
)

s3_folder = 'daily-files/'
local_dir = None

s3 = session.resource('s3')
bucket = s3.Bucket('card-prices-data-lake')

print("Downloading files from S3")
for obj in bucket.objects.filter(Prefix=s3_folder):
    target = obj.key if local_dir is None \
        else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))
    if obj.key[-1] == '/':
        continue
    if not os.path.exists(target):
        print("downloading {} to {}".format(obj.key, target))
        bucket.download_file(obj.key, target)
print("Download complete")