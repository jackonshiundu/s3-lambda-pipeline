import json
import urllib.parse
import boto3

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    """
    Triggered by S3 events (e.g. object uploaded).
    Logs bucket name, file key, size, and content type.
    """
    print("Received S3 event:", json.dumps(event, indent=2))

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key    = urllib.parse.unquote_plus(
                     record["s3"]["object"]["key"],
                     encoding="utf-8"
                 )
        size   = record["s3"]["object"].get("size", "unknown")

        print(f"📦 Bucket : {bucket}")
        print(f"📄 File   : {key}")
        print(f"📏 Size   : {size} bytes")

        # Fetch object metadata from S3
        try:
            response = s3_client.head_object(Bucket=bucket, Key=key)
            content_type = response.get("ContentType", "unknown")
            print(f"🔍 Content-Type: {content_type}")
        except Exception as e:
            print(f"⚠️  Could not fetch metadata: {e}")

    return {
        "statusCode": 200,
        "body": json.dumps("S3 event processed successfully")
    }