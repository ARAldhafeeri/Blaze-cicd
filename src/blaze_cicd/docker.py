import requests 
from blaze_cicd import blaze_logger

def create_dockerhub_repo(repo_name: str, docker_hub_username: str, is_private: bool, api_key: str) -> None:
    """Create a DockerHub repository."""
    url = "https://hub.docker.com/v2/repositories/"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "namespace": docker_hub_username,
        "name": repo_name,
        "is_private": is_private
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        blaze_logger.info(f"Created DockerHub repo: {repo_name} under namespace: {docker_hub_username}")
    else:
        blaze_logger.error(f"Failed to create DockerHub repo: {response.text}")
