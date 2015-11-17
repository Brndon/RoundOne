#!/usr/bin/python
# poll the AWS Trusted Advisor for resource limits and posts an SNS message to a topic with AZ and resource information
# Import the SDK
import boto3
import uuid
import json
import ec2Limits
import cloudformationLimits

# Instantiate a new client for AWS Support API and SNS.

support_client = boto3.client('support', region_name='us-east-1')
sns_client = boto3.client('sns', region_name='us-west-2')

# SNS ARN. This should be replaced with the name of the topic ARN that you want to publish
sns_arn = "arn:aws:sns:us-west-2:141820633316:AWS-Limits"
# Configure the regions that you want to poll in the list below
regions = ['us-east-1', 'us-west-1', 'us-west-2', 'ap-northeast-1']


def limitPoll():	
	# call trusted advisor for the limit checks
	response = support_client.describe_trusted_advisor_check_result(
		checkId='eW7HH0l7J9',
		language='en'
	)
	print "Contacting Trusted Advisor..."
	return response;

def publishSNS(warn_list, sns_client, sns_arn):
	# if warn_list has data, publish a message to the SNS_ARN
	if not warn_list:
		print "All systems green!"
	else:
		print "Publishing message to SNS topic..."
		sns_client.publish(
			TargetArn=sns_arn,
			Message=makeMessage(warn_list)
		)
	return;

def makeMessage(warn_list):
	#make the message that we send to the SNS topic
	sns_message = 'You have limits approaching their upper threshold. Please take action accordingly. \n'
	sns_message += '\n Region  -  Resource:'
	sns_message += '\n ------------------------'
	for rs in warn_list:
		sns_message += '\n' + rs 
	
	sns_message += '\n'
	sns_message += '\n EC2 Usage:'
	sns_message += '\n ------------------------'
	for rgn in regions:
		sns_message += "\n Region: " + rgn
		sns_message += "\n Instance Limit: "
		sns_message += ec2Limits.get_limit(rgn)
		sns_message += "\n Actual Usage: "
		sns_message += ec2Limits.get_actual(rgn)
		sns_message += "\n"

	sns_message += '\n'
	sns_message += '\n Cloudformation Usage:'
	sns_message += '\n -------------------------'
	for rgn in regions:
		sns_message += "\n Region: " + rgn
		sns_message += "\n Stack Limit: "
		sns_message += cloudformationLimits.get_limit(rgn)
		sns_message += "\n Actual Stacks: "
		sns_message += cloudformationLimits.get_actual(rgn)
		sns_message += "\n"


	print sns_message

	return sns_message;

def lambda_handler(event, context):

	response = limitPoll();

	# parse the json and find flagged resources that are in warning mode
	flag_list = response['result']['flaggedResources']
	warn_list=[]
	for fr in flag_list:
		if fr['metadata'][5] != "Green":
			warn_list.append(fr['metadata'][0]+' - '+fr['metadata'][2])
			print json.dumps(fr, indent=4, separators=(',', ': '))

	publishSNS(warn_list, sns_client, sns_arn);

	return;	
