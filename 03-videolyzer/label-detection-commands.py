import boto3
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')
bucket = s3.create_bucket(Bucket='laljitvideoanalyzer',
                CreateBucketConfiguration={'LocationConstraint':session.region_name})

from pathlib import Path
pathname = '~/Downloads/production ID_4426380.mp4'
path = Path(pathname).expanduser().resolve()
print(path)
bucket.upload_file(str(path), str(path.name))
rekognition_client = session.client('rekognition')
response = rekognition_client.start_label_detection(
                Video={'S3Object': {'Bucket':bucket.name,'Name':path.name}})

response
job_id = response.get('JobId')
result = rekognition_client.get_label_detection(JobId=job_id)
result.keys()
result['JobStatus']
result.get('VideoMetadata')
len(result['Labels'])
