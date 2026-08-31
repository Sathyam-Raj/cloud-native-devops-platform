\# Demo Guide



\## Demo Objective



Demonstrate the complete flow from a code change to a tested Docker image, Amazon ECR, GitOps deployment, Kubernetes rollout, autoscaling, and monitoring.



The recommended demo duration is approximately 8–12 minutes.



\## 1. Start with the Architecture



Open the project README and briefly explain:



> This project demonstrates an end-to-end cloud-native DevOps workflow. GitHub Actions handles CI and image publishing, AWS ECR stores immutable images, Argo CD manages GitOps deployment, Kubernetes runs the application, and Prometheus and Grafana provide monitoring and alerting.



Do not spend too long on the architecture.



\---



\## 2. Show the Repository



Show the main project structure:



```text

.github/

app/

docker/

helm/

k8s/

argocd/

terraform/

monitoring/

docs/

README.md

```



Explain that each directory represents a part of the DevOps platform.



\---



\## 3. Show GitHub Actions



Open:



```text

GitHub → Actions → CI

```



Show a successful workflow.



Highlight:



```text

Ruff

Pytest

Docker Build

Trivy Scan

Configure AWS Credentials

ECR Login

Docker Push

Update Helm Image Tag

```



Key point to explain:



> GitHub Actions does not use long-lived AWS access keys. It uses GitHub OIDC to assume a dedicated AWS IAM role.



\---



\## 4. Show Amazon ECR



Open:



```text

AWS Console → ECR → cloud-native-devops-platform

```



Show the image tags.



Explain:



> Images are tagged using the Git commit SHA, which gives every deployment a traceable and immutable image version.



\---



\## 5. Show Argo CD



Open the Argo CD application:



```text

cloud-app

```



Show:



```text

Synced

Healthy

Automated Sync

Prune

Self-Heal

```



Explain:



> Argo CD continuously compares the Kubernetes environment with the desired state stored in Git.



\---



\## 6. Show Kubernetes



Run:



```cmd

kubectl get nodes

kubectl get pods -n cloud-app

kubectl get hpa -n cloud-app

```



Explain:



> The application runs in Kubernetes with health probes and an HPA configured between 2 and 5 replicas with a 70% CPU target.



\---



\## 7. Demonstrate GitOps Deployment



Make a small safe Helm change, for example a pod annotation.



Then:



```cmd

git add .

git commit -m "Demo GitOps deployment"

git push

```



Show:



```text

GitHub Actions

&#x20;     ↓

New image / Git change

&#x20;     ↓

Argo CD detects revision

&#x20;     ↓

Kubernetes rollout

&#x20;     ↓

New pods

```



Then verify:



```cmd

kubectl get pods -n cloud-app

```



This demonstrates that a Git change can automatically reach Kubernetes through the GitOps pipeline.



\---



\## 8. Show Monitoring



Open Grafana.



Show the:



```text

Cloud App

Kubernetes Monitoring

```



dashboard.



Highlight:



\- CPU usage

\- Memory usage

\- Ready pod count

\- HPA current vs target

\- Deployment replicas

\- Container restarts

\- High CPU alert



Explain:



> Prometheus collects the metrics and Grafana provides the monitoring dashboard and alerting.



\---



\## 9. Show Terraform



From the Terraform directory:



```cmd

terraform plan

```



Show:



```text

No changes. Your infrastructure matches the configuration.

```



Explain:



> The AWS ECR, OIDC, IAM role, and ECR policy are represented in Terraform, and the existing resources were imported rather than recreated.



\---



\## 10. Strong Interview Talking Points



\### Why GitHub OIDC?



> It avoids storing long-lived AWS access keys in GitHub and allows the workflow to assume a restricted IAM role.



\### Why ECR?



> It provides a private AWS-native container registry for the Kubernetes deployment pipeline.



\### Why Helm?



> It packages the Kubernetes application and makes deployment configuration reusable and manageable.



\### Why Argo CD?



> It provides GitOps-based continuous reconciliation, automated synchronization, pruning, and self-healing.



\### Why Terraform?



> It makes the AWS infrastructure reproducible and declarative.



\### Why Trivy?



> It adds container vulnerability scanning before images are promoted to the deployment environment.



\### Why Prometheus and Grafana?



> Prometheus collects metrics and Grafana provides visualization and alerting for the Kubernetes application.



\### What happens when a pod fails?



> Kubernetes restarts or replaces the workload according to the Deployment and health-probe configuration, while Argo CD ensures the desired state remains aligned with Git.



\---



\## 11. Commands to Keep Ready During the Demo



```cmd

kubectl get nodes

kubectl get pods -n cloud-app

kubectl get hpa -n cloud-app

kubectl top pods -n cloud-app

kubectl get application cloud-app -n argocd

kubectl get pods -n monitoring

```



AWS:



```cmd

aws sts get-caller-identity

aws ecr list-images --repository-name cloud-native-devops-platform --region eu-north-1

```



Terraform:



```cmd

cd terraform

terraform plan

```



\---



\## 12. Final Demo Message



A good closing explanation is:



> The project automates the complete path from source code to Kubernetes deployment. GitHub Actions validates and scans the application, AWS ECR stores the immutable container image, Terraform manages the AWS infrastructure, Argo CD handles GitOps deployment and self-healing, Kubernetes provides orchestration and autoscaling, and Prometheus with Grafana provides observability.

