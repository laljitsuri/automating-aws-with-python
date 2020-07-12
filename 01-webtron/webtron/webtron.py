#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Webtron automated the process of deploying static websites to AWS.

- Crate and Configure S3 buckets
- Enable Static websiote hosting on them
- Deploy local files to buckets
"""

from pathlib import Path
import mimetypes
import boto3
import botocore
from botocore.exceptions import ClientError
import click


session=boto3.Session(profile_name='pythonAutomation')
s3=session.resource('s3')


def create_bucket():
    """Create Bucket."""
    location = {'LocationConstraint': 'ap-southeast-2'}
    try:
        s3.create_bucket(Bucket='automating-aws-project',CreateBucketConfiguration=location)
    except:
        print("Error in creating bucket")


@click.group()
def cli():
    """Webtron deploys websites to s3 bucket."""


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets available in the account."""
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')
@click.option('--bucket',help='List objects for specific bucket with given name')
def list_bucket_objects(bucket):
    """List objects in a given bucket."""
    buckets=s3.buckets.all()
    if bucket and s3.Bucket(name=bucket) in buckets:
        print("Found bucket with given name "+s3.Bucket(bucket).name)
        for obj in s3.Bucket(bucket).objects.all():
            print(obj)
    else:
        for b in buckets:
            print("Objects in bucket: "+b.name+"\n")
            for obj in b.objects.all():
                print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure s3 bucket."""
    s3_bucket=None
    try:
        s3_bucket=s3.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={'LocationConstraint':session.region_name}
        )
        s3_bucket.upload_file('index.html',
                              'index.html',
                              ExtraArgs={'ContentType':'text/html'}
            )
    except ClientError as e:
        if e.response['Error']['Code']=='BucketAlreadyOwnedByYou':
            s3_bucket=s3.Bucket(bucket)
        else:
            raise e

    policy="""
    {
        "Version": "2012-10-17",
        "Statement": [{
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": [
            "s3:GetObject"
        ],
        "Resource": [
            "arn:aws:s3:::%s/*"
        ]
        }]
    }
    """%s3_bucket.name
    policy=policy.strip()

    pol=s3_bucket.Policy()
    pol.put(Policy=policy)

    ws=s3_bucket.Website()
    ws.put(WebsiteConfiguration={
        'ErrorDocument':{'Key':'error.html'},
        'IndexDocument':{'Suffix':'index.html'
        }
    })

    url="http://%s.s3-website.ap-southeast-2.amazonaws.com"%s3_bucket.name

    print(s3_bucket)
    print("Access website in new bucket at "+url)
    return


def upload_file(s3_bucket,path,key):
    """Upload file from given path in given bucket with given key."""
    content_type=mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(path,
                          key,
                          ExtraArgs={'ContentType':content_type}
    )


@cli.command('sync')
@click.argument('pathname',type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname,bucket):
    """Sync contents of PATHNAME to Bucket."""
    s3_bucket=s3.Bucket(bucket)
    root=Path(pathname).expanduser().resolve()

    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir():handle_directory(p)
            if p.is_file():upload_file(s3_bucket,str(p),str(p.relative_to(root)))

    handle_directory(root)


if __name__=='__main__':
    cli()
