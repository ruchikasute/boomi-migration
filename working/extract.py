# extract.py

import base64
import requests
import xml.etree.ElementTree as ET
import csv
import io

def build_auth_headers(username, password):
    auth_string = f"{username}:{password}"
    auth_token = base64.b64encode(auth_string.encode()).decode()
    return {
        "Authorization": f"Basic {auth_token}",
        "Accept": "application/xml"
    }

# extract.py

import base64
import requests
import xml.etree.ElementTree as ET
import csv
import io

# Build Boomi Basic Auth headers
def build_auth_headers(username, password):
    auth_string = f"{username}:{password}"
    auth_token = base64.b64encode(auth_string.encode()).decode()
    return {
        "Authorization": f"Basic {auth_token}",
        "Accept": "application/xml",
        "Content-Type": "application/xml"
    }

# Make POST request to Boomi /Process/query API
def fetch_processes(account_id, headers):
    url = f"https://api.boomi.com/api/rest/v1/{account_id}/Process/query"

    payload = """<?xml version="1.0" encoding="UTF-8"?>
<query xmlns="http://api.platform.boomi.com/">
    <filter>
        <expression operator="EQUALS" property="processType" value="EXECUTABLE"/>
    </filter>
</query>"""

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        print("❌ Status Code:", response.status_code)
        print("❌ Response Body:", response.text)
        raise e

# Parse XML response and extract process ID and name
def extract_process_list(xml_str):
    ns = {'bns': 'http://api.platform.boomi.com/'}
    root = ET.fromstring(xml_str)
    rows = []

    for proc in root.findall(".//bns:result", ns):
        proc_id = proc.attrib.get("id", "")
        name = proc.attrib.get("name", "")
        rows.append({"ID": proc_id, "Name": name})

    return rows

# Convert extracted data to CSV
def convert_to_csv(rows):
    output = io.StringIO()
    if not rows:
        return ""
    writer = csv.DictWriter(output, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()

# Optional: Render CSV data into HTML table for frontend
def csv_to_html_table(csv_data):
    lines = csv_data.strip().splitlines()
    if not lines:
        return "<p>No data</p>"

    headers = lines[0].split(",")
    html = "<table class='table table-bordered'><thead><tr>"
    html += "".join([f"<th>{h}</th>" for h in headers]) + "</tr></thead><tbody>"

    for row in lines[1:]:
        cells = row.split(",")
        html += "<tr>" + "".join([f"<td>{c}</td>" for c in cells]) + "</tr>"

    html += "</tbody></table>"
    return html


def extract_process_list(xml_str):
    root = ET.fromstring(xml_str)
    rows = []
    for proc in root.findall(".//process"):
        proc_id = proc.findtext("id")
        name = proc.findtext("name")
        rows.append({"ID": proc_id, "Name": name})
    return rows

def convert_to_csv(rows):
    output = io.StringIO()
    if not rows:
        return ""
    writer = csv.DictWriter(output, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()

def csv_to_html_table(csv_data):
    lines = csv_data.strip().splitlines()
    if not lines:
        return "<p>No data</p>"

    headers = lines[0].split(",")
    html = "<table class='table table-bordered'><thead><tr>"
    html += "".join([f"<th>{h}</th>" for h in headers]) + "</tr></thead><tbody>"

    for row in lines[1:]:
        cells = row.split(",")
        html += "<tr>" + "".join([f"<td>{c}</td>" for c in cells]) + "</tr>"

    html += "</tbody></table>"
    return html
