import boto3
import time
# create a boto3 client
sqs = boto3.client('sqs')
sns = boto3.client('sns')

QUrl = 'https://sqs.us-east-1.amazonaws.com/956983767321/Lambda'
TopicArn = 'arn:aws:sns:us-east-1:956983767321:LazyShout'
while True:
	messages = sqs.receive_message(QueueUrl=QUrl ,MaxNumberOfMessages=10) # adjust MaxNumberOfMessages if needed
	if 'Messages' in messages: # when the queue is exhausted, the response dict contains no 'Messages' key
		for message in messages['Messages']:
			# 
			print("Receive sqs message : ")
			print(message['Body'])

			# Publishing to SNS
			print("Publishing to SNS")
			ms = message['Body']
			response = sns.publish(
				    TopicArn='arn:aws:sns:us-east-1:956983767321:LazyShout',
				    Message=ms,
				    Subject='DoTheseUrls'
				)
			# next, we delete the message from the queue so no one else will process it again
			sqs.delete_message(QueueUrl=QUrl,ReceiptHandle=message['ReceiptHandle'])
	else:
		print('Queue is now empty')
		time.sleep(3)