#!/usr/bin/env python
#
# Script to receive an alert if a new picture is shown in a public folder of dropbox
#
# Author: Loto <lotooo@gmail.com>
#
import requests
from lxml import html
import json
import sys
from sender import Mail
import hashlib

config_file = "config.json"

# Try to open and read the config file
try:
	with open(config_file, 'r') as c:
		config = json.load(c)
except:
	print("Impossible to read your configuration file")
	print("Please create a config.json file")
	sys.exit(2)

# Let's loop over the dropbox public folder we are monitoring
for dp in config['sources']:
	dropbox_public_url = dp['url']

	# Create a md5 hash from the url to get a unique backup filename
	m = hashlib.md5()
	m.update(dropbox_public_url.encode())
	backup_file = m.hexdigest() + '.json'

	try:
		# If a backup file of already seen pictures exist, open it
		f = open(backup_file, 'r')
		pictures_seen = set(json.load(f))
		f.close()
	except:
		# It is the first time you run this script
		print("No previous pictures. Creating an empty set")
		pictures_seen = set()

	last_pictures = set()

	raw = requests.get(dropbox_public_url)
	doc = html.fromstring(raw.content)

	# Grab the list of link of pictures
	for a in doc.find_class('filename-link'):
		last_pictures.add(a.attrib['href'])


	# Build a set of mot seen pictures. The last pictures list - the saved pictures list
	pictures_not_seen = last_pictures - pictures_seen

	if len(pictures_not_seen) == 0:
		print("No new pictures. Exiting")
	else:
		# Send an email containing the URL of the new pictures
		mail = Mail(config['smtp']['host'], 
				port	 = int(config['smtp']['port']),
				username = config['smtp']['username'],
				password = config['smtp']['password'],
				use_tls	 = config['smtp']['use_tls'],
				use_ssl	 = config['smtp']['use_ssl'])
		body = "<p>A new picture has been posted !</p>"

		for picture in pictures_not_seen:
			body += "- <a href='%s'>%s</a><br>" % (picture, picture)

		mail.send_message("New pictures of %s" % dp['name'], fromaddr=dp['from'], bcc=dp['to'], html=body)

	# Save the last pictures seen to the backup file
	with open(backup_file, 'w') as f:
		f.write(json.dumps(list(last_pictures), indent=4))


