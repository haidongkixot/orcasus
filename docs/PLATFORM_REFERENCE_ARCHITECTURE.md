# Platform Reference Architecture

This document is a starting hypothesis for complex modular web/mobile platforms, not a universal stack mandate. Run Project Discovery before applying it to any existing repository.

## Principles
- Prefer a modular monolith for a new platform until deployment independence, team topology, throughput or domain isolation justify separate services.
- Separate platform primitives, domain modules and product-specific capabilities.
- Define stable contracts and dependency direction between modules.
- Treat authentication, authorization, tenant isolation, audit history, schema migrations and observability as cross-cutting concerns.
- Design for extension without turning every field or operation into an untyped generic mechanism.
- Build one vertical slice that demonstrates UI → API → domain logic → persistence → authorization → tests before broad module expansion.

## Capability areas to evaluate
- Identity, organizations, membership and access policies
- Tenant isolation and data lifecycle
- Module registry, module dependencies and extension lifecycle
- Domain entities and explicit schema/migrations
- Metadata/custom fields where genuine flexibility is required
- Workflow, rules, background jobs and events
- Search, filters, reports, imports/exports and audit history
- External integrations and API versioning
- Mobile workflows, offline/resume and synchronization
- Administration, observability, backup and recovery

Only include capabilities supported by user needs, acceptance criteria, evidence and approved scope.

## Architecture decision gate
For material choices, compare at least two feasible options when they exist. Weigh product fit, usability, security, extensibility, migration costs, operational skills, runtime, hosting cost and reversibility. Record evidence, rejected alternatives and owner decisions in ADRs. Do not select microservices, a new framework, managed service or plugin architecture merely because the platform is ambitious.

## Resource and test readiness
Before implementation, verify current stack, assets/licenses, external APIs/scopes, data access, target environments, CI/test runner, supported devices, observability and budget. If any prerequisite is unknown or unavailable, mark it accurately and escalate material decisions.
