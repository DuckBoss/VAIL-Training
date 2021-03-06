# -*- coding: utf-8 -*-
"""day19_upsampling2d_generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qWjMT7tBQUXI0xSZ3RX9PDlIN_Szw72L
"""

import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, UpSampling2D, Reshape, Conv2D
from tensorflow.keras import regularizers
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import IPython.display

"""### Define the model -"""

# define model
model = Sequential()
# define input shape, output enough activations for 128 5x5 image
model.add(Dense(128 * 5 * 5, input_dim=100))
# reshape vector of activations into 128 feature maps with 5x5
model.add(Reshape((5, 5, 128)))
# double input from 128 5x5 to 1 10x10 feature map
model.add(UpSampling2D())
# fill in detail in the upsampled feature maps and output a single image
model.add(Conv2D(1, (3,3), padding='same'))
model.summary()

"""### Generate a random image using CNN output -
This isn't part of the guide, but I was just curious to see how the generated image would look, so I used a random input value and scaled the image to visualize it.
"""

random_data = np.random.rand(1, 100)
print(f"Input data:\n{random_data}")

output = model.predict(random_data)
print(f"Output data:\n{output.reshape(1, 100)}")
reshaped_output = output.reshape(1, 10, 10)

generated_image = Image.fromarray(reshaped_output, mode='RGB')
generated_image = generated_image.resize((100, 100))
print(f"\nGenerated Image: {reshaped_output.shape} => 100x100")
IPython.display.display(generated_image)