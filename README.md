# Introduction
An OpenAI RAG Implementation for psoriasis data, the data sourcing from Postgres.

#### Setup
1. Change directories at the command line
   to be inside the `rag-ai` folder

2. Run `docker-compose up postgres -d` to start the `postgres` image.

3. Run `pip install -r requirements.txt` to install python packages

#### How to develop locally

To connect to db:

    IDE

To run the code: 

   Run `python main.py`

To test code, run the following command:

    coverage run -m pytest -rP