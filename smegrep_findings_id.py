import requests

SEMGREP_APP_TOKEN = ""

deployment_slug = ""

url = f"https://semgrep.dev/api/v1/deployments/{deployment_slug}/findings"

count = 0

finding_ids = []

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SEMGREP_APP_TOKEN}"
}

response = requests.get(url, headers=headers)

data = response.json()["findings"]

# print(json.dumps(data, indent=4))

for i in data:
    if i["ref"] == "gitlab-mr":
        finding_ids.append(i["id"])
        count += 1
    
print(len(finding_ids))
print(count)    
