import requests 
from blaze_cicd import blaze_logger

def create_github_repo(repo_name: str, is_private: bool, api_key: str, template_url: str = None) -> None:
    """
    Create a GitHub repository. If a template URL is provided, create the repository from the template.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.github.v3+json"
    }

    if template_url:
        # Extract owner and repo from the template URL
        # Example: https://github.com/owner/template-repo -> owner/template-repo
        template_path = template_url.replace("https://github.com/", "").strip("/")
        owner, template_repo = template_path.split("/")

        # Use the GitHub API to create a repository from a template
        url = f"https://api.github.com/repos/{owner}/{template_repo}/generate"
        data = {
            "name": repo_name,
            "private": is_private,
            "owner": owner  # Optional: Specify the owner of the new repo (defaults to the authenticated user)
        }
    else:
        # Use the GitHub API to create a regular repository
        url = "https://api.github.com/user/repos"
        data = {
            "name": repo_name,
            "private": is_private,
            "auto_init": True 
        }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        blaze_logger.info(f"Created GitHub repo: {repo_name} {'from template' if template_url else ''}")
    else:
        blaze_logger.error(f"Failed to create GitHub repo: {response.text}")


