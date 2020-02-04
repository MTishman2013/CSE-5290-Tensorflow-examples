from keras.datasets import mnist

# This data set is a 60,000 matrices of 28x28.
# Each matrix is a grayscale image, with coefficient between 0 and 255

# Train_images[i] is the image of the number
# Train_images[i][x][y] is the pixels of the image
# In general, the first axis (axis 0, because indexing starts at 0)
#   in all data tensors you’ll come across in deep learning will be the samples axis
#   (sometimes called the samples dimension).
# In the MNIST example, samples are images of digits.
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

print("Rank of tensor set: ", train_images.ndim)
print("Shape of tensor set: ", train_images.shape)
print("DataType of tensor set: ", train_images.dtype)

# Output:
# Rank of tensor set:  3                 <-- 3D tensor
# Shape of tensor set:  (60000, 28, 28)  <-- 60,000 Matrices of 28x28
# DataType of tensor set:  uint8         <-- 8-bit integers

# tensor-slicing
digit = train_images[0]

import matplotlib.pyplot as plt
plt.imshow(digit, cmap=plt.cm.binary)
plt.show()

# tensor slicing to select 14x14 pixels in the bottom right corner of all images
cornerSlice = train_images[:, 14:, 14:]
print("14 x 14 Slice ===> train_images[:, 14:, 14:]  = ", cornerSlice.shape)
# Output
# 14 x 14 Slice ===> train_images[:, 14:, 14:]  =  (60000, 14, 14)

plt.imshow(cornerSlice[0], cmap=plt.cm.binary)
plt.show()


# Smaller subset batch
batch = train_images[:128]
next_batch = train_images[128:256]
print("First Batch: ", batch.shape)
print("Second Batch: ", next_batch.shape)
