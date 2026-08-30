\# Cloud Native DevOps Platform



\## Description



Cloud Native DevOps Platform is an end-to-end DevOps project that demonstrates how a Python application can be containerized, tested, security-scanned, deployed to Kubernetes, and continuously delivered using GitOps.



The project integrates GitHub Actions, Docker, Kubernetes, Helm, AWS ECR, AWS IAM with GitHub OIDC, Terraform, Argo CD, Prometheus, and Grafana to create an automated and observable deployment pipeline.



The application uses PostgreSQL as its database and includes health checks, autoscaling, Kubernetes Secrets, automated image promotion, GitOps synchronization, monitoring, and alerting.




\## Technology Stack



\- Python

\- Flask

\- PostgreSQL

\- Docker

\- Kubernetes

\- Kind

\- Helm

\- GitHub Actions

\- Trivy

\- Amazon ECR

\- AWS IAM / OIDC

\- Terraform

\- Argo CD

\- Prometheus

\- Grafana





\## Architecture



```text

+----------------------+

|      Developer       |

+----------+-----------+

&#x20;          |

&#x20;       Git Push

&#x20;          v

+----------------------+

|       GitHub         |

|      Repository      |

+----------+-----------+

&#x20;          |

&#x20;          v

+--------------------------------+

|       GitHub Actions CI        |

|                                |

|  Ruff → Pytest → Docker Build  |

|              ↓                 |

|           Trivy Scan            |

+---------------+----------------+

&#x20;               |

&#x20;           AWS OIDC

&#x20;               |

&#x20;               v

+--------------------------------+

|          AWS IAM Role          |

|   GitHubActionsECRPushRole     |

+---------------+----------------+

&#x20;               |

&#x20;               v

+--------------------------------+

|          Amazon ECR            |

| cloud-native-devops-platform   |

+---------------+----------------+

&#x20;               |

&#x20;        Update Helm Tag

&#x20;               |

&#x20;               v

+--------------------------------+

|            Argo CD             |

|      Auto-Sync + Prune         |

|          + Self-Heal           |

+---------------+----------------+

&#x20;               |

&#x20;               v

+--------------------------------+

|       Kubernetes / Kind        |

|                                |

|   +------------------------+   |

|   |    Cloud App + HPA     |   |

|   +------------------------+   |

|                                |

|   +------------------------+   |

|   |      PostgreSQL        |   |

|   +------------------------+   |

+---------------+----------------+

&#x20;               |

&#x20;               v

+--------------------------------+

|       Prometheus + Grafana     |

|       Monitoring + Alerts      |

+--------------------------------+

```





\## Key Features



\- Automated CI with Ruff and Pytest

\- Docker image build and vulnerability scanning with Trivy

\- Immutable Git SHA image tags in Amazon ECR

\- Secure GitHub Actions → AWS authentication using OIDC

\- Least-privilege IAM for ECR access

\- Terraform-managed AWS infrastructure

\- Helm-based Kubernetes deployment

\- GitOps deployment with Argo CD

\- Automated sync, pruning, and self-healing

\- Kubernetes HPA-based autoscaling

\- Kubernetes Secret-based database credentials

\- Prometheus and Grafana monitoring with alerting





\## CI/CD Flow



```text

Git Push

&#x20;  ↓

GitHub Actions

&#x20;  ↓

Lint → Test → Docker Build → Trivy Scan

&#x20;  ↓

AWS OIDC

&#x20;  ↓

Push Image to ECR

&#x20;  ↓

Update Helm Image Tag

&#x20;  ↓

Argo CD

&#x20;  ↓

Kubernetes Deployment

```





\## Project Outcome



The platform provides an automated path from source-code changes to a tested and security-scanned container image, secure AWS image publishing, GitOps-based Kubernetes deployment, autoscaling, monitoring, and self-healing.

