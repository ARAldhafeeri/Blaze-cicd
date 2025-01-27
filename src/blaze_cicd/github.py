import requests 
from blaze_cicd import blaze_logger
from blaze_cicd.data import GITHUB_APIS_BASE_URL, GITHUB_BASE_URL
from blaze_cicd.utils import encrypt_secret

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
    
def create_github_repo(
        repo_name: str, 
        owner_name: str,  
        is_private: bool, 
        api_key: str, 
        source_template_name: str, 
        source_owner_name: str, 
        argocd_template_name: str, 
        argocd_owner_name: str ) -> None:
    """
    Create a GitHub repository. If a template URL is provided, create the repository from the template.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.github.v3+json"
    }

    if github_repo_exists(repo_name, owner_name, api_key):
        pass
    else:  
    
        if source_template_name and source_owner_name:
            data, url = create_repo_from_template(source_template_name, repo_name, source_owner_name, is_private, False)
        else:
            data, url = create_new_repo(repo_name, is_private)

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            blaze_logger.info(f"Created GitHub repo: {repo_name} {'from template' if source_owner_name else ''}")
        else:
            blaze_logger.error(f"Failed to create GitHub repo: {response.text}")
    
    if github_repo_exists(f"{repo_name}-argocd", owner_name, api_key):
        pass 
    else:  
    
        if argocd_template_name and argocd_owner_name:
            data, url = create_repo_from_template(argocd_template_name, repo_name, argocd_owner_name, is_private, True)
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                blaze_logger.info(f"Created GitHub argocod config repo: {repo_name} {'from template' if argocd_template_name else ''}")
            else:
                blaze_logger.error(f"Failed to create GitHub repo: {response.text}")

def create_repo_from_template(template_name: str, repo_name: str, owner_name: str,  is_private: bool, is_argocd_repo: bool):
    url = f"{GITHUB_APIS_BASE_URL}/repos/{owner_name}/{template_name}/generate"
    repo_name = f"{repo_name}-argocd" if is_argocd_repo else repo_name
    data = {
        "name": repo_name,
        "private": is_private,
        "owner": owner_name,
    }
    print("data", data, url)
    return data, url

def create_new_repo(repo_name: str, owner_name: str,  is_private: bool):
    url = f"{GITHUB_APIS_BASE_URL}/user/repos"
    data = {
        "name": repo_name,
        "private": is_private,
        "auto_init": True 
    }
    blaze_logger.info(f"Creating new repo {repo_name}")
    return data, url

def get_repo_public_key(repo_name: str, owner_name: str, api_key: str):
    url = f"{GITHUB_APIS_BASE_URL}/repos/{owner_name}/{repo_name}/actions/secrets/public-key"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve public key: {response.status_code} {response.text}")
    
def create_github_repo_secret(repo_name: str, owner_name: str, api_key: str, secret_name: str, secret_value: str):
    # Get the public key
    public_key_info = get_repo_public_key(repo_name, owner_name, api_key)
    public_key = public_key_info['key']
    key_id = public_key_info['key_id']
    
    encrypted_value = encrypt_secret(public_key, secret_value)
    
    url = f"{GITHUB_APIS_BASE_URL}/repos/{owner_name}/{repo_name}/actions/secrets/{secret_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "encrypted_value": encrypted_value,
        "key_id": key_id
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 201:
        blaze_logger.info(f"Secret {secret_name} created for {repo_name}!")
    elif response.status_code == 204:
        blaze_logger.info(f"Secret {secret_name} updated for {repo_name}!")
    else:
        blaze_logger.info(f"Failed to create/update {secret_name}! Status code: {response.status_code}, Response: {response.text}")
