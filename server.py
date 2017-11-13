import requests
import mbta_api
import data as mappings
import os
from flask import Flask, request, render_template
from flask_json import FlaskJSON, JsonError, json_response, as_json
from datetime import datetime, timedelta
from memoize import *

app = Flask(__name__)
FlaskJSON(app)
T = mbta_api.T(os.environ['MBTA_KEY'])
@memoize_with_expiry(60)
def _rl_status(route='Red'):
    # Get alerts
    alerts = T._call('alertsbyroute', params={'route': route, 'include_access_alerts': False})
    
    if alerts.get('error'):
        result = alerts.get('error')
        result['status'] = 0
        return result
                
    # Create alert summary
    data = [{'text': a.get('short_header_text'),
         'severity': a.get('severity'),
         'effect': a.get('effect_name'), 
         'cause': a.get('cause_name'), 
         'last_modified': datetime.fromtimestamp(float(a.get('last_modified_dt'))),
         'id': a['alert_id']} 
         for a in alerts['alerts']]
         
    # Filter out: station issues
    alerts = [alert for alert in data if alert['effect'] != 'Station Issue']
    # Filter out: construction caused delays
    delay = 'Delay' in [a['effect'] for a in alerts if a['cause'] != 'construction']
    
    # Unspecified non-delay alerts
    maybe = len([a for a in alerts if a['effect'] != 'Shuttle'])

    # Delays = bad
    if delay:
        status = 2
    # Unspecified alerts but not delays = meh
    elif maybe and not delay:
        status = 1
    # All good
    else:
        status = 0    

    result = {
        'alerts': alerts,
        'status': status,
        'name': mappings.names(route),
        'color': mappings.colors(route)
    }
    return result

@app.route('/api/<route>')
@as_json
def api(route):
    return _rl_status(route)
    
@app.route('/')
def itrlft():
    data = _rl_status()
    return render_template('itrlft.html', data=data)

@app.route('/chooser')
def chooser():
    return render_template('chooser.html', routes=mappings.routenames)
    
@app.route('/route/<route>')
def other_route(route):
    data = _rl_status(route=route)
    return render_template('other.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
