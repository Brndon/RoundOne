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
	rds_client = boto3.client('rds', region_name=region)
	instance_limit = rds_client.describe_account_attributes()
	
	print json.dumps(instance_limit, indent=4, separators=(',', ': '), default=json_serial)
	service_limit_name = instance_limit['AccountQuotas'][0]['AccountQuotaName']
	service_limit = instance_limit['AccountQuotas'][0]['Max']
	service_usage = instance_limit['AccountQuotas'][0]['Used']

	print "RDS DB Instance Limit: "
	print service_limit 
	print "RDS DB Instance Usage: "
	print service_usage
	return service_limit, service_usage;


#region = "us-east-1"
#print "Region: " + region
#get_limit(region)


