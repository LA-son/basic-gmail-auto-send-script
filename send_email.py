import smtplib
import logging
import time
from string import Template
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#set up smtp server
MY_ADDRESS = '########@gmail.com'
MY_PASSWORD = "##########"

session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls() #enable security ?
session.login(MY_ADDRESS, MY_PASSWORD)

def get_contact(filename):
	names = []
	emails = []
	with open(filename, mode='r',encoding='utf-8') as file_handler:
		for line in file_handler:
			temp = []
			for item in line.split(","):
				if item.find("@") > 0:
					temp.append(item)
			if not temp:
				continue
			names.append(line.split(",")[0])
			emails.append(temp)
	return names, emails

def read_template(filename):
	with open(filename, mode='r',encoding='utf-8') as file_handler:
		file_template = file_handler.read()
	return Template(file_template)

#fetch names, emails of receiver

names = []
emails =[]
names, emails = get_contact('/path_to_CSV_file/email_list.csv')

message_template = read_template('/path_to_message_template/message.txt')
count = 0
for name, email in zip(names, emails):
	msg = MIMEMultipart() #create message

	#add the receiver's name (${PERSON_NAME})

	message = message_template.substitute(PERSON_NAME=name)
	print(name)
	count = count + 1
	print(count)
	#setup parameters of the message

	msg['From'] = MY_ADDRESS
	if len(email) > 1:
		first_email = email.pop(0)
		cc = ""
		for item in email:
			if item == email[-1]:
				cc = cc + item
			else:
				cc = cc + item + ","
		msg['To'] = first_email
		msg['Cc'] = cc
	else:
		msg['To'] = email[0]

	msg['Subject'] = "Email subject"
	

	#add message in body
	msg.attach(MIMEText(message,'html'))

	#attach pdf (file 1)
	with open("/path_to_attached_file/file1.pdf", "rb") as f:
		attachthue = MIMEApplication(f.read(),_subtype="pdf")

	attachthue.add_header('Content-Disposition','attachment',filename=str("file1.pdf"))
	msg.attach(attachthue)

	#attach pdf (file 2)
	with open("/path_to_attached_file/file2.pdf", "rb") as f:
		attachtk = MIMEApplication(f.read(),_subtype="pdf")

	attachtk.add_header('Content-Disposition','attachment',filename=str("file2.pdf"))
	msg.attach(attachtk)

	#send message
	session.send_message(msg)
	
	#delete object after use
	del msg
	time.sleep(2)