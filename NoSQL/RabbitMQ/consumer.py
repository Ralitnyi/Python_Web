import json
import time

import connect
import pika
from bson.objectid import ObjectId
from models import Contact

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue="email_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    id_ = body.decode()
    contact = Contact.objects(id=ObjectId(id_)).first()
    contact.update(sent=True)
    print(contact.fullname)

    time.sleep(1)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="email_queue", on_message_callback=callback)


if __name__ == "__main__":
    channel.start_consuming()
