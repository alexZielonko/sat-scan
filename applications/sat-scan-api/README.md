# Sat-Scan-API

The Sat-Scan API provides an interface for the Data Analyzer and Sat Scan Web applications to create, access, and update persisted data.

## Endpoints

The following endpoints are currently available:

| GET    | /space-objects                  | Returns a list of space objects  |
| ------ | ------------------------------- | -------------------------------- |
| GET    | /space-object/:space_object_id  | Returns a single space object    |
| POST   | /space-objects                  | Creates a space object           |
| PUT    | /space-objects                  | Updates an existing space object |
| DELETE | /space-objects/:space_object_id | Deletes a single space object    |

## Local Development

This application can be ran alongside the rest of the Sat Scan backend system using Docker Compose.

This application requires initial setup to run locally. Follow the [initial setup instructions](../../README.md#initial-local-development-setup) in the project's root readme file to get started.

## Production Infrastructure & Continuous Delivery

The Sat Scan Database exists within a private subnet in the virtual private cloud (VPC), and it only accepts ingress from traffic within the VPC. This networking decision helps prevent the database from direct exposure to the public internet, which improves the system's security posture.

As with all of Sat Scan's production backend components and applications, all of the infrastructure and networking for the Sat Scan API is provisioned using Terraform. 

Like the Data Analyzer, the API runs using Amazon Elastic Container Service (ECS) using Amazon Fargate. The continuous integration and deployment process for the API mirrors that of the Data Analyzer.

## Endpoint Security

The API provides public GET request access without any authorization required.

The API limits requests to create, update, or delete records by requiring an API key in the the request header's bearer token.

```js
headers: {
    'Authorization': `Bearer ${API_KEY}`
}
```

Requests to create, update, or delete a resource will be rejected with a `401: Unauthorized` status if they lack an authorization header or include an invalid bearer token.
