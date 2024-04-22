#!/bin/bash

# Docker Snippets Collection: Comprehensive Guide

##### Creating and Managing Dockerfiles #####

# Create a Dockerfile
echo "FROM ubuntu:latest
RUN apt-get update && apt-get install -y nginx
CMD ['nginx', '-g', 'daemon off;']" > Dockerfile

# Create a dependencies file
echo "express
lodash" > dependencies.txt

##### Building and Running Containers #####

# Build an image from a Dockerfile (current directory)
docker build -t my_repo/my_image .

# Run a container in detached mode, exposing ports
docker run -d --name my_container -p 8000:80 my_repo/my_image

# Execute a command inside a running container
docker exec -it my_container bash

##### Image Management #####

# List, remove, and tag images
docker images
docker rmi my_repo/my_image
docker tag my_image my_dockerhub_username/my_image:tag

# Push an image to Docker Hub
docker push my_dockerhub_username/my_image:tag

##### Docker Compose #####

# Create docker-compose.yml and manage services
echo "version: '3'
services:
  web:
    image: nginx
    ports:
     - '80:80'
  app:
    image: my_repo/my_image
    volumes:
     - ./app:/app" > docker-compose.yml
docker-compose up -d
docker-compose down

##### Container Lifecycle Management #####

# List, stop, start, and remove containers
docker ps -a
docker stop my_container
docker start my_container
docker rm my_container

##### Docker Hub and Webhooks #####

# Login and logout from Docker Hub
docker login
docker logout

##### Networking and Volume Management #####

# Create and manage networks and volumes
docker network create my_network
docker volume create my_volume
docker run -d --name my_container -v my_volume:/app my_repo/my_image

##### Cleanup Commands #####

# Remove unused resources
docker image prune -a
docker container prune
docker network prune
docker volume prune

##### GitHub Integration and CI/CD Automation #####

# Example for setting up a GitHub Actions workflow for Docker
echo "name: Build and Push Docker image

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build the Docker image
      run: docker build . --file Dockerfile --tag your_username/your_repo:$(date +%s)
    - name: Log in to Docker Hub
      uses: docker/login-action@v1
      with:
        username: your_username
        password: ${{ secrets.DOCKER_PASSWORD }}
    - name: Push the Docker image
      run: docker push your_username/your_repo:$(date +%s)" > .github/workflows/dockerimage.yml

##### Advanced Image and Container Management #####

# Search for images, save/load images, restart containers, update containers
docker search ubuntu
docker save your_username/your_repo | gzip > your_repo.tar.gz
docker load < my_repo.tar.gz
docker run -d --restart unless-stopped --name your_container your_username/your_repo

##### Remote Management and SSL Setup #####

# Remote management via SSH (example command)
ssh your_remote_machine_ip 'docker ps'

# Install Certbot for Let's Encrypt SSL certificates
sudo apt-get update
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com

##### Adding Dependencies for Popular Frameworks/Languages #####

# Python with Flask
echo "FROM python:3.8
RUN pip install flask gunicorn
COPY ./app /app
WORKDIR /app
CMD ['gunicorn', '-b', '0.0.0.0:80', 'app:app']" > Dockerfile

# Node.js with Express
echo "FROM node:14
RUN npm install express
COPY . /app
WORKDIR /app
CMD ['node', 'app.js']" > Dockerfile

# PHP with Laravel
echo "FROM php:7.4-fpm
RUN apt-get update && apt-get install -y libpq-dev && docker-php-ext-install pdo pdo_pgsql
COPY . /var/www/html
WORKDIR /var/www/html
RUN curl -sS https://getcomposer.org/installer | php
RUN php composer.phar install
CMD ['php', 'artisan', 'serve', '--host', '0.0.0.0', '--port', '80']" > Dockerfile

##### Free Hosting Services Without Time-Based Usage Limits #####

# Deployment examples for Google Cloud Run and AWS ECS (refer to their CLI documentation for specific commands)

##### Note #####
# This script serves as a guideline. Adjustments may be required based on specific project needs or platform updates.

# Docker Snippets Collection Part 2: Leveraging Free Services

##### Deploying to Free Cloud Services #####

# Note: The following commands are examples and require respective CLI tools installed and configured.

### Google Cloud Run Deployment (Always Free tier limits apply) ###

# Deploy a container to Google Cloud Run
gcloud run deploy your-service --image gcr.io/your-project-id/your-image --platform managed --region your-region --allow-unauthenticated

### AWS ECS Fargate Deployment (AWS Free Tier limits apply) ###

# Create an ECS Task Definition from a JSON file
aws ecs register-task-definition --cli-input-json file://your-task-definition.json

# Create an ECS service using the created task definition
aws ecs create-service --cluster your-cluster-name --service-name your-service-name --task-definition your-task-family-name --desired-count 1 --launch-type FARGATE

### Azure Container Instances (ACI) Deployment (Azure Free Account options) ###

# Create a container instance in Azure Container Instances
az container create --resource-group yourResourceGroup --name yourContainerName --image yourImageName --dns-name-label yourDnsNameLabel --ports 80

