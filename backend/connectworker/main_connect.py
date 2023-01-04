import pika
import json
import os
# which handles all different types of info which needs to be saved in either mongo db or es
from query_services.saving_payload_class import save_p


TOPIC_SUBSCRIBE= os.environ.get('TOPIC', 'connect')
MQ_HOST = os.environ.get('MQ_HOST', 'localhost')
PIKA_CREDENTIALS_USR = os.environ.get('PIKA_CREDENTIALS_USR', 'guest')
PIKA_CREDENTIALS_PWD = os.environ.get('PIKA_CREDENTIALS_PWD', 'guest')
CREDENTIALS = pika.PlainCredentials(PIKA_CREDENTIALS_USR, PIKA_CREDENTIALS_PWD)

def pika_worker():


    url = f"{MQ_HOST}"
    print("[x] query worker connecting to: " + url)

    credentials = pika.PlainCredentials(PIKA_CREDENTIALS_USR, PIKA_CREDENTIALS_PWD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=url, retry_delay=5,connection_attempts=10, credentials=credentials))

    channel = connection.channel()
    channel.exchange_declare(exchange=TOPIC_SUBSCRIBE, exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=TOPIC_SUBSCRIBE, queue=queue_name)
    print(' [*] connect worker waiting for text')

    def save(ch, method, properties, body):
       
        payload = json.loads(body)
        save_p(payload=payload, channel=channel)
        
    
    channel.basic_consume(queue=queue_name, on_message_callback=save, auto_ack=True)

    channel.start_consuming()
    

if __name__ == "__main__":
    
    pika_worker()
   