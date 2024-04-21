import requests
from datetime import datetime, timedelta
import logging
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(filename='nist2slack.log', 
                    filemode='a', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# Get the logger instance
logger = logging.getLogger(__name__)

def read_config(filename):
    try:
        with open(filename, 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        logging.error(f"Config file '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON file: {filename}")
        return None

def response_parsing(data):
    vulnerabilities = data.get("vulnerabilities")
    cves_information = []
    for vuln in vulnerabilities:
        cve = vuln.get("cve")
        id = cve.get("id")
        source = cve.get("sourceIdentifier")
        published = cve.get("published")
        description = cve.get("descriptions")
        for desc in description:
            lang = desc.get("lang")
            try:
                if lang == "en":
                    description_english = desc.get("value")
                    break
            except:
                description_english = None
        try:
            metrics = cve.get("metrics")
        except:
            metrics = None
        try:
            cvssMetricV31 = metrics.get("cvssMetricV31")
            exploitabilityScore = cvssMetricV31[0].get("exploitabilityScore")
            impactScore = cvssMetricV31[0].get("impactScore")
        except:
            exploitabilityScore = None
            impactScore = None
        try:
            references = cve.get("references")
        except:
            references = None

        cve_info = {"CVE": id, "source": source, "published_at": published, "description": description_english, "exploitabilityScore": exploitabilityScore, "impactScore": impactScore, "references": references}
        cves_information.append(cve_info)
    return cves_information



def fetch_cves(severity_levels, pub_start_date, pub_end_date):
    base_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
    cves_high = []
    cves_medium = []
    cves_critical = []

    for severity in severity_levels:
        params = {
            'cvssV3Severity': severity,
            'pubStartDate': pub_start_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'),  # Corrected format
            'pubEndDate': pub_end_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'),  # Corrected format
            'resultsPerPage': 50  # Adjust as needed
        }

        # Using PreparedRequest to print the full URL
        req = requests.Request('GET', base_url, params=params)
        prepared = req.prepare()

        # Send the request
        with requests.Session() as session:
            response = session.send(prepared)
            if response.status_code == 200:
                data = response.json()
                cves_information = response_parsing(data)
                if severity == "MEDIUM":
                    cves_medium.extend(cves_information)
                elif severity == "HIGH":
                    cves_high.extend(cves_information)
                else:
                    cves_critical.extend(cves_information)
            else:
                logger.error(f"Failed to retrieve {severity} severity CVEs: {response.status_code}")
                logger.error("Response:", response.text)

    logger.info(f"Number of critical CVEs: {len(cves_critical)}")
    logger.info(f"Number of high CVEs: {len(cves_high)}")
    logger.info(f"Number of medium CVEs: {len(cves_medium)}")
    return cves_medium, cves_high, cves_critical


def create_slack_message(cve_info, severity):
    config = read_config("config.json")
    image_url = config.get("image_url")
    # Map severity to emojis for visual representation
    severity_emojis = {
        'MEDIUM': ':large_yellow_circle:',
        'HIGH': ':large_orange_circle:',
        'CRITICAL': ':red_circle:'
    }
    emoji = severity_emojis.get(severity.upper(), ':white_circle:')  # Default to white circle if unknown severity

    text_summary = f"{emoji} CVE ID: {cve_info['CVE']} - {cve_info['description'][:75]}..."  # Summary for notifications
    
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*_New {severity} Vulnerability {emoji}_*\n\n"
                    f"*CVE ID:* {cve_info['CVE']}\n"
                    f"*Source:* {cve_info['source']}\n"
                    f"*Published At:* {cve_info['published_at']}\n"
                    f"*Description:* {cve_info['description']}\n"
                    f"*Exploitability Score:* {cve_info['exploitabilityScore']}\n"
                    f"*Impact Score:* {cve_info['impactScore']}\n"
                )
            },
            "accessory": {
                "type": "image",
                "image_url": image_url,
                "alt_text": "CVE details"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "\n".join(f"<{ref['url']}|Reference>" for ref in cve_info['references'])
                }
            ]
        },
        {
            "type": "divider"
        }
    ]
    return text_summary, blocks

def send_cve_notifications(cves, severity, client):
    config = read_config("config.json")
    channel_id = config.get("channel_id")
    try:
        for cve in cves:
            text_summary, message_blocks = create_slack_message(cve, severity)
            response = client.chat_postMessage(
                channel=channel_id, 
                text=text_summary,  # Fallback text for notifications
                blocks=json.dumps(message_blocks)
            )
            logger.info("successfully posted CVE into Slack channel")

    except SlackApiError as e:
        logger.error(f"Error posting to Slack: {e}")
       

def main():
    config = read_config("config.json")
    slack_api_key = config.get("slack_api_key")
    # Define the time range for the last 24 hours
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=1)

    # Define severity levels to fetch
    severity_levels = ['MEDIUM', 'HIGH', 'CRITICAL']

    # Fetch CVEs
    cves_medium, cves_high, cves_critical = fetch_cves(severity_levels, start_date, end_date)

    # Slack client initialization
    client = WebClient(token=slack_api_key)


    send_cve_notifications(cves_medium, 'MEDIUM', client)
    send_cve_notifications(cves_high, 'HIGH', client)
    send_cve_notifications(cves_critical, 'CRITICAL', client)

if __name__ == "__main__":
    main()