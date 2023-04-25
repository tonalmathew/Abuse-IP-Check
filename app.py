from flask import Flask, render_template, request, url_for
import json
import requests

app = Flask(__name__,template_folder='template')

# API key for AbuseIPDB
API_KEY = ''  # Replace with your actual API key

# Home page route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the IP address from the form
        ip_address = request.form['ip_address']

        # Perform IP reputation check using AbuseIPDB API
        url = 'https://api.abuseipdb.com/api/v2/check'

        querystring = {
            'ipAddress': ip_address,
            'maxAgeInDays': '90'
        }

        headers = {
            'Accept': 'application/json',
            'Key': API_KEY
        }

        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        data = response.json()

        # Extract relevant information from the API response
        if 'data' in data and 'abuseConfidenceScore' in data['data']:
            confidence_score = data['data']['abuseConfidenceScore']
            ipAddress = data['data']['ipAddress']
            country = data['data']['countryCode']
            isPublic = data['data']['isPublic']
            isp = data['data']['isp']
            domain = data['data']['domain']
            isWhitelisted = data['data']['isWhitelisted']
            usageType = data['data']['usageType']
            isTor = data['data']['isTor']
            totalReports = data['data']['totalReports']
            numDistinctUsers = data['data']['numDistinctUsers']
            lastReportedAt = data['data']['lastReportedAt']
            return render_template('index.html', ipAddress=ipAddress, isPublic=isPublic, isWhitelisted=isWhitelisted, lastReportedAt=lastReportedAt, numDistinctUsers=numDistinctUsers, totalReports=totalReports, isTor=isTor, usageType=usageType, confidence_score=confidence_score, country=country, isp=isp, domain=domain)
        else:
            error = 'Unable to retrieve IP reputation information. Please try again later.'
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
