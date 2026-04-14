# ADR-005: Linkerd as Service Mesh

## Status

Accepted

## Context

Citadel SaaS Factory requires a service mesh that:

- Provides mutual TLS (mTLS) for all service-to-service communication
- Adds observability (latency, success rate, request volume) without code changes
- Has minimal resource overhead (suitable for K3s on low-cost infrastructure)
- Supports traffic splitting for canary deployments
- Is open source with no enterprise licensing requirements

The primary candidates evaluated were Linkerd, Istio, and Consul Connect.

## Decision

We chose **Linkerd** as the service mesh.

### Key Reasons

1. **Lightweight**: Linkerd's data plane proxy (linkerd2-proxy) is written in Rust and consumes approximately 10MB of memory per pod, compared to Istio's Envoy proxy at approximately 50-100MB. This is critical for running on resource-constrained K3s nodes.

2. **Automatic mTLS**: Linkerd automatically encrypts all service-to-service communication with mTLS. No application code changes or certificate management are required. Certificates are automatically rotated every 24 hours.

   ```bash
   # Inject Linkerd proxy into a deployment
   kubectl get deploy citadel-backend -n production -o yaml \
     | linkerd inject - \
     | kubectl apply -f -
   ```

3. **Observability out of the box**: Linkerd provides golden metrics (success rate, request rate, latency percentiles) per service and per route without any application instrumentation.

   ```bash
   # View live metrics
   linkerd viz stat deploy -n production
   linkerd viz top deploy/citadel-backend -n production
   ```

4. **Rust-based proxy**: The Linkerd2-proxy is written in Rust, providing memory safety guarantees and predictable performance without garbage collection pauses. This contributes to its low latency overhead (sub-millisecond p99 added latency).

5. **Simplicity**: Linkerd has a smaller API surface and fewer configuration options than Istio, making it easier to operate and debug. Installation is a single command:

   ```bash
   linkerd install | kubectl apply -f -
   linkerd check
   ```

6. **Traffic splitting**: Linkerd supports traffic splitting via TrafficSplit CRD (SMI spec), enabling canary deployments and A/B testing at the mesh level.

   ```yaml
   apiVersion: split.smi-spec.io/v1alpha2
   kind: TrafficSplit
   metadata:
     name: citadel-backend
   spec:
     service: citadel-backend
     backends:
       - service: citadel-backend-stable
         weight: 950
       - service: citadel-backend-canary
         weight: 50
   ```

## Consequences

### Positive

- All inter-service traffic is encrypted by default (zero-trust networking)
- Per-service and per-route metrics available without code changes
- Minimal resource overhead suitable for K3s on small VPS instances
- Rust proxy provides memory safety and predictable performance
- Simple operational model compared to Istio
- CNCF graduated project with long-term community support

### Negative

- Fewer features than Istio (no built-in rate limiting, no advanced traffic policies)
- Smaller ecosystem of extensions and integrations
- TrafficSplit CRD is less flexible than Istio's VirtualService for advanced routing
- Linkerd viz dashboard requires additional installation (not included in core)

### Mitigations

- Use Traefik for ingress-level rate limiting (complements Linkerd's mesh-level features)
- Deploy Linkerd viz extension for the observability dashboard
- Use Kyverno for network policies that Linkerd does not cover
- Monitor the Linkerd roadmap for feature additions (rate limiting is under discussion)
