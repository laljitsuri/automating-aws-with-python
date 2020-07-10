import boto3
import click

session=boto3.Session(profile_name='pythonAutomation')
s3=session.resource('s3')

def create_bucket():
    location = {'LocationConstraint': 'ap-southeast-2'}
    try:
        s3.create_bucket(Bucket='automating-aws-project',CreateBucketConfiguration=location)
    except:
        print("Error in creating bucket")

@click.group()
def cli():
    "Webtron deploys websites to s3 bucket"

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets available in the account"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.option('--bucket',help='List objects for specific bucket with given name')
def list_bucket_objects(bucket):
    "List objects in a given bucket"
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

if __name__=='__main__':
    cli()
