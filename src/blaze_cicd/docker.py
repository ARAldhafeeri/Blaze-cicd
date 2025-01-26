import requests 
from blaze_cicd import blaze_logger
from blaze_cicd.data import DOCKER_APIS_BASE_URL

def create_dockerhub_repo(repo_name: str, docker_hub_username: str, is_private: bool, api_key: str) -> None:
    """Create a DockerHub repository if repository does not exists for the given namespace, else skip the creation and log."""
    repository_exists = dockerhub_repo_exists(repo_name, docker_hub_username, api_key)

    if repository_exists:
        return 
    
    url = f"{DOCKER_APIS_BASE_URL}/repositories/"
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

def dockerhub_repo_exists(repo_name: str, docker_hub_username: str, api_key: str) -> None:
    """Create a DockerHub repository."""
    url = f"{DOCKER_APIS_BASE_URL}/namespaces/{docker_hub_username}/repositories/{repo_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        blaze_logger.info(f"Repository with name {repo_name} in namespace {docker_hub_username} already exists skipping creation process!")
        return True
    else:
        blaze_logger.error(f"Repository with name {repo_name} in namespace {docker_hub_username} deos not exists, creating repository..")
        return False