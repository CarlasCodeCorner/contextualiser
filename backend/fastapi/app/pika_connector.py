import os
import pika

MQ_HOST = os.environ.get('MQ_HOST', 'localhost')
PIKA_CREDENTIALS_USR = os.environ.get('PIKA_CREDENTIALS_USR', 'guest')
PIKA_CREDENTIALS_PWD = os.environ.get('PIKA_CREDENTIALS_PWD', 'guest')

def setup_pika(TOPIC):
   
    	
    url = f"{MQ_HOST}"

    print("[x] connecting to: " + url)
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=url, retry_delay=5,connection_attempts=10, credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=TOPIC, exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=TOPIC, queue=queue_name)
    print(' [*] central-api connected to rabbitmq.')

    return channel, connection