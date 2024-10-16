import requests
import os

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_USERNAME = "YonierGomez"  # Reemplaza con tu nombre de usuario de GitHub

def get_repos():
    url = f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    repos = []
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}&per_page=100", headers=headers)
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            return []
        page_repos = response.json()
        if not page_repos:
            break
        repos.extend([repo for repo in page_repos if not repo['fork']])
        page += 1
    return repos

def get_runners(repo_full_name):
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/actions/runners"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching runners for {repo_full_name}: {response.status_code}")
        return []
    return response.json()["runners"]

def delete_runner(repo_full_name, runner_id):
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/actions/runners/{runner_id}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Successfully deleted runner {runner_id} from {repo_full_name}")
    else:
        print(f"Error deleting runner {runner_id} from {repo_full_name}: {response.status_code}")

def main():
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN environment variable is not set. Please set it and try again.")
        return

    repos = get_repos()
    if not repos:
        print("No repositories found or error occurred.")
        return

    for repo in repos:
        print(f"Processing repository: {repo['full_name']}")
        runners = get_runners(repo['full_name'])
        if runners:
            for runner in runners:
                delete_runner(repo['full_name'], runner['id'])
        else:
            print(f"No runners found for {repo['full_name']}")

    print("Runner cleanup complete.")

if __name__ == "__main__":
    main()