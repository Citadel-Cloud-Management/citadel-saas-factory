# Compliance Framework

Enterprise compliance for the Citadel SaaS Factory. Covers security, privacy, financial, and industry-specific regulations.

## Structure

```
compliance/
├── frameworks/          # Framework definitions and control mappings
│   ├── soc2.yaml        # SOC 2 Type I/II controls
│   ├── gdpr.yaml        # GDPR data protection
│   ├── ccpa.yaml        # CCPA/CPRA privacy
│   ├── hipaa.yaml       # HIPAA (conditional)
│   ├── pci_dss.yaml     # PCI DSS payment security
│   ├── iso27001.yaml    # ISO 27001 ISMS
│   ├── owasp.yaml       # OWASP Top 10
│   └── nist_ai.yaml     # NIST AI RMF + EU AI Act
├── policies/            # Required policy documents
│   ├── security.yaml    # Information security policy
│   ├── privacy.yaml     # Data privacy policy
│   ├── access.yaml      # Access control policy
│   ├── incident.yaml    # Incident response plan
│   └── retention.yaml   # Data retention policy
├── checklists/          # Audit-ready checklists
│   ├── pre_launch.yaml  # Pre-launch compliance checklist
│   └── quarterly.yaml   # Quarterly compliance review
├── automation/          # Automated compliance checks
│   └── scanner.py       # Python compliance scanner
└── evidence/            # Evidence collection (gitignored in prod)
    └── .gitkeep
```

## Quick Start

```bash
# Run compliance scan
python compliance/automation/scanner.py

# Check specific framework
python compliance/automation/scanner.py --framework soc2

# Generate evidence report
python compliance/automation/scanner.py --report
```

## Priority Order

1. SOC 2 Type I → Type II
2. GDPR + CCPA compliance
3. PCI DSS (via Stripe tokenization)
4. OWASP + Secure SDLC
5. Legal policies (ToS, Privacy, DPA)
