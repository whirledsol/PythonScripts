'''
sgsend
Sends email from parameters via sendgrid api

@author: Will Rhodes
NOTE: DO NOT RUN AS SUDO. REQUIRES ENV VAR.
'''
import traceback
import sendgrid
import os
import sys
import datetime
import base64
from sendgrid.helpers.mail import *

logpath = 'mail.log'
now = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
from_email = 'peachpie@willrhod.es'
to_email = sys.argv[1] if len(sys.argv) > 1 else None
subject = sys.argv[2] if len(sys.argv) > 2 else 'A Message from your cute peachpie'
content = sys.argv[3] if len(sys.argv) > 3 else 'No body was sent. Shame.'
file = sys.argv[4] if len(sys.argv) > 4 else None

def createAttachment():
	filename, file_ext = os.path.splitext(file)
	with open(file, "rb") as openfile:
		attachment = Attachment()
		attachment.content = base64.b64encode(openfile.read())
		attachment.type = "application/" + file_ext.strip('.')
		attachment.filename = filename + file_ext
		attachment.disposition = "attachment"
		attachment.content_id = "attachment"
		return attachment




if(to_email is None or '@' not in to_email):
	with open(logpath,'a') as log:
		log.write("%s\t%s\n" % (now,'Incorrect Parameters'))
	sys.exit(0)

apikey = os.environ.get('SENDGRID_API_KEY')

if(apikey is None):
	with open(logpath,'a') as log:
                log.write("%s\t%s\t%s\n" % (now,to_email,'No API Key Specified'))
        sys.exit(0)

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email(from_email)
to_email = Email(to_email)
content = Content("text/plain", content)
mail = Mail(from_email, subject, to_email, content)

try:
	if(file is not None):
		mail.add_attachment(createAttachment())
	#print mail.get()
	response = sg.client.mail.send.post(request_body=mail.get())
	with open(logpath,'a') as log:
		log.write("%s\t%s\t%s\t%s\t%s\n" % (now, to_email, response.status_code,response.body,response.headers))
	#print(response.status_code)
	#print(response.body)
	#print(response.headers)
except:
	with open(logpath,'a') as log:
        	log.write("%s\t%s\n" % (now, sys.exc_info()[0]))
	traceback.print_exc()

