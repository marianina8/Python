import csv
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xml.etree.ElementTree as ET
import time
from time import mktime
from datetime import datetime, timedelta
import xml.sax.saxutils as saxutils
import sys  
from ftplib import FTP
import datetime
import os, sys
import gzip
import re
from smtplib import SMTP_SSL as SMTP 
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import shutil

reload(sys)  
sys.setdefaultencoding('latin-1')

now = datetime.date.today()

ftp = FTP('ftp.dnsname.com')
ftp.login('username','password')
ftp.cwd('On2')
ftp.cwd('pivo')

files = []

try:
    files = ftp.nlst()
except ftplib.error_perm, resp:
    if str(resp) == "550 No files found":
        print "No files in this directory"
    else:
        raise

try:	
    if not os.path.exists("E:\\\\tribune\\" + now.strftime("%Y%m%d") + "\\"):
        os.makedirs("E:\\\\tribune\\" + now.strftime("%Y%m%d") + "\\")
except resp:
    print "Folder already created."

folder = "E:\\\\tribune\\" + now.strftime("%Y%m%d") + "\\"

try:
    on_connector_programs_filename = now.strftime("on_connector_programs-PIVOT_%Y%m%d.xml.gz")
    rcommand = "RETR " + on_connector_programs_filename
    ftp.retrbinary(rcommand,open(folder + on_connector_programs_filename, 'wb').write)
    zipFile = gzip.open(folder + on_connector_programs_filename,"rb")
    unCompressedFile = open(folder + now.strftime("on_connector_programs-PIVOT_%Y%m%d.xml"),"wb")	
    decoded = zipFile.read()
    unCompressedFile.write(decoded)
    zipFile.close()
    unCompressedFile.close()
    os.remove(folder + on_connector_programs_filename)
except Exception as e:
    print str(e)
    shutil.rmtree(folder)
    sys.exit(0)

try:
    on_connectors_filename = now.strftime("on_connectors-PIVOT_%Y%m%d.xml.gz")
    rcommand = "RETR " + on_connectors_filename
    ftp.retrbinary(rcommand,open(folder + on_connectors_filename, 'wb').write)
    zipFile = gzip.open(folder + on_connectors_filename,"rb")
    unCompressedFile = open(folder + now.strftime("on_connectors-PIVOT_%Y%m%d.xml"),"wb")	
    decoded = zipFile.read()
    unCompressedFile.write(decoded)
    zipFile.close()
    unCompressedFile.close()
    os.remove(folder + on_connectors_filename)
except Exception as e:
    shutil.rmtree(folder)
    sys.exit(0)
	
try:
    on_unmappables_filename = now.strftime("on_unmappables-PIVOT_%Y%m%d.xml.gz")
    rcommand = "RETR " + on_unmappables_filename
    download_response = ftp.retrbinary(rcommand,open(folder + on_unmappables_filename, 'wb').write)
    zipFile = gzip.open(folder + on_unmappables_filename,"rb")
    unCompressedFile = open(folder + now.strftime("on_unmappables-PIVOT_%Y%m%d.xml"),"wb")	
    decoded = zipFile.read()
    unCompressedFile.write(decoded)
    zipFile.close()
    unCompressedFile.close()
    os.remove(folder + on_unmappables_filename)
except Exception as e:
    shutil.rmtree(folder)
    sys.exit(0)

try:	
    tree = ET.parse(folder + now.strftime("on_connectors-PIVOT_%Y%m%d.xml"))
    root = tree.getroot()
except Exception as e:
    sys.exit(0)

	
newIds = set()
for line in open('E:\\\\tribune\\new.txt', "r"):
     newIds.add(line.strip())
    
with open(folder + now.strftime("mappings_%Y%m%d.csv"), 'wb') as csvfile:
     fieldnames = ['house_id', 'tmsid']
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writeheader()
     for connectors in root.findall('connectors'):
          ENTITY = connectors.findall('entity')
          for element in ENTITY:
               ID = element.findall("id")
               LINK = element.findall("link")
               for item in ID:
                    if item.get("type") == "TMSId":
                         TMSId = item.text
               for link in LINK:
                    if link.get("idType") == "ProviderId":
                         ProviderId = link.text
               if ProviderId in newIds: # is it a new id
                    writer.writerow({'house_id': ProviderId, 'tmsid': TMSId})

tree = ET.parse(folder + now.strftime("on_unmappables-PIVOT_%Y%m%d.xml"))
root = tree.getroot()

with open(folder + now.strftime("unmapped_%Y%m%d.csv"), 'wb') as csvfile:
     fieldnames = ['house_id', 'tmsid','reason']
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writeheader()
     for connectors in root.findall('connectors'):
          ENTITY = connectors.findall('entity')
          for element in ENTITY:
               ID = element.findall("id")
               LINK = element.findall("link")
               MESSAGE = element.findall("message")
               for item in ID:
                    if item.get("type") == "TMSId":
                         TMSId = item.text
               for link in LINK:
                    if link.get("idType") == "ProviderId":
                         ProviderId = link.text
               for message in MESSAGE:
                    Reason = message.get("reason")
                    Reason += ', Missing'
                    DETAIL = message.findall('detail')
                    for details in DETAIL:
                         Reason += ' ' + details.text + ','	
               Reason = Reason[:-1]						 
               if ProviderId in newIds: # is it a new id
                    writer.writerow({'house_id': ProviderId, 'tmsid': TMSId, 'reason': Reason})


SMTPserver = 'smtp.emailsrvr.com'
sender =     'notification@participantmedia.com'
destination = ["chommel@participantmedia.com","amorton@participantmedia.com","cschechtman@participantmedia.com", "mmontagnino@participantmedia.com", "bkukla@participantmedia.com"]
#For test purposes:
#destination = ["mmontagnino@participantmedia.com"]

USERNAME = "notification@participantmedia.com"
PASSWORD = "Jackass2014"

# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'


content="""\
Attached are the daily results from Gracenote, mapped results and unmapped with reason.
"""


os.chdir(folder)

try:
    subject=now.strftime("Gracenote TMS Mapped Results - %m/%d/%Y")
    msg = MIMEMultipart()
    mapped_filename = now.strftime("mappings_%Y%m%d.csv")
    f1 = file(mapped_filename)
    attachment1 = MIMEText(f1.read())
    attachment1.add_header('Content-Disposition', 'attachment1', filename=mapped_filename)  
 
    msg.attach(attachment1)
    msg['Subject']=       subject
    msg['From']   = sender # some SMTP servers will do this automatically, not all

    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)
    try:
        conn.sendmail(sender, destination, msg.as_string())
    finally:
        conn.close()

except Exception, exc:
    sys.exit( "mail failed; %s" % str(exc) ) # give a error message

	
try:
    subject=now.strftime("Gracenote TMS Unmapped Results - %m/%d/%Y")
    msg = MIMEMultipart()
    unmapped_filename = now.strftime("unmapped_%Y%m%d.csv")
    f2 = file(unmapped_filename)    
    attachment2 = MIMEText(f2.read())
    attachment2.add_header('Content-Disposition', 'attachment2', filename=unmapped_filename)  
    msg.attach(attachment2)
    msg['Subject']=       subject
    msg['From']   = sender # some SMTP servers will do this automatically, not all

    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)
    try:
        conn.sendmail(sender, destination, msg.as_string())
    finally:
        conn.close()

except Exception, exc:
    sys.exit( "mail failed; %s" % str(exc) ) # give a error message
