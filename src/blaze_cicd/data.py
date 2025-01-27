YAML_TEMPLATE = """
project:
  name: "your-project-name"
  namespace: "your-namespace"
  argocd:
    apiKey: "%ARGOCD_API_KEY%"
    url: "%ARGOCD_URL%"        
  dockerHub:
    username: "your-docker-registery-username"
    apiKey: "%DOCKER_HUB_API_KEY%" 
  github:
    apiKey: "%GITHUB_API_KEY%"     
    privateKey: "%GITHUB_SSH_PRIVATE_KEY%"  

apps:
  - name: "your-app-name"
    templates:
      source:
        name: "blaze-cicd-react-template"
        owner: "araldhafeeri"
      argocd:
        name: "blaze-cicd-argocd-template"
        owner: "araldhafeeri"
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
        path: "path/to/manifests"
        clusterUrl: "https://kubernetes.default.svc"
        namespace: "your-namespace"
      repo:
        connectionType: "ssh"
        name: "your-repo-name"
        githubRepoUrl: "git@github.com:your-org/your-repo.git"
"""

DOCKER_APIS_BASE_URL = "https://hub.docker.com/v2"
GITHUB_APIS_BASE_URL = "https://api.github.com"
GITHUB_BASE_URL = "https://github.com"