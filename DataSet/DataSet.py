import keras.utils as image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
from sklearn.cluster import KMeans
import shutil, glob, os.path

# Path to the folder with images
imdir = "Start_buildings"
targetdir = "Clustered_buildings/"
number_clusters = 5

# Load the VGG16 model
model = VGG16(weights='imagenet', include_top=False)

# Load images and extract features
filelist = glob.glob(os.path.join(imdir, '*.jpg'))
filelist.sort()
featurelist = []
for i, imagepath in enumerate(filelist):
    print("Status: %s / %s" %(i, len(filelist)), end="\r")
    img = image.load_img(imagepath, target_size=(224, 224))  # Required size for VGG16
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = np.array(model.predict(img_data))
    featurelist.append(features.flatten())

# Clustering using k-means
kmeans = KMeans(n_clusters=number_clusters, init='k-means++', n_init=10, random_state=0).fit(np.array(featurelist))

# Create folders for each cluster and copy images
try:
    os.makedirs(targetdir)
except OSError:
    pass

# Copy images into cluster folders
print("\n")
for i, m in enumerate(kmeans.labels_):
    print("Copy: %s / %s" %(i, len(kmeans.labels_)), end="\r")
    shutil.copy(filelist[i], targetdir + str(m) + "_" + str(i) + ".jpg")
