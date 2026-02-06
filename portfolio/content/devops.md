# DevOps

## How I Got Here

In the past few months, I've gained hands-on experience with Kubernetes and container orchestration. One of our three DevOps engineers left, so I volunteered to take on basic deployment responsibilities.

I worked on Dockerfiles, Kubernetes manifests (deployments, ConfigMaps, secrets, HPAs), and used Kustomize to manage configurations across Dev and QA environments. I also took ownership of the CI/CD pipelines for the services I'm involved with and learned to write multistage Dockerfiles.

I'm now confident in owning the full deployment lifecycle for my services, and the DevOps team has bandwidth for higher priority complex projects.

## Cloud Platforms

| Platform | Experience | What I've Done |
|----------|------------|----------------|
| **GCP** | Primary | GKE, Pub/Sub, Cloud Storage, Bigtable, Cloud Logging |
| **AWS** | Limited | CloudWatch for log monitoring |
| **Azure** | Limited | Azure AD for SSO integration |

I have hands-on experience with Google Cloud Platform, primarily working with GKE (Kubernetes Engine), Pub/Sub for messaging, Cloud Storage for scan data, and Bigtable for metadata. While the DevOps team handles infrastructure provisioning, I work directly with these services for deployments, messaging, and data storage.

## Kubernetes

- Kubernetes manifests and Kustomize for environment configuration
- CI/CD pipelines using GitHub Actions
- Multistage Dockerfiles for optimized builds
- Managing deployments across Dev and QA environments in GKE

One improvement I designed was for one of our custom scanners. Previously, we had to update the entire deployment just to update the scanning templates. I built a GitHub Actions pipeline that pushes templates to our artifact registry, and used a Kubernetes initContainer to pull the latest templates at startup. This segregated template updates from application deployments.

## CI/CD

I am responsible for releases and monitor rollouts, fixing issues as they come up. My current setup involves:

- **GitHub Actions** - Build, test, and deploy pipelines
- **Docker** - Containerization with multistage builds
- **Kubernetes** - Deployment to GKE

## Infrastructure Tools

- **Docker** - Daily driver for local development and production deployments
- **Ansible** - Used at EY to automate baseline configuration checks across Active Directory systems
- **Kustomize** - Managing configuration across environments

## Monitoring & Observability

- **Cloud Logging** - GCP's native logging, redirected to Cloud Storage for non-prod to reduce costs
- **OpenSearch** - Pushing logs when we need to analyze them
- **Slack Alerts** - Created and deployed a company-wide alerting library that enables all microservices to send real-time incident notifications

## Honest Assessment

I'd be honest that my DevOps experience is more recent and practical rather than deep. I haven't built infrastructure from scratch using Terraform, and I don't have experience with service meshes or advanced Kubernetes operators. But I can deploy, troubleshoot, and manage the full lifecycle of services I own. This is an area I'm actively developing.
