import functions_framework
from google.cloud import storage

BUCKET_NAME = 'bucket-road-signs'
FILE = 'test.txt'

@functions_framework.http
def read_file(request):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(FILE)
    blob.download_to_filename('/tmp/test.txt')

    with open("/tmp/test.txt", "r") as f:
      file_content = f.read()
    
    return file_content