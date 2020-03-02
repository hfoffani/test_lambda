import json
import logging
import sys
import os
import watchtower, logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

boto3_profile = os.getenv("BOTO3PROF")

cl_handler = watchtower.CloudWatchLogHandler(
    boto3_profile_name=boto3_profile,
    log_group="hmfLogs",
    stream_name="logger", )
logger.addHandler(cl_handler)

def process(country):
    logger.warn(f"Hello from {country}")
    cl_handler.flush()
    return f"OK {country}"

def lambda_handler(event, context):

    res = process(event["country"])

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }
