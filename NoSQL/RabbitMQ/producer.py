import connect
import pika
from faker import Faker
from models import Contact

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange="task_mock", exchange_type="direct")
channel.queue_declare(queue="email_queue", durable=True)
channel.queue_bind(exchange="task_mock", queue="email_queue")


def main():
    fake = Faker()
    for i in range(10):
        contact = Contact(fullname=fake.name(), email=fake.email()).save()

        channel.basic_publish(
            exchange="task_mock",
            routing_key="email_queue",
            body=str(contact.id),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print(" [x] Sent %r" % str(contact.id))
    connection.close()


if __name__ == "__main__":
    main()
