import os
import urllib.parse
import boto3
import json

def start_label_detection(bucket, key):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
                    Video={
                        'S3Object': {
                            'Bucket':bucket,
                            'Name':key
                            }
                    },
                    NotificationChannel={
                        'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
                        'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
                    }
                )
    print(response)
    return

def get_video_labels(job_id):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.get_label_detection(JobId=job_id)

    next_token = response.get('NextToken', None)

    while next_token:
        next_page = rekognition_client.get_label_detection(
                                                JobId=job_id,
                                                NextToken=next_token
                                            )
        response['Labels'].extend(next_page['Labels'])
        next_token = next_page.get('NextToken', None)

    return response


def put_labels_in_db(data, video_name, video_bucket):
    pass


def start_processing_video(event, context):
    for record in event.get('Records'):
        start_label_detection(
            record.get('s3').get('bucket').get('name'),
            urllib.parse.unquote_plus(record.get('s3').get('object').get('key'))
        )

    return

def handle_label_detection(event, context):
    for record in event.get('Records'):
        message = record.get('Sns').get('Message')
        message_json = json.loads(message)
        job_id = message_json['JobId']
        s3_bucket = message_json['Video']['S3Bucket']
        s3_object = message_json['Video']['S3ObjectName']

        response = get_video_labels(job_id)
        print("Response from rekognition job is "+str(response))
        put_labels_in_db(response, s3_object, s3_bucket)

    return
