from pathlib import Path

import boto3
import click

@click.option('--profile', default=None, help="Use given profile name")
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucketname')
@click.command()
def upload_file(profile, pathname, bucketname):
    """Upload file to S3 bucketname"""

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    else:
        session_cfg['profile_name'] = 'pythonAutomation'

    session = boto3.Session(**session_cfg)
    s3 = session.resource('s3')

    bucket = s3.Bucket(bucketname)

    path = Path(pathname).expanduser().resolve()
    bucket.upload_file(str(path), str(path.name))


if __name__ == '__main__':
    upload_file()