##### CI/CD with GitHub Actions for Docker #####

# Example GitHub Action to build and push Docker images to Docker Hub and deploy to a cloud service

echo "name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Log in to Docker Hub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKER_HUB_USERNAME }}
        password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
    - name: Build and push Docker image
      uses: docker/build-push-action@v2
      with:
        push: true
        tags: yourusername/yourimagename:latest
  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to Cloud Run
      env:
        GCP_PROJECT: ${{ secrets.GCP_PROJECT }}
        GCP_SA_KEY: ${{ secrets.GCP_SA_KEY }}
      run: |
        echo "$GCP_SA_KEY" | gcloud auth activate-service-account --key-file=-
        gcloud run deploy your-service --image gcr.io/$GCP_PROJECT/yourimagename --platform managed --region your-region --allow-unauthenticated" > .github/workflows/cicd_pipeline.yml

##### Setting Up SSL with Let's Encrypt for Dockerized Applications #####

# Using Certbot with nginx Docker container
# Note: This requires your DNS to be properly configured to point to your server

echo "version: '3'
services:
  web:
    image: nginx
    ports:
     - '80:80'
     - '443:443'
    volumes:
     - ./nginx.conf:/etc/nginx/nginx.conf
     - ./data/certbot/conf:/etc/letsencrypt
     - ./data/certbot/www:/var/www/certbot
  certbot:
    image: certbot/certbot
    volumes:
     - ./data/certbot/conf:/etc/letsencrypt
     - ./data/certbot/www:/var/www/certbot
    entrypoint: '/bin/sh -c "trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;"'" > docker-compose.yml

# Ensure you have an nginx.conf configured for HTTPS and the Certbot challenge

##### Using Docker in Development With Live Reloading #####

# Example with Node.js using nodemon
echo "FROM node:14
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
CMD ['nodemon', 'src/app.js']" > Dockerfile

# Example Docker Compose for development with live reloading
echo "version: '3'
services:
  app:
    build: .
    command: nodemon src/app.js
    volumes:
      - .:/usr/src/app
      - /usr/src/app/node_modules
    ports:
      - '3000:3000'
    environment:
      NODE_ENV: development" > docker-compose.yml
#!/bin/bash

# Advanced Docker Snippets Collection: Deployment, Backup, and Security

##### Backup Docker Volumes #####

# Backup a Docker volume to a local tar.gz file
docker run --rm -v your_volume:/volume -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /volume ./

# Restore Docker volume from a backup tar.gz file
docker run --rm -v your_volume:/volume -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /volume

##### Deploying to Vercel #####

# Note: Install Vercel CLI globally with npm install -g vercel if not already installed

# Deploying a static site or Node.js project to Vercel
vercel deploy --prod

##### Deploying to OnRender.com #####

# Note: Install Render CLI with npm install -g render-cli if not already installed

# Login to Render
render login

# Deploy a service to Render using render.yaml
# Ensure you have a render.yaml file configured with your service details
render deploy --file render.yaml

##### Deploying Python Applications #####

# Example Dockerfile for a Python (Flask) application
echo "FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ['gunicorn', '--bind', '0.0.0.0:80', 'app:app']" > Dockerfile

# Build and run the Docker container
docker build -t python-app .
docker run -d --name python-app-container -p 80:80 python-app

##### Exposing Services on Specific Ports with SSL (without a domain) #####

# Setting up SSL for services without a domain is challenging as Let's Encrypt requires a domain for issuing certificates. A workaround is to use a service like ngrok or localtunnel, which provides a temporary public URL.

# Using ngrok as an example (Install ngrok from https://ngrok.com/download)

# Expose your service running on localhost
./ngrok http 80

# Ngrok will provide a public HTTPS URL which you can use to access your service securely from anywhere.

##### Note on SSL without a Domain #####

# For a permanent solution without a domain, consider acquiring a domain or using dynamic DNS services that offer free subdomains. This allows you to use Let's Encrypt for a real SSL certificate. Services like DuckDNS (duckdns.org) provide a way to update DNS records dynamically, enabling the use of Let's Encrypt with your subdomain.

##### Additional Tips #####

# These snippets are designed to provide a starting point for various Docker-related tasks including deployment, backups, and handling SSL certificates. Due to the complexity of some scenarios, especially around SSL without a domain, further research and configuration might be necessary to tailor these solutions to your specific needs.
#!/bin/bash

# GitHub Integration and CI/CD Automation

# This script sets up a GitHub Actions workflow for Docker.
# It builds and pushes Docker images to Docker Hub on each push to the main branch.

echo "name: Build and Push Docker image

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build the Docker image
      run: docker build . --file Dockerfile --tag your_username/your_repo:$(date +%s)
    - name: Log in to Docker Hub
      uses: docker/login-action@v1
      with:
        username: your_username
        password: ${{ secrets.DOCKER_PASSWORD }}
    - name: Push the Docker image
      run: docker push your_username/your_repo:$(date +%s)" > .github/workflows/dockerimage.yml

# Advanced Image and Container Management

