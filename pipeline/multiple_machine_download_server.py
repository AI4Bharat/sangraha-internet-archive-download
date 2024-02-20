import pika
import pandas as pd
import json
from tqdm import tqdm 

rabbitmq_credentials = json.load(open("../config/rabbitmq_credentials.json"))

def send_to_queue(queue_ip, username, password, queue_name, message):


    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=queue_ip,
            credentials=credentials
            )
        )
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )

    connection.close()

if __name__=="__main__":
    
    data_path = "../../data/"

    queue_name = rabbitmq_credentials["queue_name"]

    identifierDf = pd.read_csv(f"{data_path}/identifiers.csv")
    
    print("Queueing Identifiers to RabbitMQ Server")
    for idx,row in tqdm(identifierDf.iterrows(),total=len(identifierDf)):
        jsonObj = json.dumps({
            "identifier":row["identifier"],
            "language":row["language"]
        })
        send_to_queue(queue_ip=rabbitmq_credentials["queue_ip"],username=rabbitmq_credentials["username"],password=rabbitmq_credentials["password"],queue_name=queue_name,message=str(jsonObj))
    print("Identifiers Queued to Server")