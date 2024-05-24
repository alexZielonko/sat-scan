# Space-Data-Analyzer

At it's core, the Data Analyzer consumes messages from the broker, normalizes them, and saves them in the database via the Sat Scan API.

The Data Analyzer consumes raw messages from the RabbitMQ broker. When a new message is received, it normalizes the message contents by converting it to a standard data structure. This helps ensure data integrity for downstream consumers and aligns the space object data with the schema required by the Sat Scan API.

> [!TIP]
> For more information on the Data Analyzer, see this project's [report documentation](../../report//final-report.md#data-analyzer)

## Local Development

This application can be ran alongside the rest of the Sat Scan backend system using Docker Compose.

This application requires initial setup to run locally. Follow the [initial setup instructions](../../README.md#initial-local-development-setup) in the project's root readme file to get started.
