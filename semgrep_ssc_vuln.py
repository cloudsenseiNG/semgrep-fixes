import requests

count = 0

deployment_id = ""

url = f"https://semgrep.dev/api/v1/deployments/{deployment_id}/ssc-vulns"

payload = {
    "pageSize": 100,
    "exposure": ["REACHABLE"]
}

token = ""

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    # Print the response data
    data = response.json()
else:
    # Print an error message if the request failed
    print("Error:", response.text)

for vuln in data['vulns']:
    if 'title' in vuln:
        count += 1

print("Total number of titles:", count)