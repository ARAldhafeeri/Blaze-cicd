YAML_TEMPLATE = """
project:
  name: "your-project-name"
  namespace: "your-namespace"
  argocd:
    apiKey: "{{ .Env.ARGOCD_API_KEY }}"
    url: "https://argocd.example.com"
  dockerHub:
    username: "{{ .Env.DOCKER_HUB_USERNAME }}"
    apiKey: "{{ .Env.DOCKER_HUB_API_KEY }}"
  github:
    apiKey: "{{ .Env.GITHUB_API_KEY }}"
    privateKey: "{{ .Env.GITHUB_PRIVATE_KEY }}"
apps:
  - name: "your-app-name"
    templates:
      source: "git"
    docker:
      isPrivate: true
      name: "your-docker-image-name"
    github:
      isPrivate: true
      name: "your-github-repo-name"
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
"""