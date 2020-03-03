import json
import logging
import sys
import os
import watchtower, logging
import boto3
from io import BytesIO
from ftplib import FTP_TLS


loremipsum = """
5 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum
dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum.

Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris. Integer in mauris eu nibh euismod gravida. Duis ac tellus et risus vulputate vehicula. Donec lobortis risus a elit. Etiam tempor. Ut ullamcorper, ligula eu tempor congue, eros est euismod turpis, id tincidunt sapien risus a quam. Maecenas fermentum consequat mi. Donec fermentum. Pellentesque malesuada nulla a mi. Duis sapien sem, aliquet nec, commodo eget, consequat quis, neque. Aliquam faucibus, elit ut dictum aliquet, felis nisl adipiscing sapien, sed malesuada diam lacus eget erat. Cras mollis scelerisque nunc. Nullam arcu. Aliquam consequat. Curabitur augue lorem, dapibus quis, laoreet et, pretium ac, nisi. Aenean magna nisl, mollis quis, molestie eu, feugiat in, orci. In hac habitasse platea dictumst.
""" # from wikipedia


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

boto3_profile = os.getenv("BOTO3PROF")
session = boto3.Session(profile_name=boto3_profile)

cl_handler = watchtower.CloudWatchLogHandler(
    boto3_profile_name=boto3_profile,
    log_group="hmfLogs",
    stream_name="logger", )
logger.addHandler(cl_handler)


def read_ftp():
    with FTP_TLS(os.environ['host']) as ftps:
        ftps.login(os.environ['user'], os.environ['password'])
        ftps.prot_p()

        ftps.cwd(os.environ['dir'])
        filename = os.environ['finput']

        with BytesIO() as inpbin:
            ftps.retrbinary('RETR %s' % filename, inpbin.write)
            return inpbin.getvalue().decode('utf-8-sig')


def process(country):
    logger.warn(f"Hello from {country}")

    # read from FTP
    txt = read_ftp()
    logger.warn(f"Got {len(txt)} chars.")

    # write to S3
    filename = "lorenipsum.txt"

    s3 = session.client('s3')
    with BytesIO(loremipsum.encode()) as bio:
        s3.upload_fileobj( bio, os.environ["bucket"], filename )
    logger.warn(f"Wrote to S3.")

    cl_handler.flush()
    return f"OK {country}"


def lambda_handler(event, context):

    res = process(event['country'])

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }
