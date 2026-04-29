---
name: ms-cloud-security
description: Cloud security requirements for AWS/Azure/GCP — managed identities, no static credentials, MFA, RBAC, logging, private networking, WAF, threat detection, encryption. Cross-cloud security baseline.
type: standard
priority: 18
---

# Cloud Security Requirements

## Core Rule

All cloud deployments must follow security best practices regardless of provider. Default to the strictest reasonable configuration.

## Universal Requirements (All Providers)

### Identity & Access
- **Managed identities** — use cloud-native identity (IAM roles, managed identity, workload identity)
- **No static credentials** — no long-lived access keys in code, configs, or CI
- **MFA enforced** — all human accounts require MFA
- **RBAC enforced** — role-based access, no individual permissions
- **Conditional access** — location, device, risk-based policies
- **Session limits** — maximum session duration, re-auth for sensitive ops

### Logging & Monitoring
- **Cloud audit logs enabled** — all API calls logged (CloudTrail, Activity Log, Cloud Audit)
- **Log retention** — minimum 90 days hot, 1 year cold
- **SIEM integration** — forward to centralized security monitoring
- **Anomaly detection** — unusual access patterns trigger alerts

### Networking
- **Private networking** — services communicate via private endpoints
- **Minimize public exposure** — only load balancers/CDN face the internet
- **Network segmentation** — separate VPCs/VNets for prod, staging, dev
- **WAF protection** — web application firewall on all public endpoints
- **DDoS protection** — enable provider-native DDoS mitigation
- **DNS security** — DNSSEC where supported

### Encryption
- **Encryption at rest** — all storage encrypted with managed KMS
- **Encryption in transit** — TLS 1.2+ for all communications
- **Key management** — customer-managed keys for sensitive data
- **Certificate management** — automated cert rotation

### Threat Detection
- **Enable native threat detection** — GuardDuty, Defender, SCC
- **Vulnerability scanning** — VM, container, and serverless scanning
- **Compliance monitoring** — CIS benchmarks, provider security hub

## Provider-Specific Controls

### AWS
```
[ ] CloudTrail enabled in all regions
[ ] GuardDuty enabled
[ ] Security Hub with CIS benchmark
[ ] IAM Access Analyzer enabled
[ ] S3 public access blocked at account level
[ ] VPC Flow Logs enabled
[ ] EBS default encryption enabled
[ ] RDS encryption enabled
[ ] Secrets Manager for secrets (not SSM Parameter Store for sensitive data)
[ ] SCPs for organizational guardrails
```

### Azure
```
[ ] Activity Log forwarded to Log Analytics
[ ] Microsoft Defender for Cloud enabled
[ ] Azure Policy for compliance
[ ] Key Vault for secrets
[ ] Private Link for PaaS services
[ ] NSG flow logs enabled
[ ] Azure AD Conditional Access
[ ] Managed Disk encryption
[ ] SQL TDE enabled
[ ] Subscription-level resource locks
```

### GCP
```
[ ] Cloud Audit Logs enabled
[ ] Security Command Center enabled
[ ] VPC Service Controls for sensitive projects
[ ] Cloud KMS for key management
[ ] Private Google Access enabled
[ ] VPC Flow Logs enabled
[ ] Binary Authorization for GKE
[ ] Cloud Armor WAF rules
[ ] Organization policies enforced
[ ] Workload Identity for GKE
```

## Cloud Security Posture Checklist

```
[ ] No public S3 buckets / Storage blobs / GCS buckets
[ ] No overly permissive security groups / NSGs / firewall rules
[ ] No wildcard IAM policies
[ ] No default VPC in use
[ ] No unencrypted storage volumes
[ ] No public database endpoints
[ ] No long-lived access keys
[ ] No root/owner account usage for daily operations
[ ] All resources tagged (owner, environment, cost-center)
[ ] Billing alerts configured
```
