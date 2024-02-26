import boto3
import os, json

def get_s3_resource():
    with open('secrets.json', 'r') as file:
        data = json.load(file)
        access_key_id = data['aws_access_key_id']
        secret_key = data['aws_secret_access_key']

    return boto3.resource(
        service_name='s3',
        region_name='ap-south-1',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_key
    )

def image2url(file_path, object_name=None):
    bucket_name = 'eyes-of-tryon'
    if object_name is None:
        object_name = file_path

    s3 = get_s3_resource()
    s3.Bucket(bucket_name).upload_file(Filename=file_path, Key=object_name)
    public_url = f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{object_name}"
    return public_url