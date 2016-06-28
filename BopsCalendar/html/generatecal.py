#!/usr/bin/python
import json
import webbrowser
import time
from datetime import datetime
from shotgun_api3 import Shotgun


#Change path to reflect file location
#filename = 'file:///Users/mmontagnino/Desktop/python-api-master/fullcalendar-2.8.0/demos/' + 'Calendar.html'
id = "d54c59d248f978ad103976c2b47875b06df5dc56c71afa774901d7791d9d9870"
name = "Test_Calendar"
srvr = "https://participant.shotgunstudio.com"

sg = Shotgun(srvr, name, id)

colors = {'Helen Ly': 'red', 'Rafiah Sessoms': 'blue', 'Nathaniel Bryan': 'green', 'Nick Kubinski': 'purple', 'Marian Montagnino': 'cyan'}

proj = sg.find_one("Project", [["name", "is", "Asset Pipeline"]])
print proj

filters = [
   ['project', 'is', proj],
   ['sg_status_list', 'is', 'wtg']
]
fields = [
        'entity.Shot.sg_sequence.Sequence.code',
	    'entity.Shot.sg_air_date',
	    'entity.Shot.code',
        'content',
        'task_assignees',
        'sg_task_order',
        'Id',
#	    'created_at',
	    'entity.Shot.sg_status_list',
#	    'content',
	    'start_date',
	    'due_date',
	    'entity.Shot.sg_title',
	    'entity.Shot.sg_title_name',
        #	'upstream_tasks',
        #	'downstream_tasks',
        #	'dependency_violation',
        #	'pinned'
]

results = sg.find("Task", filters, fields)

print "Due Date\tShot Code\tTitle\tTitle Name\tContent\tAssigned To"
for r in results:
	s = str(r['due_date'])
	if s == "None":
		print "None\t" + str(r['entity.Shot.code']) + "\t" + str(r['entity.Shot.sg_title']) + "\t" + str(r['entity.Shot.sg_title_name']) + "\t" + str(r['content']) 
	else:
		dueDate = datetime.strptime(s,'%Y-%m-%d') 
		for u in r['task_assignees']:
			print str(dueDate) + "\t" + str(r['entity.Shot.code']) + "\t" + str(r['entity.Shot.sg_title']) + "\t" + str(r['entity.Shot.sg_title_name']) + "\t" + str(r['content']) +"\t" + str(u['name'])

######################
events = ""
for r in range(0, len(results)):
    due = str(results[r]['due_date'])
    if due != "None":
		for u in range(0, len(results[r]['task_assignees'])):
			if len(results) - r > 1 or len(results[r]['task_assignees']) - u > 1:
				event = "				{\n"
				event += "					title: " 
				s = "'" + str(results[r]['entity.Shot.code']) + ", " + str(results[r]['content']) +"',\n"
				event += s
				event += "					url: " 
				s = "'https://participant.shotgunstudio.com/detail/Task/" + str(results[r]['id']) +"',\n"
				event += s
				event += "					backgroundColor: '"
				s = colors[results[r]['task_assignees'][u]['name']] + "',\n"
				event += s
				event += "					start: "
				s = "'" + datetime.strptime(due,'%Y-%m-%d').strftime("%Y-%m-%d") + "'\n"
				event += s
				event += "				},\n"
				events += event
			else:
				event = "				{\n"
				event += "					title: " 
				s = "'" + str(results[r]['entity.Shot.code']) + ", " + str(results[r]['content']) +"',\n"
				event += s
				event += "					url: " 
				s = "'https://participant.shotgunstudio.com/detail/Task/" + str(results[r]['id']) +"',\n"
				event += s
				event += "					backgroundColor: '"
				s = colors[results[r]['task_assignees'][u]['name']] + "',\n"
				event += s
				event += "					start: "
				s = "'" + datetime.strptime(due,'%Y-%m-%d').strftime("%Y-%m-%d") + "'\n"
				event += s
				event += "				}"
				events += event


proj = sg.find_one("Project", [["name", "is", "Media Requests"]])
print proj

filters = [
   ['project', 'is', proj],
   ['sg_status_list', 'is', 'wtg']
]
fields = [
        'content',
        'task_assignees',
        'Id',
	    'due_date'
]

results = sg.find("Task", filters, fields)
	
if len(results) > 0:
	events += ",\n"
else:
	events += "\n"
    
for r in range(0, len(results)):
    due = str(results[r]['due_date'])
    if due != "None":
		for u in range(0, len(results[r]['task_assignees'])):
			if len(results) - r > 1 or len(results[r]['task_assignees']) - u > 1:
				event = "				{\n"
				event += "					title: " 
				s = "'" + str(results[r]['content']) +"',\n"
				event += s
				event += "					url: " 
				s = "'https://participant.shotgunstudio.com/detail/Task/" + str(results[r]['id']) +"',\n"
				event += s
				event += "					backgroundColor: '"
				s = colors[results[r]['task_assignees'][u]['name']] + "',\n"
				event += s
				event += "					start: "
				s = "'" + datetime.strptime(due,'%Y-%m-%d').strftime("%Y-%m-%d") + "'\n"
				event += s
				event += "				},\n"
				events += event
			else:
				event = "				{\n"
				event += "					title: " 
				s = "'" + str(results[r]['content']) +"',\n"
				event += s
				event += "					url: " 
				s = "'https://participant.shotgunstudio.com/detail/Task/" + str(results[r]['id']) +"',\n"
				event += s
				event += "					backgroundColor: '"
				s = colors[results[r]['task_assignees'][u]['name']] + "',\n"
				event += s
				event += "					start: "
				s = "'" + datetime.strptime(due,'%Y-%m-%d').strftime("%Y-%m-%d") + "'\n"
				event += s
				event += "				}"
				events += event


