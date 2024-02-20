import pika
import json
import os
import argparse
from archive_utils import dowload_identifier_data

rabbitmq_credentials = json.load(open("../config/rabbitmq_credentials.json"))

def get_url_from_queue(queue_ip, username, password, queue_name):
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=queue_ip, credentials=credentials))
    channel = connection.channel()

    method, header_frame, body = channel.basic_get(queue=queue_name)

    if method is None:
        print("No more messages in queue")
        connection.close()
        return None
    
    channel.basic_ack(method.delivery_tag)
    message = json.loads(body)
    identifier, language = (
        message["identifier"],
        message["language"],
    )

    connection.close()

    return identifier,language

parser = argparse.ArgumentParser()
parser.add_argument("--pdf_only",type=bool,default=True,help="To download only associated PDF Files")

if __name__=="__main__":
    data_path = "../../data/"
    args = parser.parse_args()

    while True:
        queueStatus = get_url_from_queue(queue_ip=rabbitmq_credentials["queue_ip"],username=rabbitmq_credentials["username"],password=rabbitmq_credentials["password"],queue_name=rabbitmq_credentials["queue_name"])
        if queueStatus!=None:
            identifier = queueStatus[0]
            language = queueStatus[1]
            destination_path = f"{data_path}/{language}/{identifier}"
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            print(f"Downloading Data for {language}/{identifier}")
            dowload_identifier_data(identifier=identifier,language=language,destination_folder=data_path,pdf_only=args.pdf_only)
        else:
            break
    print("Data for Identifiers from Queue have been downloaded.")