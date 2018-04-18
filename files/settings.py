# Environment name - staging, production, testing
ENVIRONMENT = 'staging'

import os

# Used only by dpkg
IS_PROXY = False

##### Get data from AWS Cloudformation ####
DB_HOST = ''
DB_NAME = ''
DB_USER = ''
DB_PWD = ''
APP_URL = ''
PREVIEWS_URL = ''
RIDE_URL = ''
EFS_DNS = ''
S3_REGION = ''
BUCKET_SNAPSHOTS = ''
BUCKET_MP_ASSETS = ''
BUCKET_ASSESTS = ''


import boto
import boto.utils
import boto.cloudformation
import json


aws_region = boto.utils.get_instance_identity()['document']['region']
conn = boto.cloudformation.connect_to_region(aws_region)
stacks = conn.describe_stacks(boto.utils.get_instance_userdata())
if len(stacks) == 1:
  stack = stacks[0]
else:
  print 'STACK NOT FOUND'

aws_data = {}
for output in stack.outputs:
  aws_data[output.key] = output.value

DB_HOST = aws_data['RDSPostgres']
DB_NAME = aws_data['DatabaseName']
DB_USER = aws_data['DatabaseUsername']
DB_PWD = aws_data['DatabaseUserPassword']
APP_URL = aws_data['AppELB']
PREVIEWS_URL = aws_data['PreviewsELB']
RIDE_URL = aws_data['RideProxyELB']
EFS_DNS = aws_data['efsdns']
S3_REGION = 's3-' + aws_region + '.amazonaws.com'
BUCKET_SNAPSHOTS = aws_data['BucketNameRideSnapshots']
BUCKET_MP_ASSETS = aws_data['BucketNameMarketplaceAssets']
BUCKET_ASSESTS = aws_data['BucketNameStaticAssets']
###########################################
#print S3_REGION

CELERY_BROKER_URL = 'amqp://rbrain:ovNadyojnopArm2@localhost:5672/rbrain'

CUSTOM_DJOSER_SETTINGS = {
     'PROTOCOL': 'http',
     'DOMAIN': APP_URL
}

NOTEBOOK_PREVIEW_DOMAIN = PREVIEWS_URL

SECRET_KEY = '&lyxkjm!oh2qar$6rc0oc=ks_eamdcuhg$b1p4#@f*-x*(rimz'

STATIC_URL = 'http://' + APP_URL + '/static/'
STATIC_ROOT = '/home/rbrain/static/'

MEDIA_ROOT = '/'
PRIVATE_STATIC_ROOT = STATIC_ROOT

DEBUG = False
ALLOWED_HOSTS =  [ "*"]

# We use IAM profile for S3 access
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PWD,
        'HOST': DB_HOST,
        'PORT': '5432',
    }
}

AWS_BUCKETS = {
    'ride_snapshots': BUCKET_SNAPSHOTS,
    'marketplace': BUCKET_MP_ASSETS,
}

DEFAULT_FROM_EMAIL = 'no-reply@staging-r-brain.io'
LANDINGPAGE_EMAIL_RECEIVERS = ['landingpage@mailinator.com', ]

INVITATION_NOTIFY = ['invitation@mailinator.com', ]

RIDE_DOMAIN = RIDE_URL

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'

DOCKER_ADDR = 'tcp://localhost:4000'
DOCKER_CREATE_TIMEOUT = 60
DOCKER_DEV_JUPYTER_IMAGES = []

MOUNT_POINTS = {
    'ride': '/mnt/ride',
    'inventory': '/mnt/ride/inventory',
    'marketplace': '/mnt/ride/marketplace',
}

REGISTRATION_IS_ENABLED = True
