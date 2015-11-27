import os
import sys
from datetime import datetime

import time
import smtplib

## functions #################################################################
    
def send(content, recipient, subject, sender, verbose=False):
    # |content| should be a string
    # |recipient| should be an email address (string)
    # |subject| should be a string
    # |sender| should be a GmailAccount object instance
    # |verbose| should be a boolean value
    
    if verbose: print("Firing up email server ...")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(sender.username, sender.password)
    
    if verbose: print("Composing email ...")
    headers = "\r\n".join(["from: %s" % sender.name,
                           "subject: %s" % subject,
                           "to: %s" % recipient,
                           "mime-version: 1.0",
                           "content-type: text/html",
                           "reply-to: %s@gmail.com" % sender.username])
    content = headers + "\r\n\r\n" + content
    
    if verbose: print("Sending mail ...")
    server.sendmail(sender.username + "@gmail.com", recipient, content)
    server.quit()

    if verbose: print("Done!")

## GmailAccount ##############################################################

class GmailAccount(object):

    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name
