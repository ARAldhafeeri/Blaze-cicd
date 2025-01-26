import os
import yaml
import subprocess
from blaze_cicd import blaze_logger
from blaze_cicd.data import YAML_TEMPLATE
from blaze_cicd.github import create_github_repo
from blaze_cicd.argocd import create_argocd_app, create_argocd_project
from blaze_cicd.docker import create_dockerhub_repo
from blaze_cicd.kubectl import  kubectl_create_project_namespace
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
            project["github"]["apiKey"],
            app["templates"]["source"]["name"],
            app["templates"]["source"]["owner"],
            app["templates"]["argocd"]["name"],
            app["templates"]["argocd"]["owner"],
        )

    # Create ArgoCD Project
    blaze_logger.info("Creating ArgoCD Project...")
    create_argocd_project(
        project["argocd"]["project"]["name"],
         project["argocd"]["project"]["description"],
        project["argocd"]["apiKey"],
        project["argocd"]["url"]
    )

    # Create ArgoCD Apps
    for app in apps:
        blaze_logger.info(f"Creating ArgoCD App {app['name']}...")
        create_argocd_app(
            app["argocd"]["app"]["name"],
            app["argocd"]["repo"]["githubRepoUrl"],
            app["argocd"]["app"]["path"],
            app["argocd"]["app"]["projectName"],
            project["argocd"]["apiKey"],
            project["argocd"]["url"],
            app["argocd"]["namespace"]
        )
