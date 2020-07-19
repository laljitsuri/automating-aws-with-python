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

# S3 event and getting bucket and key from events
event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'ap-southeast-2', 'eventTime': '2020-07-19T08:56:54.484Z', 'eventName': 'ObjectCreated:CompleteMultipartUpload', 'userIdentity': {'principalId': 'AWS:AIDAZUTP5XJNK4C66OIA3'}, 'requestParameters': {'sourceIPAddress': '141.168.87.232'}, 'responseElements': {'x-amz-request-id': 'B39BE0118F2FD439', 'x-amz-id-2': 'CzerFt0E8qlLny/vSgqUX7FOx8xsTaFf2jonBcIgL9UUD3/PTjU6GBvrgkKvhogUzCRGtpCwW2/YRDegscZUiAPHEIzDDcPa'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '23058e34-dfb2-44cd-80de-ab741e229848', 'bucket': {'name': 'laljitvideoanalyzer', 'ownerIdentity': {'principalId': 'A3SNFGB7D2C7ZG'}, 'arn': 'arn:aws:s3:::laljitvideoanalyzer'}, 'object': {'key': 'production_ID_4426380.mp4', 'size': 20649866, 'eTag': 'a22ad94c309236ed3d4d7df4925ff3c1-3', 'sequencer': '005F140ACBC58598B5'}}}]}
event
rec = event.get('Records')[0]
rec.get('s3').get('bucket').get('name')
rec.get('s3').get('object').get('key')
import urllib.parse
urllib.parse.unquote_plus(rec.get('s3').get('object').get('key'))
