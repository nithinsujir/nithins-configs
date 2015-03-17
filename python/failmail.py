# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_fail(to, line):
	msg = MIMEText(line)
	msg['Subject'] = 'Test email'
	msg['From'] = 'nsujir@broadcom.com'
	msg['To'] = 'nsujir@broadcom.com'

	s = smtplib.SMTP('mail.broadcom.com')
	s.sendmail('nsujir@broadcom.com', to, msg.as_string())
	s.quit()
