import requests 
from blaze_cicd import blaze_logger

def create_argocd_app(name: str, repo_url: str, server: str,  path: str, project_name: str, api_key: str, argocd_url: str) -> None:
    """Create an ArgoCD application."""
    url = f"{argocd_url}/api/v1/applications"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "metadata": {
            "name": name
        },
        "spec": {
            "source": {
                "repoURL": repo_url,
                "path": path
            },
            "destination": {
                "namespace": "default",
                "server": server
            },
            "project": project_name,
            "syncPolicy": {
                "automated": {}
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        blaze_logger.info(f"Created ArgoCD app: {name}")
    else:
        blaze_logger.error(f"Failed to create ArgoCD app: {response.text}")



def create_argocd_project(name: str, description: str,  api_key: str, argocd_url: str) -> None:
    """Create an ArgoCD project."""
    url = f"{argocd_url}/api/v1/projects"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "project": {
            "metadata": {
                "name": name,
                "description": description
            },
            "spec": {
                "sourceRepos": ["*"],
                "destinations": [
                    {
                        "namespace": "*",
                        "server": "*"
                    }
                ]
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        blaze_logger.info(f"Created ArgoCD project: {name}")
    else:
        blaze_logger.error(f"Failed to create ArgoCD project: {response.text}")