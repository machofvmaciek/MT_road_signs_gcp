import json
import functions_framework

import tensorflow as tf
import numpy as np

from google.cloud import storage

# Replace with your bucket and file names
BUCKET_NAME = 'bucket-road-signs'
FILE_MODEL = 'cnn_v8_ep_18_tensor_16.h5'

CLASSES = ['Speed limit (20km/h)', 'Speed limit (30km/h)', 'Speed limit (50km/h)', 'Speed limit (60km/h)', 'Speed limit (70km/h)', 'Speed limit (80km/h)', 'End of speed limit (80km/h)', 'Speed limit (100km/h)', 'Speed limit (120km/h)', 'No passing', 'No passing for vehicles over 3.5 metric tons', 'Right-of-way at the next intersection', 'Priority road', 'Yield', 'Stop', 'No vehicles', 'Vehicles over 3.5 metric tons prohibited', 'No entry', 'General caution', 'Dangerous curve to the left', 'Dangerous curve to the right', 'Double curve', 'Bumpy road', 'Slippery road', 'Road narrows on the right', 'Road work', 'Traffic signals', 'Pedestrians', 'Children crossing', 'Bicycles crossing', 'Beware of ice/snow', 'Wild animals crossing', 'End of all speed and passing limits', 'Turn right ahead', 'Turn left ahead', 'Ahead only', 'Go straight or right', 'Go straight or left', 'Keep right', 'Keep left', 'Roundabout mandatory', 'End of no passing', 'End of no passing by vehicles over 3.5 metric tons'] 

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
        # prediction = np.argmax(probabilities, axis=1)
        prediction = CLASSES[np.argmax(probabilities, axis=1)[0]]

        return json.dumps({"prediction": prediction})
