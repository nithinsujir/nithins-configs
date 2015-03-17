import smtplib
import os
import optparse
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SERVER = 'mail.broadcom.com'

class Emailer:
    def __init__(self, recepients, sender):
        self.server = SERVER
        self.recepients = recepients
        self.sender = sender


    def send_email(self, subject = 'No Subject', message = 'No Message'):
        session = smtplib.SMTP(self.server)

        #message = 'From: %s\nTo: %s\nSubject: %s\n\n%s\n' % (self.sender, self.recepients, subject, message)
        #message = self.createhtmlmail('<html><head>headd</head><body font="arial" color="red">abcd</body></html>', message, subject)

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = self.recepients

        # Create the body of the message (a plain-text and an HTML version).
        text = ''
        for line in message:
            text = text + '\n' + line
        html = """\
        <html>
          <head></head>
          <body>
            <p style="color:white; background-color:firebrick" >
            """
        print message
        for line in message:
            html = html + '<br>' + line
        html = html + """\
            </p>
          </body>
        </html>
        """

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)


        rval = session.sendmail(self.sender, self.recepients, msg.as_string())
        
if __name__ == "__main__":
    em = Emailer('nithinsujir@gmail.com', 'nithinsujir@gmail.com')
    #em = Emailer('nsujir@broadcom.com', 'nsujir@broadcom.com')
    subj = 'Test Mail'
    body = 'Mail Body'

    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', dest='file')
    parser.add_option('-s', '--subj', dest='subj')

    (opts, args) = parser.parse_args()

    if opts.file:
        fil = open(opts.file, 'r')
        body = fil.readlines()
        fil.close()

    if opts.subj:
        subj = opts.subj

    em.send_email(subj, body)
