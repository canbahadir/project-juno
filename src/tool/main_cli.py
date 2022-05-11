"""A CLI tool to read queries from SQS queue and writes to DynamoDB.


Following paramaters can be given to configure during call.

AWS_REGION 
SQS_and_DB_ENDPOINT
USE_SSL
ACCESS_KEY
SECRET_KEY
SQS_QUEUE_NAME

using same port.

Parameters can be used partially or together.
When all parameters given command looks like this:

    AWS_REGION=ap-southeast-1 SQS_and_DB_ENDPOINT=http://localhost:4576 USE_SSL=0 ACCESS_KEY=mock SECRET_KEY=mock SQS_QUEUE_NAME=test-queue python main_cli.py <cmd>

Or it is possible to go with defaults and call
python main_cli.py <cmd>

Find the cmd list by typing python main_cli.py

"""

import fire
import os
import boto3
from pprint import pprint
from botocore.exceptions import ClientError


# Set global variables to work with  
global received_message, Verify, Region_name, Endpoint_url, Use_ssl, Aws_access_key_id, Aws_secret_access_key, QueueNameVar

def get_sqs_query(count, sqs_client=None):
    try:
        sqs_client = boto3.client(
            'sqs',
            region_name=Region_name,
            endpoint_url=Endpoint_url,
            use_ssl=Use_ssl,
            verify=Verify,
            aws_access_key_id=Aws_access_key_id,
            aws_secret_access_key=Aws_secret_access_key)
    except Exception as e:
        print(e)

    queue_url = sqs_client.get_queue_url(QueueName=QueueNameVar)['QueueUrl']

    try:
        # Receive message from SQS queue
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=count,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )
        
        received_message = [None] * len(response['Messages']);    

        for index in range(len(response['Messages'])):
            print(response['Messages'][index])

            received_message[index] = response['Messages'][index]
            receipt_handle = received_message[index]['ReceiptHandle']

            # Delete received message from queue
            sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )

    except Exception as e:
        print(e)

    return received_message


def write_db(msg, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=Region_name, aws_access_key_id=Aws_access_key_id,
                                   aws_secret_access_key=Aws_secret_access_key, endpoint_url=Endpoint_url)

    table = dynamodb.Table('sqsqueries')
    
    for index in range(len(msg)):
        response = table.put_item(
            Item={
                'message'    : msg[index]['Body'],
                'messageId'  : msg[index]['MessageId'],
                'src'        : 'sqsquery',
            }
        )
    return response


def process_query(count=1):
    
    """
    Takes latest message from 
    SQS queue adds it to DynamoDB table.
    """ 
   
    result = get_sqs_query(count)
    print("Sqs succeeded:")
    pprint(result, sort_dicts=False)
        
    writedb = write_db(result)
    print("writedb succeeded:")
    pprint(writedb, sort_dicts=False)
    return 'success'


def get_list(item1, item2, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=Region_name, aws_access_key_id=Aws_access_key_id,
                                   aws_secret_access_key=Aws_secret_access_key, endpoint_url=Endpoint_url)

    table = dynamodb.Table('sqsqueries')

    try:
        response = table.scan(ProjectionExpression=item1+","+item2)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']

def display_list():
    
    """
    Scans DynamoDB table and returns messages.
    """ 
    
    elementlist = get_list("message","messageId")
    if elementlist:
        print("Get elementlist succeeded:")
        pprint(elementlist, sort_dicts=False)


def clear_db(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=Region_name, aws_access_key_id=Aws_access_key_id,
                                   aws_secret_access_key=Aws_secret_access_key, endpoint_url=Endpoint_url)

    table = dynamodb.Table('sqsqueries')
    scan  = None
    ID    = "message"

    with table.batch_writer() as batch:
        count = 0
        while scan is None or 'LastEvaluatedKey' in scan:
            if scan is not None and 'LastEvaluatedKey' in scan:
                scan = table.scan(
                    ProjectionExpression=ID,
                    ExclusiveStartKey=scan['LastEvaluatedKey'],
                )
            else:
                scan = table.scan(ProjectionExpression=ID)

            for item in scan['Items']:
                if count % 5000 == 0:
                    print(count)
                batch.delete_item(Key={ID: item[ID]})
                count = count + 1
        return count


def clear_apply():
    cleardb = clear_db()
    print("cleardb succeeded:")
    pprint(cleardb)
    return 'success'


def main():

    fire.Fire({
        "consume"   : process_query,
        "show"      : display_list,
        "clear"     : clear_apply,
    })
    
    
if __name__ == "__main__":
    
    received_message = {}
    Use_ssl          = True
    Verify           = False

    # If given parse variables from CLI Command otherwise use defaults.
    if "AWS_REGION" in os.environ:
        Region_name = os.environ['AWS_REGION'] 
    else:
        Region_name = "ap-southeast-1"

    if "SQS_and_DB_ENDPOINT" in os.environ:
        Endpoint_url = os.environ['SQS_and_DB_ENDPOINT'] 
    else:
        Endpoint_url = "http://localhost:4576"

    if "USE_SSL" in os.environ:
        Use_ssl = os.environ['USE_SSL']  
    else:
        Use_ssl = True

    if "ACCESS_KEY" in os.environ:
        Aws_access_key_id = os.environ['ACCESS_KEY'] 
    else:
        Aws_access_key_id = "mock"
        
    if "SECRET_KEY" in os.environ:
        Aws_secret_access_key = os.environ['SECRET_KEY'] 
    else:
        Aws_secret_access_key = "mock"

    if "SQS_QUEUE_NAME" in os.environ:
        QueueNameVar = os.environ['SQS_QUEUE_NAME'] 
    else:
        QueueNameVar = "test-queue"

    main()