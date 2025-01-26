YAML_TEMPLATE = """
project:
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
      source:
        name: "source-code-github-template-name"
        owner: "source-code-github-owner-name"
      argocd:
        name: "source-code-github-template-name"
        owner: "source-code-github-owner-name"
    docker:
      private: true # true -> private repo, false -> public repo
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
        sshPrivateKeyData: "your-github-account-ssh-key-to-pull-private-repos"
"""

DOCKER_APIS_BASE_URL = "https://hub.docker.com/v2"
GITHUB_APIS_BASE_URL = "https://api.github.com"
GITHUB_BASE_URL = "https://github.com"