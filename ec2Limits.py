#!/usr/bin/python

#determine the actual usage of EC2 vs the account instance limits

import boto3
import json
from datetime import datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def instance_limit(region):
	ec2_client = boto3.client('ec2', region_name=region)
	print "For Region: "+region
	get_limit(ec2_client)
	get_actual(ec2_client)

def get_limit(ec2_client):
	response = ec2_client.describe_account_attributes()

	attribute_list = response['AccountAttributes']
	for att in attribute_list:
		if att['AttributeName'] == 'max-instances':
			print "Max Instances: "
			max_instances = att['AttributeValues'][0]['AttributeValue']
			print max_instances
	return max_instances;

def get_actual(ec2_client):
	response_two = ec2_client.describe_instances()
	instance_list = response_two['Reservations']
	print "Number of instances: "
	num_of_instances = len(instance_list)
	print num_of_instances
	return num_of_instances;

	# print json.dumps(instance_list, indent=4, separators=(',', ': '), default=json_serial)

# instance_limit('us-east-1')

