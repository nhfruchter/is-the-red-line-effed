import requests
import json
from datetime import datetime,timedelta

class T(object):
    ENDPOINT = "http://realtime.mbta.com/developer/api/v2/{apicall}"

    def __init__(self, api_key, response_format='json'):
        if api_key == "YOUR API KEY HERE" or api_key.strip() == "":
            raise ValueError("Fill in a real API key.")
            
        self.api_key = api_key
        self.response_format = response_format
        
    def _call(self, apicall, params=dict(), raw=False):
        params['api_key'] = self.api_key
        params['format'] = self.response_format
        url = self.ENDPOINT.format(apicall=apicall)

        response = requests.get(url, params=params)
        if raw:
            return response.content
        else:
            return response.json() 
            
        