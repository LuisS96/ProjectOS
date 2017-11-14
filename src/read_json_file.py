import json
import os
import boto3


def readSQS():
    sqs = boto3.client("sqs")
    while True:
        MaxNumberOfMessages = 10
        response = sqs.receive_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/292274580527/cc406_team1')
        received = []
        for message in response['Messages']:
            received.append(message['ReceiptHandle'])
            print(message['Body'])
            return message
        WaitTimeSeconds = 20


def read_order(file):
    # Assures that the file exists and is located in the same directory
    if os.path.isfile(file) == False:
        print('The file "{0}" is not located in the same directory or does not exist.'.format(file))
        return
    else:
        # Creates file title into lowercase string and checks file extension if json
        if file.lower().endswith('.json'):
            # Trys to open the json file, an exception is raised if file can not be read properly
            try:
                with open(file) as jsfl:
                    data = json.load(jsfl)
                return data
            except:
                print("Make sure your json file is written correctly")
        else:
            print('File type is not .json and cannot be read')
