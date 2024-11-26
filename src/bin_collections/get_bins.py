import json
import requests
import os
import boto3
from datetime import datetime, timedelta

API_URL = "https://manchester.form.uk.empro.verintcloudservices.com/api/custom?action=bin_checker-get_bin_col_info&actionedby=_KDF_custom&loadform=true&access=citizen&locale=en"
AUTH_URL = "https://manchester.form.uk.empro.verintcloudservices.com/api/citizen?archived=Y&preview=false&locale=en"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0"}
TIMEOUT = 10
UPRN = os.environ['UPRN']
BIN_MAP = {
    "ahtm_dates_black_bin": "Black bin",
    "ahtm_dates_brown_commingled_bin": "Brown bin",
    "ahtm_dates_blue_pulpable_bin": "Blue bin",
    "ahtm_dates_green_organic_bin": "Green Bin",
}
NOTIFICATIONS_ENABLED = os.environ['NOTIFICATIONS_ENABLED']

sns = boto3.client("sns")

#Publish message to SNS topic
def publish(message):
    sns.publish(
        TopicArn = os.environ['SNS_TOPIC'],
        Subject = "Bin Collections",
        Message = message
    )

#Get auth token
def auth():
    response = requests.get(
        AUTH_URL,
        headers=HEADERS,
        timeout=TIMEOUT,
    )
    auth_token = response.headers["authorization"]
    return auth_token

#Query which bins it is this week
def main(event, context):
    auth_token = auth()
    post_data = {
        "name": "sr_bin_coll_day_checker",
        "data": {
            "uprn": UPRN,
            "nextCollectionFromDate": (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            "nextCollectionToDate": (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
        },
        "email": "",
        "caseid": "",
        "xref": "",
        "xref1": "",
        "xref2": ""
    }
    headers = {
        "Referer": "https://manchester.portal.uk.empro.verintcloudservices.com/",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": auth_token,
    }

    #Get bin collections
    response = requests.post(API_URL, data=json.dumps(post_data), headers=headers)
    data = response.json()
    bins = []
    
    #Loop over each item and if the bin has a date set, lookup the bin type in the collections_map add it to the bins array
    for k,v in data["data"].items():
        if k.startswith("ahtm_dates_"):
            coll_date = v.split(";")[0].strip()
            if coll_date != "":
                bins.append(BIN_MAP.get(k))

    #Send message with the bins to be collected tomorrow
    if len(bins) > 0:
        message = "The bins for collection tomorrow are: \n\n" + ','.join(map(str, bins))
        print(message)
        #Env vars imported from Lambda come in as string rather than bool
        if NOTIFICATIONS_ENABLED == "true":
            publish(message)
    else:
        print('No bins for collection')
