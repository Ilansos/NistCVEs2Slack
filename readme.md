# CVE Notification System

This Python script automates the process of fetching recent cybersecurity vulnerabilities from the National Vulnerability Database (NVD) and posting them into a Slack channel using a MicroK8s deployment with Docker. This documentation covers the entire setup, configuration, and usage of the script in a Kubernetes environment.

## System Requirements

- Docker
- MicroK8s
- Python 3.6 or higher
- requests library
- slack_sdk library

## Setting Up a Slack Bot

To use this script, you need to create a Slack bot and configure it with appropriate permissions. Follow these steps:
#### Creating a Bot

    Create an App: Go to Your Apps on Slack API and click "Create New App".
    Name Your App: Provide a name and select the workspace where you want the app.
    Add Features and Functionality: Go to "Bot Users" and add a new bot user.

#### Configuring Permissions

    Navigate to OAuth & Permissions: In the app settings.

    Add Scopes: Under "Scopes", add the following permissions:
        chat:write: To post messages in the channels.
        channels:read: To access channel information.
        files:write: To upload files/images (if using images in notifications).

    Install App to Workspace: Install the app in your Slack workspace.

#### Extracting the Channel ID

    Navigate to Slack: Open your Slack workspace.
    Find Your Channel: Go to the channel where you want notifications.
    Open Channel Details: Click on the channel name at the top to view details.
    Locate the Channel ID: Usually found in the URL or under "More" in the channel details.

## Getting Started

First, clone the repository to your local machine and change into the project directory:

```bash
git clone https://github.com/Ilansos/NistCVEs2Slack.git
cd NistCVEs2Slack
```

## Install Docker

Install Docker on your system by following the instructions on the official Docker website:
[Install Docker](https://docs.docker.com/get-docker/)

## Install MicroK8s

Install MicroK8s using the following command:

```bash
sudo snap install microk8s --classic
```

## Enable MicroK8s Addons

Enable necessary MicroK8s addons, including DNS and the registry:


```bash
sudo microk8s enable dns registry
```

## Create a Local Docker Registry

MicroK8s includes a built-in Docker registry where you can push your images. It is available at localhost:32000. Use this registry to manage local images.
Create Docker Image

#### Build the Docker image:

```bash
docker build -t localhost:32000/nist2slack:v1 .
```

#### Push the image to the local registry:

```bash
docker push localhost:32000/nist2slack:v1
```

## Kubernetes Deployment Configuration

Environmental variables are set directly in the deployment.yaml file. Modify the following section with your actual values:

```yaml
env:
- name: SLACK_API_KEY
  value: "YOUR SLACK API KEY"
- name: CHANNEL_ID
  value: "YOUR CHANNEL ID"
- name: IMAGE_URL
  value: "YOUR IMAGE ID"
```

## Deploy the Script

Deploy your application to MicroK8s by applying the Kubernetes deployment file:

```bash
microk8s kubectl apply -f deployment.yaml
```
### Verify the Deployment

Check the status of your deployment:
```bash
microk8s kubectl get all
```

Ensure that the pods are running without issues:

```bash
microk8s kubectl logs -f <pod-name>
```

## Automating the Script with Cron Job

This is handled within the Docker container using a cron job as defined in the Dockerfile and crontab.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### MIT License