#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Webtron automated the process of deploying static websites to AWS.

- Crate and Configure S3 buckets
- Enable Static websiote hosting on them
- Deploy local files to buckets
"""


import boto3
import botocore
import click
from bucket import BucketManager


session = None
bucket_manager = None
s3 = None


def create_bucket():
    """Create Bucket."""
    location = {'LocationConstraint': 'ap-southeast-2'}
    try:
        s3.create_bucket(Bucket='automating-aws-project',CreateBucketConfiguration=location)
    except:
        print("Error in creating bucket")


@click.group()
@click.option('--profile', default=None,
    help = "Use given profile name.")
def cli(profile):
    """Webtron deploys websites to s3 bucket."""
    global session, bucket_manager, s3
    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    else:
        session_cfg['profile_name'] = 'pythonAutomation'

    session=boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)
    s3=session.resource('s3')


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets available in the account."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.option('--bucket',help='List objects for specific bucket with given name')
def list_bucket_objects(bucket):
    """List objects in a given bucket."""
    buckets=bucket_manager.all_buckets()
    if bucket and bucket_manager.s3.Bucket(name=bucket) in buckets:
        print("Found bucket with given name "+bucket_manager.s3.Bucket(bucket).name)
        for obj in bucket_manager.all_objects(bucket):
            print(obj)
    else:
        for b in buckets:
            print("Objects in bucket: "+b.name+"\n")
            for obj in bucket_manager.all_objects(b.name):
                print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure s3 bucket."""
    s3_bucket=bucket_manager.init_bucket(bucket)

    bucket_manager.set_policy(s3_bucket)

    bucket_manager.configure_website(s3_bucket)

    url="http://%s.s3-website.ap-southeast-2.amazonaws.com"%s3_bucket.name

    print(s3_bucket)
    print("Access website in new bucket at "+url)
    return


@cli.command('sync')
@click.argument('pathname',type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname,bucket):
    """Sync contents of PATHNAME to Bucket."""

    bucket_manager.sync(pathname, bucket)
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))


if __name__=='__main__':
    cli()
