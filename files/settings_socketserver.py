SECRET_KEY = '&lyxkjm!oh2qar$6rc0oc=ks_eamdcuhg$b1p4#@f*-x*(rimz'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

APP_PROTOCOL = 'http',
ELB_PORT = 4443


APP_URL = ''

import boto
import boto.utils
import boto.cloudformation

conn = boto.cloudformation.connect_to_region(boto.utils.get_instance_identity()['document']['region'])
stacks = conn.describe_stacks(boto.utils.get_instance_userdata())
if len(stacks) == 1:
  stack = stacks[0]
else:
  print 'STACK NOT FOUND'

aws_data = {}
for output in stack.outputs:
  aws_data[output.key] = output.value

APP_URL = aws_data['AppELB']

APP_DOMAIN = APP_URL
