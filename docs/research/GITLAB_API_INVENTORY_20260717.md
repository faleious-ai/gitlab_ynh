# GitLab API inventory for MCP planning

Status: `STRUCTURALLY_OBSERVED` — research artifact, not an implementation or capability promise.

Round: `RND-20260717-015`
Task: `T-MCP-02-api-inventory`

## Authority and transport

The official REST documentation defines the versioned API surface under `/api/v4`. The official GraphQL documentation defines the versionless endpoint `/api/graphql`. This inventory records the transport and policy facts needed to design a catalog; it does not claim that every operation is available on every GitLab instance.

Sources:

- REST: <https://docs.gitlab.com/api/rest/>
- GraphQL: <https://docs.gitlab.com/api/graphql/>

## REST operation inventory

The rows below are the first read-oriented catalog slice. Paths are official REST shapes; availability, response schema, edition and license must be checked against the target instance before an MCP tool is enabled.

| Operation ID | Method/path | Minimum access | Pagination/volume | Mutability | Risk | MCP state |
|---|---|---|---|---|---|---|
| `rest.projects.list` | `GET /projects` | `read_api` when authentication is required | page or keyset; cap client page at 100 | read | `R0_READ` | research-only |
| `rest.project.get` | `GET /projects/:id` | `read_api` when authentication is required | single resource | read | `R0_READ` | research-only |
| `rest.repository.tree.list` | `GET /projects/:id/repository/tree` | `read_api` | page or keyset where offered; bounded page | read | `R0_READ` | research-only |
| `rest.repository.branches.list` | `GET /projects/:id/repository/branches` | `read_api` | page or keyset where offered; bounded page | read | `R0_READ` | research-only |
| `rest.merge_requests.list` | `GET /projects/:id/merge_requests` | `read_api` | page or keyset; bounded page | read | `R0_READ` | research-only |
| `rest.pipelines.list` | `GET /projects/:id/pipelines` | `read_api` | page or keyset; bounded page | read | `R0_READ` | research-only |
| `rest.jobs.list` | `GET /projects/:id/jobs` | `read_api` | page or keyset; traces/artifacts require streaming limits | read | `R0_READ` | research-only |
| `rest.releases.list` | `GET /projects/:id/releases` | `read_api` | page or keyset where offered; bounded page | read | `R0_READ` | research-only |
| `rest.packages.list` | `GET /projects/:id/packages` | `read_api` | page or keyset where offered; bounded page | read | `R0_READ` | research-only |

The inventory intentionally excludes write paths from the initial MCP fixture. A future write catalog must add an explicit authorization, idempotency, optimistic-concurrency and audit policy per operation. It must also reject arbitrary URLs and unknown catalog identifiers.

## GraphQL inventory

GraphQL is queried through `/api/graphql`; operation names and response fields are schema-discovered rather than assumed from a REST path. The first catalog slice should discover and describe only read queries for project metadata, repository content, merge requests, pipelines and jobs. Each discovered field needs:

- schema/type snapshot and deprecation status;
- variables and bounded connection arguments;
- cursor/page information and a client maximum of 100 items per page;
- required scope, instance version, edition/license availability and redaction policy;
- complexity and rate-limit handling;
- `R0_READ` risk and no mutation side effect.

GraphQL queries may be available without authentication, while authenticated queries use the documented read scope. Mutations require the broader API scope and remain outside this research task. No credential, query result, mutation or target-instance capability claim is persisted here.

## Policy mapping

| Concern | Required MCP behavior | Current evidence |
|---|---|---|
| Instance drift | run version/edition/capability discovery before enabling an operation | not observed against a live instance |
| Pagination | expose a bounded page/cursor and `next_page`/cursor state; never load an unbounded collection | documented transport requirement |
| Large payloads | return references or bounded streams for traces, artifacts and downloads | design requirement; no transfer performed |
| Errors | preserve safe HTTP/GraphQL category, status, operation, retryability, rate-limit metadata and trace ID | design requirement; fixture foundation covers stable JSON-RPC errors |
| Writes | separate allowlist, explicit authorization, audit and idempotency policy | deferred; no write enabled |
| Editions/licenses | record observed availability per instance instead of inferring CE/EE parity | not observed; remains an explicit discovery field |

## Limits and next gate

This is not a complete API catalog, schema dump, compatibility matrix or remote contract test. It does not prove authentication, instance capability, CE/EE parity, response freshness, rate-limit headers or GraphQL field availability. The next MCP wave must run authenticated and unauthenticated read-only contract probes against an approved fixture or target instance, record redacted responses, and keep unavailable operations classified rather than silently omitting them.
