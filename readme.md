# CVE Notification System

This Python script automates the process of fetching recent cybersecurity vulnerabilities from the National Vulnerability Database (NVD) and posting them into a Slack channel. This documentation covers the setup requirements, configuration, and usage of the script.
System Requirements

    Python 3.6 or higher
    requests library
    slack_sdk library

You can install the required libraries using pip:

```
pip install requests slack_sdk
```

## Configuration

The script depends on a configuration file named config.json placed in the same directory as the script. This JSON file should contain the following keys:

    slack_api_key: The Slack API token for authentication.
    channel_id: The ID of the Slack channel where notifications will be posted.
    image_url: URL of an image to display in Slack messages (optional).

### Sample config.json

```
{
  "slack_api_key": "xoxb-your-slack-api-key",
  "channel_id": "your-channel-id",
  "image_url": "https://example.com/image.png"
}
```
### Setting Up a Slack Bot

To use this script, you need to create a Slack bot and configure it with appropriate permissions. Follow these steps:
Creating a Bot

    Create an App: Go to Your Apps on Slack API and click "Create New App".
    Name Your App: Provide a name and select the workspace where you want the app.
    Add Features and Functionality: Go to "Bot Users" and add a new bot user.

Configuring Permissions

    Navigate to OAuth & Permissions: In the app settings.

    Add Scopes: Under "Scopes", add the following permissions:
        chat:write: To post messages in the channels.
        channels:read: To access channel information.
        files:write: To upload files/images (if using images in notifications).

    Install App to Workspace: Install the app in your Slack workspace.

Extracting the Channel ID

    Navigate to Slack: Open your Slack workspace.
    Find Your Channel: Go to the channel where you want notifications.
    Open Channel Details: Click on the channel name at the top to view details.
    Locate the Channel ID: Usually found in the URL or under "More" in the channel details.

### Usage

Once the configuration is set up, you can run the script using Python:

```
python nist2slack.py
```

Ensure that the script and config.json are in the same directory.
Logging

The script logs all its operations and errors into nist2slack.log. You can view this file to monitor activity or troubleshoot issues.

## Automating the Script with a Cron Job

To ensure that the CVE notification script runs once a day, you can set up a cron job on a Unix-like operating system. This will automatically execute the script at a specified time each day.

### Setting up a Cron Job

1. **Open the Terminal**.
2. **Edit the Crontab**: Enter `crontab -e` to edit the cron jobs for your user.
3. **Add a Cron Job**: You will need to specify the time you want the script to run and the path to the Python interpreter and the script. For example, to run the script every day at 7:00 AM, you might add the following line to your crontab:

```bash
0 7 * * * cd /path/to/script/folder/ && /usr/bin/python3 /path/to/nist2slack.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### MIT License

