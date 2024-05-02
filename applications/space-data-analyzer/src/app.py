#!/usr/bin/env python3
import sys, os

from channels.recent_objects_channel import RecentObjectsChannel
from components.secret_manager import SecretManager

def main():
    print('🏃🏻‍♂️ Space Data Analyzer is Running..')
    secret_manager = SecretManager()
    RecentObjectsChannel(sat_scan_api_key=secret_manager.sat_scan_api_key)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)