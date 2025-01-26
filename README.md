# Blaze-cicd

<div align="center">
  <img src="blaze-cicd.png" alt="Blaze CI/CD Logo" width="200" style="border-radius: 50%;"/>
</div>

Blaze CI/CD is a Command Line Interface (CLI) tool designed to automate the creation of production-ready CI/CD pipelines.

## Overview

Blaze CI/CD is a Command Line Interface (CLI) tool designed to automate the creation of production-ready CI/CD pipelines. The tool integrates with Kubernetes, Docker, DockerHub, GitHub, GitHub Actions, and ArgoCD to provide a seamless setup experience. Users provide essential details such as project name, API keys, and application configurations, and the tool handles the creation of namespaces, repositories, and CI/CD pipelines.

## Installation

You can install the Blaze CI/CD CLI tool using pip:

```bash
pip install blaze-cicd
```

## Architecture Diagram

Below is a high-level architecture diagram of blaze CI/CD:

<div align="center">
  <img src="diagram.png" alt="Blaze CI/CD Architecture Diagram" width="600" style="border: 1px solid #ccc; border-radius: 8px;"/>
</div>

## Key Features

- **Automated Pipeline Creation**: Automates the setup of CI/CD pipelines using Kubernetes (`kubectl`), Docker, GitHub, and ArgoCD.
- **YAML Configuration**: Users provide project and application details via a YAML configuration file that will be used to construct the entire CI/CD pipeline with a single command.
- **Multi-Service Integration**: Integrates with DockerHub, GitHub, and ArgoCD to create repositories, projects, and applications. Can handle pipelines for multiple services.
- **CLI Interface**: Simple command-line interface with `init` and `build` commands.
- **Minimal Setup**: Other than configuring `kubectl`, Python, installing the package, and providing API keys, there are no additional steps other than filling out the `config.yaml`.
- **Graceful Degradation**: Blaze CI/CD ensures robust pipeline creation by verifying the existence of resources at each step. If a resource (e.g., repository, project, or application) already exists, Blaze skips its creation to avoid redundancy. If a resource is missing, it creates it automatically.

In case of failure, Blaze stops the process and provides detailed error messages, enabling users to troubleshoot and resolve issues efficiently. This step-by-step approach ensures that subsequent operations rely on successful completion of the previous steps, maintaining the integrity of the CI/CD pipeline while empowering users with actionable insights.

## Targeted Stack

- **Kubernetes**: For container orchestration and namespace management.
- **Docker**: For containerization of applications.
- **DockerHub**: For Docker image storage and management.
- **GitHub**: For source code management and version control.
- **GitHub Actions**: For CI/CD workflows.
- **ArgoCD**: For GitOps-based continuous delivery.

## Prerequisites

Before using blaze CI/CD, ensure the following prerequisites are met:

1. **Kubernetes Cluster**:

   - A running Kubernetes cluster with `kubectl` configured on the machine you plan to run this CLI tool from.
   - Ensure you have the necessary permissions to create namespaces and manage resources in the cluster.

2. **DockerHub Account**:

   - A DockerHub account with an API key for creating and managing Docker repositories, with write/read access.

3. **GitHub Account**:

   - A GitHub account with an API key for creating repositories and managing GitHub Actions workflows.
   - A GitHub private key for integrating with ArgoCD config repositories.

4. **ArgoCD**:

   - An ArgoCD instance with an API key account for creating projects and applications.
   - Ensure the ArgoCD URL is accessible from the machine where you plan to run the tool from.

5. **Python**:

   - Python 3.7 or higher installed on your machine.
   - Required Python libraries: `argparse`, `yaml`, `subprocess`, and `requests`.

6. **blaze CI/CD Installation**:
   - Install the blaze CI/CD CLI tool using pip:
     ```bash
     pip install blaze-cicd
     ```

## User Input

The user also creates a YAML file with the following format:

```yaml
project:
  name: "your-project-name"
  namespace: "your-namespace"
  argocd:
    apiKey: "your-argocd-api-key"
    url: "https://argocd.example.com"
  dockerHub:
    username: "your-docker-registery-username"
    apiKey: "your-docker-registery-apikey"
  github:
    apiKey: "your-github-developer-apikey"
    privateKey: "your-ssh-key"
apps:
  - name: "your-app-name"
    templates:
      source: "source-code-github-template-name"
      sourceTemplateOwnerName: "source-owner-name"
      argocd: "argocd-application-config-files-template-name"
      argocdTemplateOwnerName: "argocd-owner-name"
    docker:
      private: true # true -> private repo , false -> public repo.
      name: "your-docker-image-name"
    github:
      private: true
      name: "your-github-repo-name"
      owner: "your-github-repo-owner-name"
    argocd:
      project:
        name: "your-argocd-project-name"
        description: "Your ArgoCD project description"
      app:
        name: "your-argocd-app-name"
        projectName: "your-argocd-project-name"
        path: "path/to/manifests"
        clusterUrl: "https://kubernetes.default.svc"
        namespace: "your-namespace"
      repo:
        connectionType: "ssh"
        name: "your-repo-name"
        projectName: "your-project-name"
        githubRepoUrl: "git@github.com:your-org/your-repo.git"
        sshPrivateKeyData: "{{ .Env.SSH_PRIVATE_KEY }}"
```

## Workflow

1. **Initialization**: The user runs the `init` command to generate a YAML template which the user will fill with the needed information.
2. Setup needed API keys in GitHub, ArgoCD, DockerHub.
3. Kubernetes Cluster with configured kubectl on machine.
4. **Configuration**: The user fills in the YAML file with project and application details.
5. **Build**: The user runs the `build` command to create the CI/CD pipeline.

Important note: your tempalte repo should not have any github workflow in it, argocd is fine to have data in it but ideally none. This allows for no accedental creation of resources.

## CLI Commands

### `init` Command

- **Purpose**: Generates a YAML template for the user to fill in.
- **Usage**: `blaze init --file blaze-config.yaml`
- **Output**: Creates a `blaze-config.yaml` file with the predefined template.

### `build` Command

- **Purpose**: Reads the YAML configuration and creates the CI/CD pipeline.
- **Usage**: `blaze build --file blaze-config.yaml`
- **Output**:
  - Creates a Kubernetes namespace using current context configured to kubectl.
  - Creates DockerHub repositories.
  - Creates GitHub repositories.
  - Configures repositories in ArgoCD.
  - Creates an ArgoCD project.
  - Creates ArgoCD applications.
