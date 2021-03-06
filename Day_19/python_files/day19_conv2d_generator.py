# -*- coding: utf-8 -*-
"""day19_conv2d_generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KPj8BX-_mkZF4fqjf4JTVoGAoAL217f2
"""

import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Reshape, Conv2D, Conv2DTranspose
from tensorflow.keras import regularizers
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import IPython.display

"""### Define the model -"""

# define input data
X = np.asarray([[1, 2],
			 [3, 4]])
# show input data for context
print(X)
# reshape input data into one sample a sample with a channel
X = X.reshape((1, 2, 2, 1))

# define model
model = Sequential()
# define input shape, output enough activations for for 128 5x5 image
model.add(Dense(128 * 5 * 5, input_dim=100))
# reshape vector of activations into 128 feature maps with 5x5
model.add(Reshape((5, 5, 128)))
# double input from 128 5x5 to 1 10x10 feature map
model.add(Conv2DTranspose(1, (3,3), strides=(2,2), padding='same'))
# summarize model
model.summary()

"""### Generate a random image using CNN output -
This isn't part of the guide, but I was just curious to see how the generated image would look, so I used a random input value and scaled the image to 100x100 to visualize it.
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