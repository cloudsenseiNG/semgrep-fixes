# Importing required libraries
import requests
import os
import re

# Retrieving authentication tokens from environment variables
GITHUB_AUTH_TOKEN = os.getenv("GITHUB_AUTH_TOKEN")
SEMGREP_APP_TOKEN = os.getenv("SEMGREP_APP_TOKEN")

def get_paginated_data(url, github_token):
    next_pattern = r'(?<=<)([\S]*)(?=>; rel="next")'
    pages_remaining = True
    data = []

    while pages_remaining:

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28"
            }
        
        response = requests.get(url, params={"per_page": 100}, headers=headers)
        response_data = response.json()

        parsed_data = parse_data(response_data)
        data.extend(parsed_data)

        link_header = response.headers.get("link")

        pages_remaining = link_header and "rel=\"next\"" in link_header

        if pages_remaining:
            next_url_match = re.search(next_pattern, link_header)
            if next_url_match:
                url = next_url_match.group(0)

    return data

def parse_data(data):
    if isinstance(data, list):
        return data

    if not data:
        return []

    del data["incomplete_results"]
    del data["repository_selection"]
    del data["total_count"]

    namespace_key = list(data.keys())[0]
    data = data[namespace_key]

    return data

# Function to retrieve archived repositories from GitHub
def get_archived_repos(data):

    repos = data
    
    # Extracting archived repository names
    archived_repos = [repo["full_name"] for repo in repos if repo.get("archived")]
    
    print(f"GitHub Archived Repos: {archived_repos}")
    return archived_repos
    
# Function to retrieve all projects from SEMGREP
def get_all_projects(archived_repos, semgrep_token):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {semgrep_token}"
    }
    page = 0
    deployment_slug = "bodlexnig_personal_org"
    url = f"https://semgrep.dev/api/v1/deployments/{deployment_slug}/projects"
    
    # Sending GET request to SEMGREP API to retrieve projects
    response = requests.get(url, params={"page": {page}}, headers=headers)
    
    # Parsing response JSON data
    projects_data = response.json()["projects"]
    
    # Matching archived repositories with SEMGREP projects
    projects_to_tag = [project["name"] for project in projects_data if project["name"] in archived_repos]
    
    print(f"Scanned SCP Projects to Tag: {projects_to_tag}")

    return projects_to_tag    

# Function to tag archived repositories in SEMGREP
def tag_archived_repos(projects_to_tag, semgrep_token):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {semgrep_token}"
    }
    deployment_slug = "bodlexnig_personal_org"
    
    # Constructing payload for tagging archived repositories
    payload = {"tags": ["archived"]}
    
    # Tagging archived repositories in SEMGREP
    for project_name in projects_to_tag:
        url = f"https://semgrep.dev/api/v1/deployments/{deployment_slug}/projects/{project_name}/tags"
        response = requests.put(url, headers=headers, json=payload) 
        try:
            if response:
                print(f"Project Tag Sucessful: {response}") # Printing response data
        except Exception as e:
            print(f"Error fetching projects: {e}")    

# Retrieve archived repositories
data = get_paginated_data("https://org-link", GITHUB_AUTH_TOKEN)
archived_repos = get_archived_repos(data)

# Retrieve all projects from SEMGREP
projects_to_tag = get_all_projects(archived_repos, SEMGREP_APP_TOKEN)

# Tag archived repositories in SEMGREP
tag_archived_repos(projects_to_tag, SEMGREP_APP_TOKEN)