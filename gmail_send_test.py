#https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4Ofjn3ID_vhD7J2hl8VNONJdXGSPlue0PjxQbYhLqDq0w1gTrIeagJk0xtqc7yCaVMt2g7PTmZNMbqTN_i7aoACm3kBOg
#kich hoat quyen truy cap kem an toan

# import smtplib
# import config
# import getpass

# email_pw = getpass.getpass("nhap mat khau cho email: ")
# def send_email(subject, msg):
#     try:
#         server = smtplib.SMTP('smtp.gmail.com:587')
#         server.ehlo()
#         server.starttls()
#         server.login(config.email_add, email_pw)
#         message = 'Subject: {}\n\n{}'.format(subject, msg)
#         server.sendmail(config.email_add, config.email_add, message)
#         server.quit()
#         print("Success: Email sent!")
#     except Exception as e:
#         print(str(e))

# subject = "Test subject"
# msg = "Hello there, how are you today?"

# send_email(subject, msg)

import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "nbhd10042001@gmail.com"
password = input("Type your password and press enter: ")

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)
    # TODO: Send email here
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 