import logging
from concurrent.futures.thread import ThreadPoolExecutor

import boto3
import qiniu

MAX_READ_SIZE = 64 * 1024

QINIU_ACCESS_KEY = 'Bkmr1dcogeHX4Q7I4tmppGLWXAoz6dQk5wa9CrbV'
QINIU_SECRET_KEY = 'yp4NzDIhEalZxQrI6TDKiMXdfykQRTkw775knKTX'
QINIU_BUCKET_NAME = 'tangzufang'

AUTH = qiniu.Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)

# AWS3_REGION = 'region_name'
# AWS3_AK = 'access_key'
# AWS3_SK = 'secret_key'
# AWS3_BUCKET = 'bucket_name'
#
# S3 = boto3.client('s3', region_name=AWS3_REGION,
#                   aws_access_key_id=AWS3_AK, aws_secret_access_key=AWS3_SK)

MAX_THREAD_WORKERS = 16
EXECUTOR = ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS)