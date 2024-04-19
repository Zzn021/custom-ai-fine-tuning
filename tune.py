import os
import sys

from openai import OpenAI
from dotenv import load_dotenv

from data import validate

load_dotenv()
API_KEY = os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)

# Return a list of uploaded files
def file_list():
    return client.files.list().to_dict()

# Upload a file and return the file id
def tuning_upload_file(file_path: str) -> str:
    # Check if the file is already uploaded
    file_name = os.path.basename(file_path)
    
    files = file_list()
    for file in files['data']:
        if file['filename'] == file_name:
            id = file['id']
            print(f'{file_name} already uploaded with id: {id}')
            
            return id
    
    if validate(file_path):
        print(f'uploading file: {file_name}')
        id = client.files.create(
            file=open(file_path, "rb"),
            purpose="fine-tune"
        ).id
        
        return id

# Deletes an uploaded file
def file_delete(file_id: str) -> bool:
    return client.files.delete(file_id).deleted

# Create a fine-tuning job
def tuning_create(training_file: str, model: str):
    id = client.fine_tuning.jobs.create(
        training_file=training_file,
        model=model
    ).id
    
    return id

# Return a list of tunings
def tuning_list():
    return client.fine_tuning.jobs.list().to_dict()

# Retrieves a tuning job
def tuning_retrieve(job_id: str):
    return client.fine_tuning.jobs.retrieve(job_id).to_dict()

# Cancle a tuning job
def tuning_cancle(job_id: str) -> bool:
    status = client.fine_tuning.jobs.cancel(job_id).status
    if status == "cancelled":
        return True
    
    return False

# Usage python3 tune.py FILE_PATH
if __name__ == "__main__":
    file_path = sys.argv[1]
    # id = tuning_upload_file(file_path)
    # print(id)
    # id = tuning_create(id, "gpt-3.5-turbo")
    # print(id)
    tuning_cancle("ftjob-mtrNrg58NxXSfvo1QoI6snou")