#!/usr/bin/env python3

from flask import Flask

from channels.recent_objects_channel import RecentObjectsChannel
from config_parsers.credentials import Credentials
from config_parsers.route_config import RouteConfig


if __name__ == "__main__":
    print("👉 Space Data Analyzer starting (🚀)")

    app = Flask(__name__)


    @app.route("/health-check")
    def health_check():
        return "Success", 200


    print("🏃🏻‍♂️ Space Data Analyzer is Running..")

    sat_scan_api_key = Credentials().sat_scan_api_key

    channel = RecentObjectsChannel(
        sat_scan_api_key=sat_scan_api_key, route_config=RouteConfig()
    )

    channel.start()

    app.run(host="0.0.0.0", port=8000, debug=True)
