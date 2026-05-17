# AI Security by Design — Comprehensive Framework 2026

> 11 Domains | 80+ Controls | 10 LLM Threats | 15+ Tools | 8 Certifications | 30+ Resources
> Sources: IBM X-Force 2026, Verizon DBIR 2025, NIST, OWASP, MITRE, International AI Safety Report 2026

## Threat Intelligence Dashboard (2025-2026)

| Stat | Source |
|------|--------|
| **$5.72M** avg AI-powered breach cost (+13% YoY) | Verizon DBIR 2025 |
| **56%** rise in AI-related security incidents | Stanford AI Index 2025 |
| **44%** increase in public-facing app attacks | IBM X-Force 2026 |
| **80%** social engineering attacks using AI | ENISA 2025 |
| **97%** AI breach victims lacked AI access controls | IBM CODB 2025 |
| **82:1** AI agents outnumber human users | Palo Alto Networks 2026 |
| **2,000%** increase in AI-specific CVEs since 2022 | NIST NVD / OWASP 2025 |
| **$670K** extra cost of shadow AI breaches | IBM CODB 2025 |
| **32%** orgs hit by AI prompt attacks in 2025 | Security Boulevard 2025 |
| **4x** rise in supply chain compromises since 2020 | IBM X-Force 2026 |
| **11 min** avg detection time for AI-assisted breaches | Network Installers 2025 |
| **24%** enterprises with dedicated AI security team | Practical DevSecOps 2026 |

---

## 11 Security Domains

### D01: Secure Architecture Principles
- Zero Trust Architecture (ZTA) — never trust, always verify on every AI pipeline hop
- Least Privilege Access — time-bound, task-scoped JIT permissions
- Defense in Depth — WAF + API gateway + prompt guardrails + output filters + behavioral monitoring
- Immutable Infrastructure — signed container images, GitOps for all changes
- Microsegmentation — isolate training, fine-tuning, inference, embedding, vector DB
- Blast Radius Minimization — compromised model cannot pivot to unrelated systems
- AI System Inventory — continuously updated catalog of all models, agents, datasets, prompts

### D02: Data Security & Privacy
- Data Classification & Tagging — label by sensitivity before ML ingestion
- Differential Privacy — calibrated noise (Laplace/Gaussian) for membership inference prevention
- Encryption at Rest & In Transit — AES-256-GCM + mTLS 1.3
- Machine Unlearning — GDPR Article 17 compliance
- GenAI Output DLP — intercept confidential data before external AI API submission
- **Tools**: Microsoft Presidio (PII), OpenDP (differential privacy), TensorFlow Privacy (DP-SGD)

### D03: Model Security
- Model Signing — Sigstore/cosign, verify before every deployment
- Adversarial Robustness Testing — FGSM, PGD, model inversion, membership inference (ART, Foolbox)
- Backdoor Detection — Neural Cleanse, STRIP for HuggingFace models
- Continuous Red Teaming — PyRIT, Garak, Promptfoo as CI/CD gates
- Anti-Extraction Controls — output perturbation, query rate limits
- **Tools**: ProtectAI ModelScan, Garak LLM Scanner, Sigstore

### D04: LLM-Specific Security (OWASP Top 10)
- **LLM01** Prompt Injection — sanitize inputs, instruction hierarchy, structured output schemas
- **LLM02** Sensitive Info Disclosure — PII detection on outputs, deny-by-default
- **LLM03** Supply Chain — SBOM, ModelScan, signed attestations
- **LLM04** Data & Model Poisoning — statistical anomaly detection, hash verification
- **LLM05** Improper Output Handling — treat LLM output as untrusted, sandbox code execution
- **LLM06** Excessive Agency — tool allowlists, HITL gates, action budgets
- **LLM07** System Prompt Leakage — no secrets in prompts, extraction testing
- **LLM08** Vector & Embedding Weaknesses — RBAC on vector DBs, cosine similarity monitoring
- **LLM09** Misinformation — authoritative RAG, confidence scoring, citation verification
- **LLM10** Unbounded Consumption — hard token/compute budgets, circuit breakers
- **Tools**: Microsoft PyRIT (multi-turn red teaming), Promptfoo (OWASP compliance testing)

### D05: Identity & Access Management
- AI Workload Identity (SPIFFE/SPIRE) — cryptographic SVID for every model/agent
- Non-Human Identity Lifecycle — full IAM for agent credentials
- API Key Vault — HashiCorp Vault, 30-day rotation, no hardcoded keys
- Credential Exposure Monitoring — TruffleHog, GitGuardian pre-commit

### D06: Monitoring, Observability & Threat Detection
- AI-Specific SIEM — full inference request/response pairs with context
- Behavioral Baselines — 3-sigma deviation alerting
- Runtime LLM Guardrails — Guardrails AI, LlamaGuard, NeMo in real-time
- Immutable Audit Logging — cryptographic chaining
- **Tools**: Guardrails AI (50+ validators), Evidently AI (drift monitoring)

