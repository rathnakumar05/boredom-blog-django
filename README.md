# Boredom Blog App

Boredom is a simple blog app that uses Docker Compose to set up both development and production environments with Django, Apache, MySQL, and MongoDB.

## Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

## Getting Started

1. Clone the Boredom repository:

```shell
git clone <repository_url>
cd <repository_directory>
```

2. Add your third-party email service credentials:
Edit the docker-compose.yml file and replace the following environment variables under the web service with your email service credentials:

```shell
- EMAIL_HOST_USER=<your_email_username>
- EMAIL_HOST_PASSWORD=<your_email_password>
- EMAIL_HOST=<your_email_host>
```

3. Build and start the Docker containers:

```shell
docker-compose up --build
```

4. Access the Boredom blog app:
Open your web browser and visit http://localhost.

Stopping the Application
To stop the Docker containers, use the following command:

```shell
docker-compose down
```

That's it! You now have the basic steps to get started with running your Boredom blog app using Docker Compose. Feel free to customize the instructions based on your specific requirements.
