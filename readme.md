# NistCVE2Slack: CVE Notification System

This Python script automates the process of fetching recent cybersecurity vulnerabilities from the National Vulnerability Database (NVD) and posting them into a Slack channel.

## How It Works

The script is designed to run once a day as a Kubernetes CronJob, ensuring that it fetches and delivers up-to-date information about new vulnerabilities in a timely manner. Here's how it operates:

  1- Kubernetes CronJob Setup: The script is deployed to a Kubernetes cluster, which is configured to trigger its execution daily using a CronJob. This automates the process, minimizing manual intervention and ensuring daily updates.

  2- Fetching CVEs: When triggered, the script queries the NIST API for CVEs reported within the last 24 hours, categorized by severity levels such as "Medium," "High," and "Critical."

  3- Slack Notification: The script formats the CVE information and posts it into a specified Slack channel, making the information easily accessible to the team for quick review and action.

  4- Logs: Logging is integrated into the script to track its execution, including API response statuses, any CVEs found, and the success or failure of sending notifications to Slack.

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
    Find Your Channel: Go to the channel where you want notifications.sud
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

## Using the Local Docker Registry

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

## Creating Kubernetes Secrets

To manage sensitive information securely, store it as Kubernetes Secrets:

  1- Base64 Encode the Values:Before creating the secrets, encode the values you want to store in Base64 format. For example:
```bash
echo -n "YOUR SLACK API KEY" | base64
echo -n "YOUR CHANNEL ID" | base64
echo -n "YOUR IMAGE URL" | base64
```

  2- Define the Secret in the secrets.yaml File replacing the placeholders with the actual Base64-encoded strings:
```yaml
apiVersion: v1
kind: Secret
metadata:
    name: nist2slack-secrets
data:
    SLACK_API_KEY: "BASE64_ENCODED_SLACK_API_KEY"
    CHANNEL_ID: "BASE64_ENCODED_CHANNEL_ID"
    IMAGE_URL: "BASE64_ENCODED_IMAGE_URL"
```  

  3- Apply the Secret to the Kubernetes Cluster:
```bash
microk8s kubectl apply -f secrets.yaml
```

## Deploy the Script

Deploy your application to MicroK8s by applying the Kubernetes deployment file:

```bash
microk8s kubectl apply -f cronjob.yaml
```
### Verify the CronJob Deployment

Check the status of your CronJob:
```bash
microk8s kubectl get cronjobs
```

Find the last job:
```bash
microk8s kubectl get jobs
```

Find the pod executed by the job:
``` bash
kubectl get pods --selector=job-name=<last-job>
```

View logs of the last executed pod:

```bash
microk8s kubectl logs <pod-name>
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### MIT License