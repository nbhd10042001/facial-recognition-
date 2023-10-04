# import the necessary packages
from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2
import os

name_p = input("Nhap ten:") 
os.mkdir('.\dataset\{}'.format(name_p))

cam = cv2.VideoCapture(0)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 500, 300)
print("Press space to take a photo")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "dataset/"+ name_p +"/image_{}{}.jpg".format(name_p,img_counter)   #sua doi ten
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()

# **********************************************************************************************************************************
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
	boxes = face_recognition.face_locations(rgb, model="hog")

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