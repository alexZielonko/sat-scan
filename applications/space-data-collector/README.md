# Space-Data-Collector

This application periodically pulls satellite data from external APIs and publishes it to a messaging queue for downstream processing.

> [!TIP]
> For more information on the Data Collector, see this project's [report documentation](../../report//final-report.md#data-collector)

## Local Development

This application can be ran alongside the rest of the Sat Scan backend system using Docker Compose.

This application requires initial setup to run locally. Follow the [initial setup instructions](../../README.md#initial-local-development-setup) in the project's root readme file to get started.

## Adding New Space-Track.org Requests

Edit [space_track_requests.yml](function/components/space_track_requests.yml) to add new requests for publication by the message queue.

Additional information on extending this configuration file can be found in the [report documentation](../../report//final-report.md#data-collector).


  