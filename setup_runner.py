import requests
import os
import subprocess
import yaml
import re

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

def create_runner_token(repo_full_name):
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/actions/runners/registration-token"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
        return response.json()["token"]
    else:
        print(f"Error creating token for {repo_full_name}: {response.status_code}")
        return None

def sanitize_name(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

def generate_dockerfile():
    dockerfile_content = """
FROM arm64v8/ubuntu:latest
LABEL maintainer="Yonier Gómez"

ENV RUNNER_ALLOW_RUNASROOT=1 \\
    DEBIAN_FRONTEND=noninteractive \\
    runner_user=runner \\
    runner_home_dir=/home/runner

# Update system and install dependencies
RUN apt-get update && apt-get upgrade -y && \\
    apt-get install -y \\
    curl lsb-release apt-transport-https ca-certificates software-properties-common && \\
    apt-get clean

# Create user, assign permissions, Download and configure the runner
RUN groupadd docker && useradd -mU -d $runner_home_dir $runner_user && \\
    mkdir -p $runner_home_dir/actions-runner && \\
    cd $runner_home_dir/actions-runner && \\
    curl -o actions-runner-linux-arm64-2.319.1.tar.gz -L \\
    https://github.com/actions/runner/releases/download/v2.319.1/actions-runner-linux-arm64-2.319.1.tar.gz && \\
    tar xzf ./actions-runner-linux-arm64-2.319.1.tar.gz && \\
    chown -R $runner_user:$runner_user $runner_home_dir/actions-runner && \\
    usermod -aG docker $runner_user && \\
    ./bin/installdependencies.sh

# Add Docker's official GPG key, add Docker repository, and install Docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \\
    add-apt-repository "deb [arch=arm64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \\
    apt-get update && \\
    apt-get install -y docker-ce-cli && \\
    apt-get clean

# Switch to runner user and set working directory
USER $runner_user
WORKDIR $runner_home_dir/actions-runner

# Create start.sh script
RUN echo '#!/bin/bash\\n\\
./config.sh --url $REPO_URL --token $RUNNER_TOKEN --name $RUNNER_NAME --unattended --replace\\n\\
./run.sh' > start.sh && \\
    chmod +x start.sh

# Set the entry point to the start script
ENTRYPOINT ["./start.sh"]
"""
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)

def generate_compose_yaml(repos):
    compose_content = {
        "services": {}
    }
    
    for repo in repos:
        service_name = f"runner_{sanitize_name(repo['name'])}"
        token = create_runner_token(repo['full_name'])
        
        if token:
            compose_content["services"][service_name] = {
                "build": {
                    "context": ".",
                    "dockerfile": "Dockerfile"
                },
                "environment": [
                    f"REPO_URL={repo['html_url']}",
                    f"RUNNER_TOKEN={token}",
                    f"RUNNER_NAME={service_name}"
                ],
                "volumes": [
                    "/var/run/docker.sock:/var/run/docker.sock"
                ],
                "restart": "unless-stopped"
            }
    
    with open("compose.yaml", "w") as f:
        yaml.dump(compose_content, f, default_flow_style=False)

def generate_runner_script():
    script = """#!/bin/bash

# Start containers
docker compose -p work_runners up -d

# Wait for a specified time or until a specific condition is met
sleep 3600  # Wait for 1 hour, adjust as needed

# Stop and remove containers
docker compose -p work_runners down
"""
    
    with open("run_runners.sh", "w") as f:
        f.write(script)
    
    # Make the script executable
    subprocess.run(["chmod", "+x", "run_runners.sh"])

def main():
    repos = get_repos()
    if not repos:
        print("No repositories found or error occurred.")
        return

    generate_dockerfile()
    generate_compose_yaml(repos)
    generate_runner_script()
    print("Setup complete. Run './run_runners.sh' to start the runners.")

if __name__ == "__main__":
    main()