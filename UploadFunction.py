import json
import boto3
import mimetypes
import base64

# Initialize the S3 client
s3_client = boto3.client('s3')

# Replace with your bucket name
BUCKET_NAME = 'joy-file-sharing-bucket'  # Ensure this is set to your actual bucket name

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        print("Received event: ", json.dumps(event))

        if 'body' in event:  # Check if the body is in the event
            body = json.loads(event['body'])
            filename = body['filename']
            file_content = body['file']  # This should be base64 encoded
            
            # Decode the base64 file content
            file_data = base64.b64decode(file_content)

            # Upload the file to S3
            s3_client.put_object(Bucket=BUCKET_NAME, Key=filename, Body=file_data, ContentType=mimetypes.guess_type(filename)[0])

            return {
                'statusCode': 200,
                'body': json.dumps({"message": "File uploaded successfully", "fileKey": filename})
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "'body' is missing in the event"})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }

def get_presigned_url(filename):
    # Generate a pre-signed URL for S3
    try:
        s3 = boto3.client('s3')

        # Generate a pre-signed URL
        presigned_url = s3.generate_presigned_url('put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600)  # URL valid for 1 hour

        return {
            'statusCode': 200,
            'uploadUrl': presigned_url,
            'fileKey': filename
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
