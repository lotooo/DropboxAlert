Dropbox Alert
=============

Script to send an email alert in case a dropbox public folder contains new pictures.

Installation
------------

pip install requests
pip install lxml
pip install sender
pip install hashlib

git clone https://github.com/lotooo/DropboxAlert.git

Configuration
-------------

Rename the config.json.example file to config.json and edit it.

### SMTP

Configure the SMTP server you want to use with :

	"smtp": {
                "host"          : "smtp.gmail.com",
                "port"          : "465",
                "username"      : "xxxxx",
                "password"      : "yyyxxxzzz",
                "use_tls"       : false,
                "use_ssl"       : true,
                "debug_level"   : null
        }

### Sources

Modify the default source and add the one you want in the JSON file :

	"sources" : [
		{
			"name" 	: "Cool blog",
			"url"	: "https://www.dropbox.com/sh/yyyyyyyyyyyy/xxxxxxxxxxxxxxx?dl=0#/",
			"from"	: "toto@gmail.com",
			"to"	: ["toto@gmail.com"]
		}
	],
