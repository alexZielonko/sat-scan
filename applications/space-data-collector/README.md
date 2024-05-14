# Space-Data-Collector

This application periodically pulls satellite data from external APIs and publishes it to a messaging queue for downstream processing.

## TODO

- Note example.credentials.ini
- Detail how to add data sources / new space track api requests

## Data Sources

Edit `space-data-collector/function/components/space_track_requests.yml` to add new requests for publication by the message queue.

- [Space Track API](https://www.space-track.org/documentation#api)
  

## Creating/Starting the Virtual Environment

[Docs](https://docs.python.org/3/tutorial/venv.html)

```
python3 -m venv .venv
source .venv/bin/activate
```

### Installing Packages

```
pip3 install -r requirements.txt
```

## Create / Update Dependencies

```
pip3 freeze > requirements.txt
```