# Sangraha Data Download

Code Repository for Scripts and Utils for downloading and curating Indic Data from Web Crawls and archive.org Files.

## Setup

Create a virtual environment and install required python dependencies provided in the requirements.txt file.

## Single Machine Download from Internet Archive

In the pipeline folder, We have [Single Machine Download Python Script](/pipeline/single_machine_download.py) for downloading archive data into your machine.
The script requires a list of language names i.e. Dogri, Tamil, Hindi, etc. followed by optional arguments such as pdf_only and id_only download options.
