#!/usr/bin/python

import sys

if len(sys.argv) < 2:
  print 'Missing argument'
  sys.exit(0)

import boto
import boto.utils
import boto.cloudformation

aws_region = boto.utils.get_instance_identity()['document']['region']
conn = boto.cloudformation.connect_to_region(aws_region)
stacks = conn.describe_stacks(boto.utils.get_instance_userdata())
if len(stacks) == 1:
  stack = stacks[0]
else:
  print 'STACK NOT FOUND'

aws_data = {}
aws_data['availabilityZone'] = boto.utils.get_instance_identity()['document']['availabilityZone']
aws_data['region'] = aws_region

for output in stack.outputs:
  aws_data[output.key] = output.value

aws_data['EFS'] = aws_data['availabilityZone'] + '.' + aws_data['efsdns']

print aws_data[sys.argv[1]]
