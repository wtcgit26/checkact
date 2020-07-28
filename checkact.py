from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from time import sleep
from time import gmtime, strftime
import json
import requests


# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url = 'https://hooks.slack.com/services/xxxxxxxxxx/yyyyyyyyyyyyy/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
negative_slack_message = ":sob: ACT is still under maintenance :sob:"
positive_slack_message = ":tada: :grin: Yeah!! ACT is no longer in maintenance!!! <!channel> :grin: :tada:"
# minutes to wait between a negative message to slack
negative_wait = 10
# URL of the website  
url = "https://my.act.org"
search_maintenance_message = "we've taken the MyACT registration page down"


# selenium options
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")

# assumes directory where python app is being run
chrome_driver = "./chromedriver"
#print (chrome_driver)
driver = webdriver.Chrome(options=options, executable_path=chrome_driver)
  

# horribly designed - will run forever unless ctrl-C - version 2.0 will be better
keep_going = True
fire_webhook = True
counting = 0
negative_count = 0
# first pass through
slack_message = negative_slack_message

while(keep_going):

	# Opening the URL in a browser (will be headless if options are made above)
	driver.get(url) 
	# Getting current URL source code as a string
	get_source = driver.page_source 
	# String to search in website
	check_maintenance = get_source.find(search_maintenance_message)
	#print(check_maintenance)

	counting = counting + 1

	clock_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

	if check_maintenance != -1:
		slack_message = negative_slack_message
		print (clock_time, " -- Try #", counting, " -- Still Under Maintenance :-(")
		negative_count = negative_count + 1
		if negative_count == negative_wait:
			fire_webhook = True
			negative_count = 0
	else:
		slack_message = positive_slack_message
		print (clock_time, " -- Try #", counting, " -- No more maintenance -- Yeah - Go get it!!! :-)")
		fire_webhook = True

	if fire_webhook:
		slack_data = {'text': slack_message}	
		response = requests.post(
		    webhook_url, data=json.dumps(slack_data),
		    headers={'Content-Type': 'application/json'}
		)
		if response.status_code != 200:
		    raise ValueError(
		        'Request to slack returned an error %s, the response is:\n%s'
		        % (response.status_code, response.text)
		)
		fire_webhook = False

	sleep(60)


#Debug

# Printing the URL 
#print(get_source) 

#print screenshot of page  
#driver.get_screenshot_as_file("capture.png")

