#!/usr/bin/env python3
import pika, sys, os, json

from components.recent_objects_channel import RecentObjectsChannel

def main():
    print('🏃🏻‍♂️ Space Data Analyzer is Running..')
    RecentObjectsChannel()
        
if __name__ == '__main__':
    try:
      main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)