#!/usr/bin/env python3

from flask import Flask

from app.channels.recent_objects_channel import RecentObjectsChannel
from app.config_parsers.credentials import Credentials

app = Flask(__name__)

@app.route('/health-check')
def health_check():
  return 'Success', 200

print('🏃🏻‍♂️ Space Data Analyzer is Running..')
# sat_scan_api_key = Credentials().sat_scan_api_key
# RecentObjectsChannel(sat_scan_api_key=sat_scan_api_key)