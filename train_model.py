#! /usr/bin/python

# import the necessary packages
from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2
import os

name_p = input("Nhap ten:") 
# our images are located in the dataset folder
print("[INFO] start processing faces...")
imagePaths = list(paths.list_images("dataset\{}".format(name_p)))

print(imagePaths)

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):   #cho i la key, imagePath la value trong enumerate imagePaths(gom key va value), value o day la duong dan path
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(imagePath,        #i + 1
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]  #name = ten thu muc chua anh
	#os.path.sep la lay dau "\", split la tach tung phan tu trong chuoi path ngan cach boi dau "\", name = ten phan tu -2

	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model="hog")

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings_{}".format(name_p): knownEncodings, "names_{}".format(name_p): knownNames}
f = open("encoding_{}.pickle".format(name_p), "wb")
f.write(pickle.dumps(data))
f.close()
