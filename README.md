# Blaze-cicd
Blazer CI/CD is a Command Line Interface (CLI) tool designed to automate the creation of production-ready CI/CD pipelines. 

# Blazer CI/CD CLI Tool

## Overview

Blazer CI/CD is a Command Line Interface (CLI) tool designed to automate the creation of production-ready CI/CD pipelines. The tool integrates with Kubernetes, Docker, DockerHub, GitHub, GitHub Actions, and ArgoCD to provide a seamless setup experience. Users provide essential details such as project name, API keys, and application configurations, and the tool handles the creation of namespaces, repositories, and CI/CD pipelines.

## Key Features

- **Automated Pipeline Creation**: Automates the setup of CI/CD pipelines using Kubernetes (`kubectl`), Docker, GitHub, and ArgoCD.
- **YAML Configuration**: Users provide project and application details via a YAML configuration file that will be used to construct the entire CI/CD pipeline with a single command.
- **Multi-Service Integration**: Integrates with DockerHub, GitHub, and ArgoCD to create repositories, projects, and applications. Can handle pipelines for multiple services.
- **CLI Interface**: Simple command-line interface with `init` and `build` commands.
- **Minimal Setup**: Other than configuring `kubectl`, Python, installing the package, and providing API keys, there are no additional steps other than filling out the `config.yaml`.

## Targeted Stack

- **Kubernetes**: For container orchestration and namespace management.
- **Docker**: For containerization of applications.
- **DockerHub**: For Docker image storage and management.
- **GitHub**: For source code management and version control.
- **GitHub Actions**: For CI/CD workflows.
- **ArgoCD**: For GitOps-based continuous delivery.

## User Input

The user provides the following information:

- **Project Name**: Name of the project.
- **Namespace**: Namespace to be used to create the project.
- **DockerHub API Key**: API key for DockerHub to create repositories for the project in the registry.
- **GitHub API Key**: API key for GitHub.
- **GitHub Private Key**: GitHub Private key used to create application repos inside argocd.
- **ArgoCD API Key**: API key for ArgoCD.

The user also creates a YAML file with the following format:

```yaml
project:
  name: 
  namespace: 
  ArgoCDAPIKey: 
  GithubAPIKey: 
  GitHubPrivateKey:
  DockerHubAPIKey: 
  ArgoCDURL: 
apps:
  - name: 
    repo: 
    template-source: 
    template-argocd: 
```

## Workflow

1. **Initialization**: The user runs the `init` command to generate a YAML template which the user will fill with the needed information.
2. Setup needed API keys in GitHub, ArgoCD, DockerHub.
3. Kubernetes Cluster with configured kubectl on machine.
4. **Configuration**: The user fills in the YAML file with project and application details.
5. **Build**: The user runs the `build` command to create the CI/CD pipeline.

## CLI Commands

### `init` Command

- **Purpose**: Generates a YAML template for the user to fill in.
- **Usage**: `blazer init --file blazer-config.yaml`
- **Output**: Creates a `blazer-config.yaml` file with the predefined template.

### `build` Command

- **Purpose**: Reads the YAML configuration and creates the CI/CD pipeline.
- **Usage**: `blazer build --file blazer-config.yaml`
- **Output**:
  - Creates a Kubernetes namespace.
  - Creates DockerHub repositories.
  - Creates GitHub repositories.
  - Configures repositories in ArgoCD.
  - Creates an ArgoCD project.
  - Creates ArgoCD applications.

## Implementation Details

### Python Script: `main.py`

The Python script uses the following libraries:

- **argparse**: For parsing command-line arguments.
- **yaml**: For reading and writing YAML files.
- **subprocess**: For executing shell commands (e.g., `kubectl`).
- **requests**: For making HTTP requests to external APIs (e.g., DockerHub, GitHub, ArgoCD).

### Key Functions

- **`init_command(file)`**:
  - Generates a YAML template file if it doesn't already exist.
  - Outputs a message indicating the file has been created.

- **`create_dockerhub_repo(repo_name, api_key)`**:
  - Makes an API call to DockerHub to create a new repository.
  - Handles the response and prints success or failure messages.

- **`create_github_repo(repo_name, api_key)`**:
  - Makes an API call to GitHub to create a new repository.
  - Handles the response and prints success or failure messages.

- **`create_argocd_project(project_name, api_key)`**:
  - Makes an API call to ArgoCD to create a new project.
  - Handles the response and prints success or failure messages.

- **`configure_argocd_repos(file)`**:
  - The ArgoCD GitHub repos will be synced as repositories inside ArgoCD.

- **`create_argocd_app(app_name, repo_url, template_source, template_argocd, api_key)`**:
  - Makes an API call to ArgoCD to create a new application.
  - Handles the response and prints success or failure messages.

- **`build_command(file)`**:
  - Reads the YAML configuration file.
  - Executes the necessary steps to create the CI/CD pipeline:
    - Creates a Kubernetes namespace.
    - Creates DockerHub repositories.
    - Creates GitHub repositories.
    - Creates an ArgoCD project.
    - Creates ArgoCD applications.

## Example Output

When the user runs the `build` command, the following output is expected:

```
Creating namespace using kubectl...DONE
Creating Docker Repos...DONE
Creating GitHub Repos...DONE
Creating ArgoCD Project...DONE
Creating ArgoCD App...DONE
```

## Error Handling

- **File Existence**: The script checks if the YAML file exists before attempting to read or write.
- **API Responses**: The script checks the status codes of API responses and prints appropriate success or failure messages.
- **Subprocess Execution**: The script uses `subprocess.run` with `check=True` to ensure that shell commands (e.g., `kubectl`) execute successfully.

## Installation

You can install the Blazer CI/CD CLI tool using pip:

```bash
pip install blazer-cicd
```

## Conclusion

Blazer CI/CD CLI tool simplifies the setup of production-ready CI/CD pipelines by automating the creation of necessary resources across multiple platforms. The tool is designed to be extensible, allowing for future enhancements and integrations with additional services.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/ARAldhafeeri/Blaze-cicd).
