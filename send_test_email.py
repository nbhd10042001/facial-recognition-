
import smtplib
import imghdr
from email.message import EmailMessage

Sender_Email = "emailpythontest12345@gmail.com"
Reciever_Email = "codeitbro@gmail.com"
Password = input('Enter your email account password: ')

newMessage = EmailMessage()                         
newMessage['Subject'] = "Check out the new logo" 
newMessage['From'] = Sender_Email                   
newMessage['To'] = Reciever_Email                   
newMessage.set_content('Let me know what you think. Image attached!') 

with open('codeitbro-logo.png', 'rb') as f:
    image_data = f.read()
    image_type = imghdr.what(f.name)
    image_name = f.name

newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    
    smtp.login(Sender_Email, Password)              
    smtp.send_message(newMessage)

# def send_email(subject, msg):
#     try:
#         server = smtplib.SMTP('smtp.gmail.com:587')
#         server.ehlo()
#         server.starttls()
#         server.login(config.email_add, password)
#         message = 'Subject: {}\n\n{}'.format(subject, msg)
#         server.sendmail(config.email_add, config.email_add, message)
#         server.quit()
#         print("Success: Email sent!")
#     except:
#         print("Email failed to send.")


