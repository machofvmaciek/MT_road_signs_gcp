import tensorflow as tf
import json

PATH_MODEL = "/Users/machofv/Projects/road_signs_binary_classification/traffic_signs_cnn/models_training_2024-07-11 15:53:50.184526/model_at_epoch_6.h5"

model = tf.keras.models.load_model(PATH_MODEL)

# print(json.dumps(model.summary()))
var = json.dumps(model.summary())

print(var)
print("aaa")