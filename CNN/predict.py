import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model(
    "laptop_classifier.keras"
)

class_names = [
    "Laptop",
    "Non Laptop"
]

img = tf.keras.utils.load_img(
    "testi.jpg",
    target_size=(128,128)
)

img_array = tf.keras.utils.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = img_array / 255.0

prediction = model.predict(img_array)

print(
    "Prediksi:",
    class_names[np.argmax(prediction)]
)