
import json
import functions_framework

import tensorflow as tf
import numpy as np

from google.cloud import storage

# Replace with your bucket and file names
BUCKET_NAME = 'bucket-road-signs'
FILE_MODEL = 'cnn_v8_ep_18_tensor_16.h5'
model = None

@functions_framework.http
def predict(request):
    global model

    # Load model on first request or if not already loaded
    if model is None:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(FILE_MODEL)
        blob.download_to_filename('/tmp/model.h5')
        model = tf.keras.models.load_model('/tmp/model.h5')
    
    # response = json.dumps(model.summary())
    # return response
    
    if request.method == "POST":
        try:
            request_json = request.get_json()

            # Extract the ndarray data from the JSON
            json_string = request_json['ndarray_data']  

            # Convert JSON string to list
            data_list = json.loads(json_string)

            # Convert list to ndarray
            img = np.array(data_list)
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            return f'Error decoding or converting ndarray: {e}', 400
        
        probabilities = model.predict(img)
        prediction = np.argmax(probabilities, axis=1)

        return json.dumps({"prediction": prediction.tolist()})
    
    # # Get input data from the request (JSON or query parameters)
    # input_data = request.get_json()
    # # Preprocess input_data as needed

    # # Make predictions
    # predictions = model.predict(input_data)

    # # Postprocess predictions as needed (e.g., convert to desired format)

    # # Return the predictions in the response
    # return {'predictions': predictions.tolist()}  # Convert to list for JSON
