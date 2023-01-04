import pika
import json
import os
#import from service 
from langdetect_service.ldetect import detect_lang_from_paragraphs


""" Interfacing with pika listener """


TOPIC_SUBSCRIBE= os.environ.get('TOPIC_SUBSCRIBE', 'langdetect')
TOPIC_PUBLISH = os.environ.get('TOPIC_PUBLISH', 'query')
MQ_HOST = os.environ.get('MQ_HOST', 'localhost')
PIKA_CREDENTIALS_USR = os.environ.get('PIKA_CREDENTIALS_USR', 'guest')
PIKA_CREDENTIALS_PWD = os.environ.get('PIKA_CREDENTIALS_PWD', 'guest')


def pika_worker():
    # connection to rabbitmq (message broker)
    url = f"{MQ_HOST}"
    print("[x] connecting to: " + url)

    credentials = pika.PlainCredentials(PIKA_CREDENTIALS_USR, PIKA_CREDENTIALS_PWD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=url, retry_delay=5,connection_attempts=10, credentials=credentials))

    channel = connection.channel()
    channel.exchange_declare(exchange=TOPIC_SUBSCRIBE, exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    channel.queue_bind(exchange=TOPIC_SUBSCRIBE, queue=queue_name)
    print(' [*] langdetect worker waiting for docs.')

    def business_logic(ch, method, properties, body):
        
        payload = json.loads(body)

        payload = detect_lang_from_paragraphs(payload)
       
        payload['status']='lang_detected'
        print(" [x] lang detected for doc_id: %r" % payload['es_id'])

        payload = json.dumps(payload)

        #send payload to query (save to es)
        channel.basic_publish(exchange=TOPIC_PUBLISH, routing_key="", body=payload)
        
        return payload
    #start listening 
    channel.basic_consume(queue=queue_name, on_message_callback=business_logic, auto_ack=True)
    channel.start_consuming()
    

if __name__ == "__main__":
    pika_worker()