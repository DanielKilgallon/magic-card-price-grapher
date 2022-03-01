import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id = os.getenv('public_key'),
    aws_secret_access_key = os.getenv('secret_key'),
)

# s3_resource = session.resource('s3')
def download_s3_folder(bucket_name, s3_folder, local_dir=None):
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
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

print("Downloading files from S3")
download_s3_folder('card-prices-data-lake', 'daily-files/')
print("Download complete")