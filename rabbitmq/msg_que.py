#!/usr/bin/env python3
#coding=utf-8

import os
import pika
import json

"""
Msg queue wrapper of rabbitmq.
Provide easy to use APIs.
"""
class MsgQueue(object):
    def __init__(self):
        pass


    #private method start with '_'
    def _privateMethod(self):
        pass
    

    def _connectServer(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))

        self.channel = self.connection.channel()

    # public API
    def createQueue(self, que_name):
        """
        create queue with name que_name
        """
        self._connectServer()

        self.channel.queue_declare(queue=que_name)
        print("create queue: ", que_name)


    def putQue(self, msg, que_name):
        """
        Put msg to que_name
        """
        self._connectServer()

        self.channel.basic_publish(exchange='',
                      routing_key=que_name,
                      body=msg,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
        self.connection.close()
        print("Put msg to que_name: ", que_name)
    

    def getQue(self, que_name):
        """
        Non-block get method. If que is empty, just return None, else get one
        """
        self._connectServer()

        print("get msg from que_name : ", que_name)

        result = self.channel.basic_get(queue=que_name, no_ack=False)

        if result[0] is not None:
            print("message is: ", result[2].decode(encoding='utf-8'))
            self.channel.basic_ack(result[0].delivery_tag)

            print("over=========")
            return result[2].decode(encoding='utf-8')
        else:
            print("Channel Empty.")
            return
        
# eg
#crawler_response = {'image_dir':"/home/ubuntu/workspace/smail_spider/crawler_service/crawler_service/smailspider/images/full/fabiaoqingtest/201902211928"}
#msq = MsgQueue()
#msq.createQueue('CRAWLER_NOTIFY_QUE')
#msq.putQue(json.dumps(crawler_response), 'CRAWLER_NOTIFY_QUE')
#msq = MsgQueue()
#msq.createQueue('abc')
#msq.putQue('abc test====11111', 'abc')
# msq.putQue('abc test====22222', 'abc')
# msq.putQue('abc test====33333', 'abc')
# msq.putQue('abc test====44444', 'abc')
# msq.putQue('abc test====55555', 'abc')
# msq.putQue('abc test====66666', 'abc')
# msq.getQue('abc')
