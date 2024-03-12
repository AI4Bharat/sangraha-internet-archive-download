# Sangraha Internet Archive Data Download

Code Repository for Scripts and Utils for downloading and curating Indic Data from archive.org Files.

## Setup

Create a virtual environment and install required python dependencies provided in the requirements.txt file.

## Single Machine Download from Internet Archive

In the pipeline folder, We have [Single Machine Download Python Script](/pipeline/single_machine_download.py) for downloading archive data into your machine.
The script requires a list of language names i.e. Dogri, Tamil, Hindi, etc. followed by optional arguments such as pdf_only and id_only download options.

## Distributed Machine Download from Internet Archive

This setup was utilized so that we can download data onto machines with more storage and parallelize downloads.

Note : You will have to setup RabbitMQ in your server and client machines and configure the [Credentials](/config/rabbitmq_credentials.json) file accordingly.

In the pipeline folder, We have two files :

- [Multiple Machine Server](/pipeline/multiple_machine_download_server.py) for queueing the identifiers from the identifiers.csv file downloaded from the previous section using id_only parameter.

- [Multiple Machine Client](/pipeline/multiple_machine_download_client.py) for pulling identifiers from server host and downloading data onto client machine.
