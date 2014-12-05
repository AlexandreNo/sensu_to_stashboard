#!/usr/bin/env python
import urllib
import urllib2
import json
import sys

# States
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

base_url = '127.0.0.1:8080'

# Read info from Sensu handler
sensu_event = sys.stdin.read()
res = json.loads(sensu_event)

# Get service list
service_url = 'http://%s/admin/api/v1/services' % base_url
response_service = urllib2.urlopen(service_url)
services_list = json.loads(response_service.read())

for service in services_list['services']:
	if service['name'] == res['check'].get('name'):
		if res['check'].get('status') == STATE_OK:
			url = 'http://%s/admin/api/v1/services/%s/events' % (base_url, service['id'])
			values = {'status' : 'up',
		        'message' : 'The service is up.' }
		elif res['check'].get('status') == STATE_CRITICAL:
			status_url = 'http://%s/admin/api/v1/services/%s' % (base_url, service['id'])
			response_status = urllib2.urlopen(status_url)
			status_list = json.loads(response_status.read())
			if status_list['current-event'].get('status')['id'] != 'down':
				url = 'http://%s/admin/api/v1/services/%s/events' % (base_url, service['id'])
				values = {'status' : 'down',
        			'message' : 'The service is not running correctly.' }

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
