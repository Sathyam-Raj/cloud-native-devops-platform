\# Troubleshooting Guide



This document records the main issues encountered while building the platform, the reason for each issue, and how it was resolved.



\## 1. GitHub Actions → AWS OIDC Authentication Failed



\### Problem



GitHub Actions failed with:



```text

Not authorized to perform sts:AssumeRoleWithWebIdentity

```



\### Cause



The AWS IAM trust policy used an incorrect GitHub OIDC `sub` value.



\### Diagnosis



Checked the GitHub repository and owner IDs using the GitHub API and reviewed the IAM role trust policy.



\### Fix



Updated the IAM trust policy to use the repository's immutable GitHub OIDC subject:



```text

repo:OWNER@OWNER-ID/REPO@REPO-ID:ref:refs/heads/main

```



After updating the trust policy, GitHub Actions successfully assumed the IAM role.



\### Verification



```bash

aws sts get-caller-identity

```



GitHub Actions successfully returned an assumed-role identity.



\---



\## 2. Docker Push Failed with "No Such Image"



\### Problem



The ECR push step failed with:



```text

No such image: cloud-native-app:<commit-sha>

```



\### Cause



The ECR push step was executed before the Docker image was built.



\### Diagnosis



Reviewed the GitHub Actions step order.



\### Fix



Reordered the workflow:



```text

Docker Build

&#x20;   ↓

Trivy Scan

&#x20;   ↓

ECR Login

&#x20;   ↓

ECR Push

```



\### Result



The Docker image was successfully pushed to Amazon ECR.



\---



\## 3. Argo CD Service Sync Failed



\### Problem



Argo CD failed to reconcile the Service with:



```text

spec.ports\[0].name: Required value

```



\### Cause



The live Kubernetes Service had drifted from the Helm definition, and the Service port did not have an explicit name.



\### Fix



Added a named port to the Helm Service template:



```yaml

ports:

&#x20; - name: http

&#x20;   protocol: TCP

&#x20;   port: 80

&#x20;   targetPort: 5000

```



The drifted Service was recreated and Argo CD successfully reconciled it.



\### Result



```text

Argo CD: Synced

Health:  Healthy

```



\---



\## 4. Terraform Authentication Failed



\### Problem



Terraform failed with:



```text

No valid credential sources found

login session has expired

```



\### Cause



The AWS CLI authentication session had expired.



\### Fix



Re-authenticated using:



```bash

aws login

```



Then verified:



```bash

aws sts get-caller-identity

```



After authentication was restored:



```bash

terraform plan

```



returned:



```text

No changes. Your infrastructure matches the configuration.

```



\---



\## 5. Kubernetes Pod Entered ImagePullBackOff



\### Problem



A newly created application pod entered:



```text

ImagePullBackOff

```



with:



```text

403 Forbidden

```



when pulling from Amazon ECR.



\### Cause



The Kubernetes `ecr-registry-secret` contained an expired ECR authentication token.



The secret had been created more than 24 hours earlier, while ECR authentication tokens are temporary.



\### Diagnosis



Checked the pod events:



```bash

kubectl describe pod <pod-name> -n cloud-app

```



The error showed:



```text

403 Forbidden

```



The image itself existed in ECR, so the problem was authentication rather than the image tag.



\### Fix



Refreshed the ECR pull secret:



```bash

aws ecr get-login-password --region eu-north-1

```



Created a new Kubernetes Docker registry secret and recreated the failed pod.



\### Result



The new pod successfully pulled the image and became:



```text

1/1 Running

```



Argo CD returned to:



```text

Synced

Healthy

```



\### Local vs Production Note



This solution is suitable for the local Kind environment used in this project.



For a production EKS deployment, ECR authentication should use an AWS-native mechanism rather than relying on a manually refreshed Kubernetes registry secret.



\---



\## 6. Helm Command Not Found



\### Problem



Windows returned:



```text

'helm' is not recognized as an internal or external command

```



\### Cause



Helm was installed, but its directory was not available on the current PATH.



\### Diagnosis



Located `helm.exe` using:



```cmd

where /R C:\\ helm.exe

```



\### Fix



Used the installed executable directly and later configured the PATH.



Example:



```cmd

"C:\\Path\\To\\helm.exe" version

```



\---



\## 7. Kind Command Not Found



\### Problem



Windows returned:



```text

'kind' is not recognized

```



\### Cause



The `kind.exe` executable existed but was not on PATH.



\### Diagnosis



Located it with:



```cmd

where /R C:\\ kind.exe

```



\### Fix



Used the actual executable path and configured the PATH correctly.



\---



\## General Troubleshooting Approach



When a component fails:



1\. Check the current status.

2\. Inspect the detailed error or events.

3\. Identify whether the issue is configuration, authentication, ordering, or runtime state.

4\. Fix the source of truth rather than repeatedly restarting components.

5\. Re-run the verification command.

6\. Confirm the final state through Git, Kubernetes, AWS, or Argo CD.



Useful commands:



```bash

kubectl get pods -n cloud-app

kubectl describe pod <pod-name> -n cloud-app

kubectl get application cloud-app -n argocd

kubectl describe application cloud-app -n argocd



aws sts get-caller-identity

aws ecr list-images --repository-name cloud-native-devops-platform --region eu-north-1



terraform validate

terraform plan

```

