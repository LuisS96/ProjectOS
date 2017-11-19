__author__ = 'lfsc96'

import json
import boto3
from queue import *
from Threads import *
from Charts import *


def assign_queues(queues, answersList):
    asadaQueue = Queue()  # Suborders of meat asada
    adobadaQueue = Queue()  # Suborders of meat adobada
    othersQueue = Queue()  # Suborders of meat suadero, tripa, cabeza, and lengua
    for answer in answersList:
        for suborder in answer.order.subordersList:  # Each suborder will be assigned to its respective queue according to the type of meat
            if suborder.meat == 'Asada':
                asadaQueue.put(suborder)
            elif suborder.meat == 'Adobada':
                adobadaQueue.put(suborder)
            else:
                othersQueue.put(suborder)
    queues.append(asadaQueue)
    queues.append(adobadaQueue)
    queues.append(othersQueue)


def classify_data(data, answersList):
    # Assignment of data for each order and suborder
    order = Order(data['request_id'], data['datetime'])
    for suborder in data['orden']:
        order.totalSubs += 1
        taco = Suborder(suborder['part_id'], suborder['type'], suborder['meat'], suborder['quantity'],
                        suborder['ingredients'])
        order.subordersList.append(taco)
    answer = Answer(order)
    answersList.append(answer)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
            # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def readSQS():
    sqs = boto3.client('sqs')
    received = []
    while True:
        response = sqs.receive_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/292274580527/cc406_team6', MaxNumberOfMessages=10, WaitTimeSeconds=20)
        answersList = []
        queues = []
        for message in response['Messages']:
            received.append(message['ReceiptHandle'])
            data = json.loads(message['Body'])
            print(data)
            classify_data(data, answersList)
        assign_queues(queues, answersList)
        threads(queues, answersList)
        for answer in answersList:
            print(json.dumps(answer.__dict__(), indent=4))

readSQS()