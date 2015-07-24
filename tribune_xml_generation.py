import csv
from xml.etree.ElementTree import Element, SubElement, ElementTree
import time
from time import mktime
from datetime import datetime
import xml.sax.saxutils as saxutils
import sys  

reload(sys)  
sys.setdefaultencoding('latin-1')

lines_seen = set() # holds lines already seen
outfile = open('E:\\\\tribune\\outfile.txt', "w")

for line in open('E:\\\\tribune\\TMSIDSEARCH (1225-665).txt', "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

f = csv.reader(open('E:\\\\tribune\\outfile.txt'), delimiter='\t')

# create XML 
root = Element('xml')
header = SubElement(root,'header')
provider_child  = Element('provider',id='PM1234')
provider_child.text = 'ParticipantMedia'
header.append(provider_child)

schedule = SubElement(root,'schedule')

i = 1
for row in f:
    if row[11] in ('0','',None):
        print str(i) + '\t' + row[0] + '\t' + row[10]
        Title_Code = row[0].encode('latin-1').strip()
        Title_Class = row[1].encode('latin-1').strip()
        Default__Series_Name = row[2].encode('latin-1').strip()
        Title_Code_w_o_Prefix = row[3].encode('latin-1').strip()
        Default__Title_Synopsis = row[4].encode('latin-1').strip()
        Default__Title_Name = row[5].encode('latin-1').strip()
        
        if Title_Class in ('Episode'):
            print "Title_Code_w_o_Prefix: " + str(int(float(Title_Code_w_o_Prefix)))
            if row[6].encode('latin-1').strip() not in ('null','',None):
                Season = row[6].encode('latin-1').strip()
            if row[6].encode('latin-1').strip() in ('null','',None):
		        Season = str(int(float(Title_Code_w_o_Prefix)))[:1]
        print "Season: " + Season
        Title_First_AirScheduled_Date_All_Schedules__TP_ = row[7].encode('latin-1').strip()
        #Title_MPAA_Code = row[8].encode('latin-1').strip()
        Title_Release_Year = row[9].encode('latin-1').strip()
        Stars = row[10].encode('latin-1').strip()
        TtlTMSID = row[11].encode('latin-1').strip()
        print row[12] + '\t'
        print row[13]
        if row[12] not in ('UFN','TBD'):
            Window_Start_Date = datetime.fromtimestamp(mktime(time.strptime(row[12],'%m/%d/%Y')))
        if row[13] not in ('UFN','TBD'):
            Window_End_Date = datetime.fromtimestamp(mktime(time.strptime(row[13],'%m/%d/%Y')))	
        if row[12] in ('UFN','TBD'):
            Window_Start_Date = row[12]
        if row[13] in ('UFN','TBD'):
            Window_End_Date = row[13]
        event = Element('event')
        Title_Length___HHMMSS__ = row[14]
        Title_FCC_Rating = row[15].encode('latin-1').strip()
        #Title_EPG_Code = row[16].encode('latin-1').strip()
        Title_Caption_Definitions = row[17].encode('latin-1').strip()
		
        programId = Element('programId')
        programId.text = Title_Code
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
        availWindow = Element('availWindow')
        start = Element('start')
        if row[12] not in ('UFN','TBD'):
            start.text = Window_Start_Date.strftime('%Y-%m-%d') + 'T00:00:00-05:00'
        end = Element('end')
        if row[13] not in ('UFN','TBD'):
            end.text = Window_End_Date.strftime('%Y-%m-%d') + 'T00:00:00-05:00'
        length = Element('length')
        length.text = Title_Length___HHMMSS__
        FCC = Element('fccRating')
        FCC.text = 'TV-' + Title_FCC_Rating
        #EPG = Element('epg')
        #EPG.text = Title_EPG_Code
        CaptionDef = Element('captionDefinition')
        CaptionDef.text = Title_Caption_Definitions
        event.append(programId)
        event.append(programType)
        if Title_Class in ('Episode'):
            event.append(seriesName)
            event.append(season)
        event.append(title)
        event.append(firstAirDate)
        event.append(Release)
        event.append(Actors)
        availWindow.append(start)
        availWindow.append(end)
        event.append(availWindow)
        event.append(length)
        event.append(FCC)
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

indent(root)

tree = ElementTree(root)

tree.write("output.xml", xml_declaration=True, encoding='utf-8', method="xml")	  
