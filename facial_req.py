# import the necessary packages
from cv2 import imwrite
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
from time import sleep
import os, os.path
import smtplib         #lib for send mail
import imghdr
from email.message import EmailMessage
import config
import getpass

#khai bao cac bien
face_error = 0
accept = 0
warning_dg = 0
ss1 = ss1 = 0
login = 1

#Determine faces from encodings.pickle file model created from train_model.py
# encodingsP = "encodings.pickle"
encodingsP = "encoding_Duc.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("Loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())  #luu du lieu train vao bien data
print(data)

#tinh so luong anh trong thu muc
listname =  os.listdir(".\dataset")
sizelist = []

for a in range(0,len(listname)):
	path = ".\dataset\{}".format(listname[a])
	sizelist.append(len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]))
#print(sizelist)


#create variable gmail
Sender_Email = config.email_add
Reciever_Email = config.email_add

#gui anh dinh kem qua gmail
def send_mail(Subj, msg, name_img):
	try:	
		newMessage = EmailMessage()                         
		newMessage['Subject'] = Subj
		newMessage['From'] = Sender_Email                   
		newMessage['To'] = Reciever_Email                   
		newMessage.set_content(msg) 

		#gui kem anh
		with open(name_img, 'rb') as f:
			image_data = f.read()
			image_type = imghdr.what(f.name)
			image_name = f.name
		newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

		smtp = smtplib.SMTP_SSL('smtp.gmail.com:465')
		smtp.login(Sender_Email, Password)              
		smtp.send_message(newMessage)
		print("Success: Email sent!")
	except:
		print("Email failed to send!")

# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
#vs = VideoStream(src=2,framerate=10).start()
vs = VideoStream(0).start()    #usePiCamera=True
time.sleep(2.0)


# loop over frames from the video file stream
while True:
	
	#send gmail to check
	# while login == 1:

	# 	Password = getpass.getpass("Nhap password gmail:") #nhap mat khau email
	# 	print("Logging in to gmail account...")
	# 	newMessage = EmailMessage()                         
	# 	newMessage['Subject'] = "Login Gmail!"
	# 	newMessage['From'] = Sender_Email                   
	# 	newMessage['To'] = Reciever_Email                   
	# 	newMessage.set_content("Logged in successfully!") 

	# 	smtp = smtplib.SMTP_SSL('smtp.gmail.com:465')
	# 	smtp.login(Sender_Email, Password)              
	# 	smtp.send_message(newMessage)
	# 	print("Dang nhap thanh cong!")
	# 	login = 0


	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	key = cv2.waitKey(1) & 0xFF
	# quit when 'q' key is pressed
	if key == ord("q"):
		break
	
	# Detect the fce boxes
	boxes = face_recognition.face_locations(frame) #xac dinh vi tri khuon mat can nhan dang
	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(frame, boxes) #ma hoa 
	names = []

	# loop over the facial embeddings
	for encoding in encodings:
		ss1 = 0
		ss2 = 0
		for e in sizelist:
			ss1 = ss1 + e
			ss2 = ss1 - e
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"][ss2:ss1],encoding) #so sanh true false
			faceDis = face_recognition.face_distance(data["encodings"][ss2:ss1],encoding) #sai so
			name = "Unknown" #if face is not recognized, then print Unknown
			
			#kiem tra khuon mat 
			if faceDis[0] < 0.4:
				#kiem tra neu co True trong match
				# check to see if we have found a match
				if True in matches:
					face_error =0   #reset count sai so
					# find the indexes of all matched faces then initialize a
					# dictionary to count the total number of times each face
					# was matched
					matchedIdxs = [i for (i, b) in enumerate(matches)  if b] #tao mang chua key cua cac gia tri true
					counts = {}

					# loop over the matched indexes and maintain a count for
					# each recognized face face
					for i in matchedIdxs:  
						name = data["names"][i+ss2] #truy cap phan tu i trong data["names"]
						counts[name] = counts.get(name, 0) + 1
					# determine the recognized face with the largest number
					# of votes (note: in the event of an unlikely tie Python
					# will select first entry in the dictionary)
					name = max(counts, key=counts.get)
					accept = accept +1
					print("chap nhan: {}".format(accept))

				break

			#neu sai so nhieu lan thi tang count sai so		
			else:
				#accept = 0
				face_error = 1

		# update the list of names
		names.append(name)

	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		if name == "Unknown":
			# draw the predicted face name Unknown on the image - color is in BGR
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 0, 255), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 0, 255), 2)
		if name != "Unknown":
			# draw the predicted face name on the image - color is in BGR
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 255), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 255), 2)

	#kiem tra dieu khien dong mo cua
	if accept > 2:
		print("True,Door open!")
		imwrite("{}.jpg".format(name), frame)  #xuat frame 
		#send gmail with image
		Subj = "You have a visitor!"
		msg = "{}".format(name)
		name_img = '{}.jpg'.format(name)
		send_mail(Subj, msg, name_img)
		#thiet lap lai bo dem va delay 3s
		accept = 0
		sleep(3)

	#neu phat hien nguoi la
	if face_error == 1:
		accept =0
		print("False,Door close!")
		warning_dg = warning_dg + 1

	#khi khong phat hien khuon mat
	if boxes == []:
		print("No one, Door close!")	
		accept = face_error = warning_dg =0

	#canh bao he thong phat Loa va gui gmail dinh kem anh
	if warning_dg == 10:
		print("Canh bao loi nhan dang!")
		print("Bao loa")
		imwrite("{}.jpg".format(name), frame)
		#send gmail 
		Subj = "You have a stranger to visit!"
		msg = "{}".format(name)
		name_img = '{}.jpg'.format(name)
		send_mail(Subj, msg, name_img)
		#thiet lap lai he thong
		warning_dg =0
		
	# display the image to our screen
	cv2.imshow("Facial Recognition is Running", frame)


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