proj = sg.find_one("Project", [["name", "is", "VOD"]])
print proj

filters = [
   ['project', 'is', proj],
   ['sg_status_list', 'is', 'wtg']
]
fields = [
        'entity.Shot.sg_sequence.Sequence.code',
        'content',
        'task_assignees',
        'Id',
	    'entity.Shot.sg_title',
	    'entity.Shot.sg_title_name',
	    'due_date'
]

results = sg.find("Task", filters, fields)

if len(results) > 0:
	events += ",\n"
else:
	events += "\n"

print "Due Date\t\tTitle Name\t\tContent\t\t\tAssigned To"
for r in results:
	s = str(r['due_date'])
	if s == "None":
		print "None\t" + str(r['entity.Shot.sg_title_name']) + "\t" + str(r['content']) 
	else:
		dueDate = datetime.strptime(s,'%Y-%m-%d') 
		for u in r['task_assignees']:
			print str(dueDate) + "\t" + str(r['entity.Shot.sg_title_name']) + "\t" + str(r['content']) +"\t" + str(u['name'])

for r in range(0, len(results)):
    due = str(results[r]['due_date'])
    if due != "None":
		for u in range(0, len(results[r]['task_assignees'])):
			if len(results) - r > 1 or len(results[r]['task_assignees']) - u > 1:
				event = "				{\n"
				event += "					title: " 
				s = "'" + str(results[r]['entity.Shot.sg_title_name']) + ", " + str(results[r]['content']) +"',\n"
				event += s
				event += "					url: " 
				s = "'https://participant.shotgunstudio.com/detail/Task/" + str(results[r]['id']) +"',\n"
				event += s
				event += "					backgroundColor: '"
				s = colors[results[r]['task_assignees'][u]['name']] + "',\n"
				event += s
				event += "					start: "
				s = "'" + datetime.strptime(due,'%Y-%m-%d').strftime("%Y-%m-%d") + "'\n"
				event += s
				event += "				},\n"
				events += event
			else:
				event = "				{\n"
				event += "					title: " 
				s = "'" + str(results[r]['entity.Shot.sg_title_name']) + ", " + str(results[r]['content']) +"',\n"
				event += s
				event += "					url: " 
				s = "'https://participant.shotgunstudio.com/detail/Task/" + str(results[r]['id']) +"',\n"
				event += s
				event += "					backgroundColor: '"
				s = colors[results[r]['task_assignees'][u]['name']] + "',\n"
				event += s
				event += "					start: "
				s = "'" + datetime.strptime(due,'%Y-%m-%d').strftime("%Y-%m-%d") + "'\n"
				event += s
				event += "				}\n"
				events += event


f = open('E:\\scripts\Pivot\BopsCalendar\html\BopsCalendar.html','w')

message = """<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<meta http-equiv="refresh" content="900" > 
<link href='../fullcalendar.css' rel='stylesheet' />
<link href='../fullcalendar.print.css' rel='stylesheet' media='print' />
<script src='../lib/moment.min.js'></script>
<script src='../lib/jquery.min.js'></script>
<script src='../fullcalendar.min.js'></script>
<script>

	$(document).ready(function() {
		
		$('#calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,basicWeek,basicDay'
			},
			defaultDate: """
message += "'"+time.strftime("%Y-%m-%d")+"'"
message += """,
			editable: false,
			eventLimit: true, // allow "more" link when too many events
			events: [
""" 
message += events
message += """
			]
		});
	});

</script>
<style>

	body {
		margin: 40px 10px;
		padding: 0;
		font-family: "Lucida Grande",Helvetica,Arial,Verdana,sans-serif;
		font-size: 14px;
        
	}

	#calendar {
		max-width: 1200px;
		margin: 0 auto;
	}
    .my-legend {
	    max-width: 1200px;
	    margin: 0 auto;
    }
	.my-legend .legend-title {
	    text-align: left;
	    margin-bottom: 8px;
	    font-weight: bold;
	    font-size: 90%;
        max-width: 1200px;
	    }
	  .my-legend .legend-scale ul {
	    margin: 0;
	    padding: 0;
	    float: left;
	    list-style: none;
	    }
	  .my-legend .legend-scale ul li {
	    display: block;
	    float: left;
	    width: 50px;
	    margin-bottom: 6px;
	    text-align: center;
	    font-size: 80%;
	    list-style: none;
	    }
	  .my-legend ul.legend-labels li span {
	    display: block;
	    float: left;
	    height: 15px;
	    width: 50px;
	    }
	  .my-legend .legend-source {
	    font-size: 70%;
	    color: #999;
	    clear: both;
	    }
	  .my-legend a {
	    color: #777;
	    }
    
</style>
</head>
<body>
	<div id='calendar'></div>
	<div class='my-legend'>
	<div class='legend-title'>Color Mapping:</div>
	<div class='legend-scale'>
	  <ul class='legend-labels'>
	    <li><span style='background:red;'></span>Helen</li>
	    <li><span style='background:blue;'></span>Rafiah</li>
	    <li><span style='background:green;'></span>Nathaniel</li>
	    <li><span style='background:purple;'></span>Nick</li>
	    <li><span style='background:cyan;'></span>Marian</li>
	  </ul>
	</div>
	</div>
</body>
</html>
"""

f.write(message)
f.close()


