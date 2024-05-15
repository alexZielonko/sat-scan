#!/usr/bin/env python3

from flask import Flask

from components.channels.recent_objects_channel import RecentObjectsChannel
from components.config_parsers.credentials import Credentials
from components.config_parsers.route_config import RouteConfig


if __name__ == "__main__":
    print("👉 Space Data Analyzer starting (🚀)")

    sat_scan_api_key = Credentials().sat_scan_api_key

    channel = RecentObjectsChannel(
        sat_scan_api_key=sat_scan_api_key, route_config=RouteConfig()
    )

    channel.start()

    app = Flask(__name__)

    @app.route("/health-check")
    def health_check():
        return "Success", 200

    app.run(host="0.0.0.0", port=8000, debug=True)
    print("🏃🏻‍♂️ Space Data Analyzer is Running..")