### D07: MLOps / DevSecOps for AI
- Secure CI/CD — TruffleHog + SAST + SCA + adversarial test gates
- AI-Specific SBOM — CycloneDX/SPDX via Syft
- Container Hardening — distroless images, Trivy scanning, no-root
- SLSA Level 3 Provenance — Sigstore attestations for model artifacts
- **Tools**: Trivy, Syft + Grype, Checkov

### D08: API & Integration Security
- AI-Aware WAF — prompt injection patterns, token-limit abuse detection
- Adaptive Rate Limiting — per-user, per-model, per-endpoint
- mTLS on AI Service Mesh — Istio/Linkerd between all AI microservices
- SSRF Prevention — whitelist external endpoints for AI agents

### D09: Multi-Agent & Agentic System Security
- Explicit Agent Permission Scoping — deny-by-default tool allowlists
- Code Execution Sandboxing — gVisor, Firecracker, WASM
- HITL Gates — human approval for irreversible actions
- Inter-Agent Message Signing — HMAC/asymmetric verification
- Blast Radius Isolation — network-segment agent environments
- Loop Prevention — hard action budgets, circuit breakers
- **Tools**: gVisor, CSA MAESTRO (7-layer agentic threat model)

### D10: Governance, Compliance & Ethics
- Living AI Risk Register — with enterprise GRC integration
- EU AI Act Compliance — enforced August 2026, fines up to 7% global revenue
- Bias & Fairness Audits — AIF360, Fairlearn before deployment
- AI Ethics Review Board — multi-disciplinary sign-off
- Chief AI Risk Officer (CAIRO) Function
- **Tools**: IBM AIF360, Microsoft Fairlearn

### D11: Supply Chain & Third-Party Security
- Third-Party Model Vetting — ModelScan all HuggingFace/Ollama models
- ML License Compliance — scan for copyleft/restricted licenses
- Continuous Weight Scanning — monthly re-scan with ModelScan
- **Tools**: ProtectAI ModelScan + NB Defense, pip-audit, SLSA

---

## Security Tools Arsenal

| Tool | Category | Install |
|------|----------|---------|
| PyRIT | Red Team | `pip install pyrit` |
| Garak | LLM Fuzzer | `pip install garak` |
| Promptfoo | CI/CD Testing | `npx promptfoo@latest redteam init` |
| Guardrails AI | Runtime Safety | `pip install guardrails-ai` |
| ModelScan | Supply Chain | `pip install modelscan` |
| Presidio | PII Detection | `pip install presidio-analyzer presidio-anonymizer` |
| AIF360 | Fairness/Bias | `pip install aif360` |
| Trivy | Container Security | `trivy image --severity CRITICAL,HIGH` |
| Syft + Grype | SBOM | `syft packages ./ -o cyclonedx-json` |
| OpenDP | Differential Privacy | `pip install opendp` |
| Evidently AI | Drift Monitoring | `pip install evidently` |
| TruffleHog | Credential Scanning | `trufflehog git <repo> --only-verified` |

---

## Framework Alignment

| Framework | Type | Maps To |
|-----------|------|---------|
| NIST AI RMF 1.0 | Voluntary | ISO 42001, EU AI Act, SOC 2, FedRAMP |
| OWASP LLM Top 10 (2025) | Community | NIST AI RMF, MITRE ATLAS, OWASP ASVS |
| MITRE ATLAS | Research | ATT&CK, NIST AI RMF, OWASP LLM |
| EU AI Act | Binding Law | ISO 42001, NIST AI RMF, GDPR, ISO 27001 |
| ISO/IEC 42001:2023 | Certifiable | NIST AI RMF, ISO 27001, EU AI Act, SOC 2 |
| NIST SP 800-53 Rev 5 | Federal | FedRAMP, CMMC, FISMA, ISO 27001 |
| CSA MAESTRO | Cloud/Agentic | NIST AI RMF, OWASP LLM, CSA CCM, ISO 42001 |

---

## Certifications

| Program | Provider | Level |
|---------|----------|-------|
| SEC411: AI Security Principles | SANS | All levels |
| SEC598: AI Security Red/Blue/Purple | SANS | Advanced (GIAC) |
| SEC595: Applied DS & AI/ML for Security | SANS | Intermediate (GMLE) |
| CAISP: Certified AI Security Professional | Practical DevSecOps | Lab-based |
| AI Red Teaming 101 | Microsoft Learn | Free |
| Secure AI Labs | Immersive Labs | Enterprise |
| CSA Trusted AI Safety Program | CSA + Northeastern | Self-paced |
| CSPAI: Certified Security Professional for AI | SISA/Praxis | ANAB Accredited |
