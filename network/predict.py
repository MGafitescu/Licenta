import keras
import numpy as np
import json
import os
from PIL import Image

from keras.preprocessing import image

model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)),'model.h5'))
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'classes.json'))
label_map = json.load(f)

def predict(predicted_image):
    predicted_image = image.load_img(predicted_image, target_size = (150, 150))
    predicted_image = image.img_to_array(predicted_image)
    predicted_image = np.expand_dims(predicted_image, axis=0)
    result = model.predict_classes(predicted_image)
    result = label_map[str(result[0][0])]
    return result

print(predict("data/2.jpg"))