# -*- coding:utf-8 -*-

"""Classes for S3 Buckets."""


from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError


class BucketManager:
    """Manage a s3 Bucket."""


    def __init__(self, session):
        """Create a BucketManager object."""
        self.session = session
        self.s3 = self.session.resource('s3')


    def all_buckets(self):
        """Get an Iterator for all s3 buckets."""
        return self.s3.buckets.all()


    def all_objects(self, bucket_name):
        """Get an iterator for all objects of a bucket."""
        return self.s3.Bucket(bucket_name).objects.all()


    def init_bucket(self, bucket_name):
        """Create Bucket or return existing Bucket."""
        s3_bucket=None
        try:
            s3_bucket=self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint':self.session.region_name}
            )
            s3_bucket.upload_file('index.html',
                                  'index.html',
                                  ExtraArgs={'ContentType':'text/html'}
                )
        except ClientError as error:
            if error.response['Error']['Code']=='BucketAlreadyOwnedByYou':
                s3_bucket=self.s3.Bucket(bucket_name)
            else:
                raise error

        return s3_bucket


    def set_policy(self, bucket):
        """Set Policy for the Bucket to be publicly readable."""
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
        """%bucket.name
        policy=policy.strip()

        pol=bucket.Policy()
        pol.put(Policy=policy)


    def configure_website(self, bucket):
        """Configure given Bucket for static website hosting."""
        website = bucket.Website()
        website.put(WebsiteConfiguration={
            'ErrorDocument':{'Key':'error.html'},
            'IndexDocument':{'Suffix':'index.html'
            }
        })


    @staticmethod
    def upload_file(bucket, path, key):
        """Upload file from given path in given bucket with given key."""
        content_type=mimetypes.guess_type(key)[0] or 'text/plain'

        return bucket.upload_file(path,
                              key,
                              ExtraArgs={'ContentType':content_type}
        )


    def sync(self, pathname, bucket_name):
        """Sync files in given directory to given bucket."""
        bucket = self.s3.Bucket(bucket_name)
        root=Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.upload_file(bucket,str(p),str(p.relative_to(root)))

        handle_directory(root)
