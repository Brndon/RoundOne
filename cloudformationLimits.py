#!/usr/bin/python

import boto3
import json
from datetime import datetime

def json_serial(obj):
	if isinstance(obj, datetime):
		serial = obj.isoformat()
		return serial
	raise TypeError ("Type not serializable")

def get_limit(region):
	cfn_client = boto3.client('cloudformation', region_name=region)
	stack_limit = cfn_client.describe_account_limits()
	
	print json.dumps(stack_limit, indent=4, separators=(',', ': '), default=json_serial)
	if  stack_limit['AccountLimits'][0]['Name'] == 'StackLimit':
		num_of_stacks = str(stack_limit['AccountLimits'][0]['Value'])
	print "Stack Limit: "
	print num_of_stacks
	return num_of_stacks;


def get_actual(region):
	cfn_client = boto3.client('cloudformation', region_name=region)
	stacks = cfn_client.describe_stacks()

	stack_list = stacks['Stacks']
	print "Actual Stacks: "
	num_of_stacks = str(len(stack_list))
	print num_of_stacks
	return num_of_stacks;

# print "Region: " + region
# get_limit(region)
# get_actual(region)


