import numpy as np
np.set_printoptions(formatter={'float': lambda x: f" {str(x)}".strip(), 'int': lambda x: f" {str(x)}".strip()})

# Creating numpy arrays
np_array = np.array([1, 2, 3])
print(f"Basic numpy array: {np_array}\n")

# Creating multi-dimension numpy arrays
np_array = np.array([[1, 2, 3], [1, 2, 3]])
print(f"Basic multi-dimension numpy array: \n{np_array}")
print(f"Shape: {np_array.shape}\n")

# Creating a numpy array with zero values
np_array = np.zeros((2, 2))
print(f"Basic multi-dimension numpy array with starting values: \n{np_array}")
print(f"Shape: {np_array.shape}\n")

# Creating a numpy array with randomized integer values
np_array = np.random.randint(10, size=(3, 3))
print(f"Basic multi-dimension numpy array with randomized values: \n{np_array}")
print(f"Shape: {np_array.shape}\n")

# Numpy array basic arithmetic
np_array = np.arange(10)
print(f"Single dimension array from 0 to 10: \n{np_array}")
print(f"Multiply all the array elements by 2: \n{np_array * 2}")
print(f"Divide all the array elements by 2: \n{np_array / 2}")
print(f"Power of 2 for all the array elements: \n{np_array ** 2}\n")
