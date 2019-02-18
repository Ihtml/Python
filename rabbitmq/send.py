#!/usr/bin/env python3
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World! from rabbitmq')
print(" [x]========== Sent Hello World!") 
connection.close() 