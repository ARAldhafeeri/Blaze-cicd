import requests 
from blaze_cicd import blaze_logger
from blaze_cicd.data import GITHUB_APIS_BASE_URL, GITHUB_BASE_URL
def create_github_repo(repo_name: str, owner_name: str,  is_private: bool, api_key: str, source_template_name: str = None, argocd_template_name: str = None, source_owner_name: str = None, argocd_owner_name: str = None) -> None:
    """
    Create a GitHub repository. If a template URL is provided, create the repository from the template.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.github.v3+json"
    }

    if github_repo_exists(repo_name, owner_name, api_key):
        return 
    
    if source_template_name and source_owner_name:
        data, url = create_repo_from_template(source_template_name, repo_name, source_owner_name, is_private)
    else:
        data, url = create_new_repo(repo_name, is_private)
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        blaze_logger.info(f"Created GitHub repo: {repo_name} {'from template' if source_owner_name else ''}")
    else:
        blaze_logger.error(f"Failed to create GitHub repo: {response.text}")
    
    if github_repo_exists(f"{repo_name}-argocd", owner_name, api_key):
        return 
    
    if argocd_template_name and argocd_owner_name:
        data, url = create_repo_from_template(argocd_template_name, repo_name, argocd_template_name, is_private)
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            blaze_logger.info(f"Created GitHub argocod config repo: {repo_name} {'from template' if argocd_template_name else ''}")
        else:
            blaze_logger.error(f"Failed to create GitHub repo: {response.text}")

def create_repo_from_template(template_name: str, repo_name: str, owner_name: str,  is_private: bool):
    url = f"{GITHUB_APIS_BASE_URL}/repos/{owner_name}/{template_name}/generate"
    data = {
        "name": repo_name,
        "private": is_private,
    }
    return url, data

def create_new_repo(repo_name: str, owner_name: str,  is_private: bool):
    url = f"{GITHUB_APIS_BASE_URL}/user/repos"
    data = {
        "name": repo_name,
        "private": is_private,
        "auto_init": True 
    }
    blaze_logger.info(f"Creating new repo {repo_name}")
    return url, data

def github_repo_exists(repo_name: str, owner_name: str, api_key):
    url = f"{GITHUB_APIS_BASE_URL}/repos/{owner_name}/{repo_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        blaze_logger.info("Skipping creation of repo, repo exists")
        return True
    else:
        blaze_logger.info("Skipping creation of repo, repo exists")
        return False

