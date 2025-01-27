import os
import yaml
import subprocess
from blaze_cicd import blaze_logger
from blaze_cicd.data import YAML_TEMPLATE
from blaze_cicd.github import create_github_repo, create_github_repo_secret
from blaze_cicd.argocd import create_argocd_app, create_argocd_project, create_argocd_repository
from blaze_cicd.docker import create_dockerhub_repo
from blaze_cicd.kubectl import  kubectl_create_project_namespace
from blaze_cicd.env import replace_env_variables
def init_command(file: str) -> None:
    """Initialize the configuration file."""
    if os.path.exists(file):
        blaze_logger.info(f"File {file} already exists. Aborting.")
        return
    with open(file, "w") as f:
        f.write(YAML_TEMPLATE)
    blaze_logger.info(f"Created {file}. Please fill in the details.")


def build_command(file: str) -> None:
    """Build the project by creating resources based on the configuration file."""
    if not os.path.exists(file):
        blaze_logger.error(f"File {file} does not exist. Run 'blazer init' first.")
        return

    with open(file, "r") as f:
        config = yaml.safe_load(f)

    config = replace_env_variables(config)
    project = config["project"]
    apps = config["apps"]

    # Create Kubernetes Namespace
    blaze_logger.info("Creating namespace using kubectl...")
    kubectl_create_project_namespace(project["namespace"])

    # Create Docker Repos
    blaze_logger.info("Creating Docker Repos...")
    for app in apps:
        create_dockerhub_repo(
            app["docker"]["name"],
            project["dockerHub"]["username"],
            app["docker"]["private"],
            project["dockerHub"]["apiKey"]
        )

    # Create GitHub Repos
    blaze_logger.info("Creating GitHub Repos...")
    for app in apps:
        create_github_repo(
            app["github"]["name"],
            app["github"]["owner"],
            app["github"]["private"],
            project["github"]["apiKey"],
            app["templates"]["source"]["name"],
            app["templates"]["source"]["owner"],
            app["templates"]["argocd"]["name"],
            app["templates"]["argocd"]["owner"],
        )
        # add secrets to the repo
        create_github_repo_secret(
             app["github"]["name"],
             app["github"]["owner"],
             project["github"]["apiKey"],
             "DOCKER_USERNAME",
            project["dockerHub"]["username"],
        )
        create_github_repo_secret(
             app["github"]["name"],
             app["github"]["owner"],
             project["github"]["apiKey"],
             "DOCKER_PASSWORD",
            project["dockerHub"]["apiKey"],
        )
        create_github_repo_secret(
             app["github"]["name"],
             app["github"]["owner"],
             project["github"]["apiKey"],
             "ARGOCD_REPO_ACCESS_TOKEN",
            project["github"]["apiKey"],
        )


    # Create ArgoCD repositories
    blaze_logger.info(f"Creating ArgoCD resources...")
    for app in apps:

        # repositories 
        create_argocd_repository(
            app["argocd"]["repo"]["githubRepoUrl"],
            project["argocd"]["apiKey"],
            project["argocd"]["url"],
            app["templates"]["argocd"]["name"],
            project["name"],
            project["github"]["privateKey"],
        )

        # projects 
        create_argocd_project(
            app["argocd"]["project"]["name"],
            app["argocd"]["project"]["description"],
            project["argocd"]["apiKey"],
            project["argocd"]["url"]
        )

        # apps
        create_argocd_app(
            app["argocd"]["app"]["name"],
            app["argocd"]["repo"]["githubRepoUrl"],
            app["argocd"]["app"]["clusterUrl"],

            app["argocd"]["app"]["path"],
            app["argocd"]["app"]["projectName"],
            project["argocd"]["apiKey"],
            project["argocd"]["url"],
            project["namespace"]
        )