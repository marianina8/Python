import csv
from xml.etree.ElementTree import Element, SubElement, ElementTree
import time
from time import mktime
from datetime import datetime
import xml.sax.saxutils as saxutils
import sys  
from ftplib import FTP
import os, sys

reload(sys)  
sys.setdefaultencoding('latin-1')

lines_seen = set() # holds lines already seen
outfile = open('E:\\\\tribune\\participantmedia_programs.txt', "w")
newlist = open('E:\\\\tribune\\new.txt', "w")

j=1
for line in open('E:\\\\tribune\\TMSIDSEARCH (1225-665).txt', "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

# create XML 
root = Element('xml')
header = SubElement(root,'header')
provider_child  = Element('provider',id='PM1234')
provider_child.text = 'ParticipantMedia'
header.append(provider_child)

schedule = SubElement(root,'schedule')

i = 1
with open('E:\\\\tribune\\participantmedia_programs.txt') as f:
    f = csv.reader(f, delimiter='\t')
    for row in f:
        if row[1] in ('0','',None):
			print str(i) + '\t' + row[0] + '\t' + row[4]
			Title_Code = row[0].encode('latin-1').strip()
			Title_Class = row[2].encode('latin-1').strip() 
			Default__Series_Name = row[3].encode('latin-1').strip()
			Title_Code_w_o_Prefix = row[6].encode('latin-1').strip()
			Default__Title_Synopsis = row[7].encode('latin-1').strip()
			Default__Title_Name = row[4].encode('latin-1').strip()

			if Title_Class in ('Episode'):
				if row[6].encode('latin-1').strip() not in ('null','',None):
					print "Season: " + str(int(float(Title_Code_w_o_Prefix)))[:1]
					print "Episode: " + str(int(str(int(float(Title_Code_w_o_Prefix)))[1:]))
					Season = str(int(float(Title_Code_w_o_Prefix)))[:1]
					Episode = str(int(str(int(float(Title_Code_w_o_Prefix)))[1:]))
				if row[6].encode('latin-1').strip() in ('null','',None):
					Season = str(int(float(Title_Code_w_o_Prefix)))[:1]
			
			Title_First_AirScheduled_Date_All_Schedules__TP_ = row[9].encode('latin-1').strip()
			#Title_MPAA_Code = row[8].encode('latin-1').strip()
			Title_Release_Year = row[10].encode('latin-1').strip()
			Stars = row[8].encode('latin-1').strip()
			TtlTMSID = row[1].encode('latin-1').strip()
			event = Element('event')
			Title_Length___HHMMSS__ = row[11]
			Title_FCC_Rating = row[12].encode('latin-1').strip()
			#Title_EPG_Code = row[13].encode('latin-1').strip()
			Title_Caption_Definitions = row[14].encode('latin-1').strip()
			
			programId = Element('programId')
			programId.text = Title_Code
			newlist.write(Title_Code + '\n')
			programType = Element('programType')
			if Title_Class in ('Film'):
				programType.text = 'Movie'
			else:
				programType.text = Title_Class
			if Title_Class in ('Episode'):
				seriesName = Element('seriesName')
				seriesName.text = Default__Series_Name.encode('utf-8')
				season = Element('season')
				season.text = Season
				episode = Element('episode')
				episode.text = Episode
			#titleCode = Element('titleCode')
			#titleCode.text = Title_Code_w_o_Prefix
			titleSynopsis = Element('titleSynopsis')
			titleSynopsis.text = Default__Title_Synopsis
			title = Element('title',lang='eng')
			title.text = Default__Title_Name
			firstAirDate = Element('firstAirDate')
			firstAirDate.text = Title_First_AirScheduled_Date_All_Schedules__TP_
			#MPAA = Element('mpaaCode')
			#MPAA.text = Title_MPAA_Code
			Release = Element('releaseYear')
			Release.text = Title_Release_Year
			Actors = Element('actors')
			Actors.text = Stars
			length = Element('length')
			length.text = Title_Length___HHMMSS__
			FCC = Element('fccRating')
			if Title_FCC_Rating.strip() in (''):
			    print "Title_FCC_Rating = " + Title_FCC_Rating
			    FCC.text = ''
			else:
			    FCC.text = 'TV-' + Title_FCC_Rating
			    print "Title_FCC_Rating = " + Title_FCC_Rating
			#EPG = Element('epg')
			#EPG.text = Title_EPG_Code
			CaptionDef = Element('captionDefinition')
			CaptionDef.text = Title_Caption_Definitions
			event.append(programId)
			event.append(programType)
			if Title_Class in ('Episode'):
				event.append(seriesName)
				event.append(season)
				event.append(episode)
			#event.append(titleCode)
			event.append(title)
			event.append(firstAirDate)
			#event.append(MPAA)
			event.append(Release)
			event.append(Actors)
			event.append(length)
			event.append(FCC)
			#event.append(EPG)
			event.append(CaptionDef)
			schedule.append(event)
			i += 1
		
def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

newlist.close()

indent(root)

tree = ElementTree(root)

tree.write("E:\\\\tribune\\participantmedia_programs.xml", xml_declaration=True, encoding='utf-8', method="xml")	  

ftp = FTP('ftp.dnsname.com')
ftp.login('username','password')

try:
    file = open("E:\\\\tribune\\participantmedia_programs.xml",'rb')                  # file to send
    ftp.storbinary('STOR participantmedia_programs.xml', file)     # send the file
    file.close()                                    # close file and FTP
    ftp.quit()
    os.remove("E:\\\\tribune\\participantmedia_programs.txt")
except Exception as e:
    print str(e)
    sys.exit(0)