# This section includes commands for searching Docker images, saving/loading images, and managing containers.

# Search for images
docker search ubuntu

# Save and load images
docker save your_username/your_repo | gzip > your_repo.tar.gz
docker load < my_repo.tar.gz

# Run a container with restart policy
docker run -d --restart unless-stopped --name your_container your_username/your_repo

# Remote Management and SSL Setup

# This section includes commands for remote management via SSH and installing Certbot for Let's Encrypt SSL certificates.

# Remote management via SSH
ssh your_remote_machine_ip 'docker ps'

# Install Certbot for Let's Encrypt SSL certificates
sudo apt-get update
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Adding Dependencies for Popular Frameworks/Languages

# This section includes Dockerfile examples for Python with Flask, Node.js with Express, and PHP with Laravel.

# Python with Flask
echo "FROM python:3.8
RUN pip install flask gunicorn
COPY ./app /app
WORKDIR /app
CMD ['gunicorn', '-b', '0.0.0.0:80', 'app:app']" > Dockerfile

# Node.js with Express
echo "FROM node:14
RUN npm install express
COPY . /app
WORKDIR /app
CMD ['node', 'app.js']" > Dockerfile

# PHP with Laravel
echo "FROM php:7.4-fpm
RUN apt-get update && apt-get install -y libpq-dev && docker-php-ext-install pdo pdo_pgsql
COPY . /var/www/html
WORKDIR /var/www/html
RUN curl -sS https://getcomposer.org/installer | php
RUN php composer.phar install
CMD ['php', 'artisan', 'serve', '--host', '0.0.0.0', '--port', '80']" > Dockerfile
#!/bin/bash

# Free Hosting Services Without Time-Based Usage Limits

# This section includes deployment examples for Google Cloud Run and AWS ECS.

# Backup Docker Volumes

# This section includes commands for backing up and restoring Docker volumes.

# Backup a Docker volume to a local tar.gz file
docker run --rm -v your_volume:/volume -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /volume ./

# Restore Docker volume from a backup tar.gz file
docker run --rm -v your_volume:/volume -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /volume

# Deploying to Vercel

# Deploying a static site or Node.js project to Vercel

# Note: Install Vercel CLI globally with npm install -g vercel if not already installed

# Log in to Vercel CLI (if not already logged in)
vercel login

# Deploy your project to Vercel with the following command:
vercel deploy --prod

# Deploying to OnRender.com

# Deploying a service to Render using render.yaml

# Note: Install Render CLI with npm install -g render-cli if not already installed

# Log in to Render CLI (if not already logged in)
render login

# Create a render.yaml file with the following content, replacing placeholders with your actual project details:
echo "services:
  - name: your-service-name
    github:
      repo: your-github-repo
      branch: main
    buildCommand: your-build-command
    startCommand: your-start-command" > render.yaml

# Deploy your service to Render using the render.yaml file:
render deploy --file render.yaml

# Deploying Python Applications

# Example Dockerfile for a Python (Flask) application
echo "FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ['gunicorn', '--bind', '0.0.0.0:80', 'app:app']" > Dockerfile

# Build the Docker image for your Python application:
docker build -t python-app .

# Run the Docker container:
docker run -d --name python-app-container -p 80:80 python-app

# Exposing Services on Specific Ports with SSL (without a domain)

# Setting up SSL for services without a domain using ngrok

# Note: Install ngrok from https://ngrok.com/download

# After installing ngrok, you can expose your service running on localhost to the public internet with HTTPS.

# Navigate to the directory where ngrok is installed in the terminal.

# Expose your service running on localhost (replace 80 with the port your service is running on):
./ngrok http 80

# Note on SSL without a Domain

# For a permanent solution without a domain, consider acquiring a domain or using dynamic DNS services that offer free subdomains. This allows you to use Let's Encrypt for a real SSL certificate. Services like DuckDNS (duckdns.org) provide a way to update DNS records dynamically, enabling the use of Let's Encrypt with your subdomain.

# Additional Tips

#!/bin/bash

# Deploying to OnRender.com

# Deploying a service to Render using render.yaml

# Note: Install Render CLI with npm install -g render-cli if not already installed

# Log in to Render CLI (if not already logged in)
render login

# Create a render.yaml file with the following content, replacing placeholders with your actual project details:
echo "services:
  - name: your-service-name
    github:
      repo: your-github-repo
      branch: main
    buildCommand: your-build-command
    startCommand: your-start-command" > render.yaml

# Deploy your service to Render using the render.yaml file:
render deploy --file render.yaml

# For redeploying or making changes to the deployment:

# After making changes to your project, such as updating code or configurations, you can redeploy to Render using the render.yaml file.

# Ensure you have already logged in to Render CLI.

# Update the render.yaml file with your changes.

# Re-deploy your service to Render:
render deploy --file render.yaml

# To edit the URL or other settings of your Render service:

# Log in to the Render web dashboard at https://dashboard.render.com/.

# Navigate to your service.

# In the service settings, you can edit various configurations, including the URL, environment variables, and scaling options.
