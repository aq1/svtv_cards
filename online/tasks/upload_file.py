import os.path

import boto3
from django.conf import settings
from nanoid import generate

from project.celery import app


class UploadError(Exception):
    pass


@app.task
def upload_file(filename, _file, content_type):
    sts_client = boto3.client('sts')
    assumed_role_object = sts_client.assume_role(
        RoleArn=settings.AWS_ROLE_ARN,
        RoleSessionName='AssumeRoleSession1'
    )
    credentials = assumed_role_object['Credentials']
    s3_client = boto3.client(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    key = '_s3/' + generate() + os.path.splitext(filename)[-1]
    response = s3_client.put_object(
        Body=_file.read(),
        Key=key,
        Bucket=settings.AWS_BUCKET,
        ContentType=content_type,
    )

    try:
        code = response['ResponseMetadata']['HTTPStatusCode']
    except KeyError:
        raise UploadError()

    if code != 200:
        raise UploadError()

    return f'/{key}'



