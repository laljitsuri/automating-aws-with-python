import urllib.parse
import boto3

def start_label_detection(bucket, key):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
                    Video={
                        'S3Object': {
                            'Bucket':bucket,
                            'Name':key
                            }
                        }
                    )
    print(response)
    return


def start_processing_video(event, context):
    for record in event.get('Records'):
        start_label_detection(
            record.get('s3').get('bucket').get('name'),
            urllib.parse.unquote_plus(record.get('s3').get('object').get('key'))
        )

    return
