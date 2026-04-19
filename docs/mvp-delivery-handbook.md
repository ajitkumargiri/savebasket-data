# SaveBasket MVP Delivery Handbook

## Purpose

This document turns the MVP idea into an execution-ready product plan.

It defines:

- all MVP components
- the responsibility of each component
- deployment strategy
- testing strategy
- acceptance criteria
- sprint structure
- demo structure
- operational requirements
- the cheapest realistic way to go live on Hetzner

This document should be used together with [docs/mvp-blueprint.md](/workspaces/savebasket-scraper/docs/mvp-blueprint.md).

## Product Definition

### Product Goal

Build a human-assisted grocery comparison application that helps a user answer one question:

Which single supermarket is cheapest for my basket after active offers are applied?

### MVP Promise

The MVP must prove these product capabilities:

- compare baskets across ALDI, Jumbo, Vomar, and AH
- support selected categories only
- use automated imports where reliable
- use manual imports where automation is fragile
- apply trusted active offers
- show the cheapest complete basket clearly

### MVP Constraints

The product intentionally accepts these constraints:

- AH comes from saved HTML imports, not live scraping as the main path
- offers come from manually prepared JSON, not OCR
- only a few categories are in scope
- the basket is compared per single store, not split across stores

## Complete Component Inventory

## Frontend Components

### App-Level Components

- `App`
  Responsibility: initialize routing, providers, global error boundary, and app boot sequence.
- `Layout`
  Responsibility: render page shell, navigation, footer, and a stable frame around every screen.
- `Header`
  Responsibility: expose brand, category entry points, basket summary, and data freshness indicator.
- `GlobalErrorBoundary`
  Responsibility: catch unhandled UI failures and show a controlled fallback.
- `ToastProvider`
  Responsibility: success and error notifications for user actions.

### User-Facing Pages

- `SearchPage`
  Responsibility: search products, filter by category, preview offers, and add items to basket.
- `BasketPage`
  Responsibility: review basket items, change quantities, remove products, and trigger comparison.
- `ComparisonPage`
  Responsibility: show totals by store, applied offers, missing items, and cheapest store.
- `StoreCoveragePanel`
  Responsibility: explain which stores carry the selected products.
- `StaleDataBanner`
  Responsibility: warn the user if imported data is old.

### Internal Pages

- `ImportStatusPage`
  Responsibility: show latest run per store, failures, stale imports, and record counts.
- `AhImportPage`
  Responsibility: start or review AH saved HTML imports.
- `OfferImportPage`
  Responsibility: upload or submit manual offer JSON and review validation status.
- `OpsDashboardPage`
  Responsibility: very small internal operational view for health, backups, and import freshness.

### Search Flow Components

- `ProductSearchInput`
  Responsibility: debounced query capture and validation.
- `CategoryFilter`
  Responsibility: enforce MVP category boundaries.
- `SearchResultsList`
  Responsibility: render search results consistently.
- `ProductCard`
  Responsibility: render a canonical product with basket action and store availability snapshot.
- `StorePricePreview`
  Responsibility: show current store-specific prices for one canonical product.
- `OfferBadge`
  Responsibility: show that active discount data exists.
- `MissingStoreBadge`
  Responsibility: show when a store does not currently carry a product.

### Basket Flow Components

- `BasketList`
  Responsibility: render all selected basket items.
- `BasketItem`
  Responsibility: display one product in basket with quantity, actions, and price summary.
- `QuantityControl`
  Responsibility: increment, decrement, and direct quantity edits.
- `BasketSummaryPanel`
  Responsibility: total basket item count and compare action.
- `BasketEmptyState`
  Responsibility: guide the user back to search if no items are selected.

### Comparison Flow Components

- `ComparisonSummary`
  Responsibility: headline outcome and chosen winner.
- `StoreComparisonCard`
  Responsibility: render one store's result block.
- `PriceBreakdownRow`
  Responsibility: show base total, savings, and final total.
- `AppliedOfferList`
  Responsibility: show which offers were applied and what they saved.
- `MissingProductNotice`
  Responsibility: explain incomplete basket status.
- `WinnerBanner`
  Responsibility: highlight the cheapest complete basket.
- `CompareAgainAction`
  Responsibility: send user back to basket editing.

### Frontend State Modules

- `searchStore`
  Responsibility: query state, filters, results, loading, pagination.
- `basketStore`
  Responsibility: canonical products selected by user and quantities.
- `comparisonStore`
  Responsibility: latest compare result, loading state, and compare errors.
- `systemStore`
  Responsibility: store freshness, API health, internal feature flags.

### Frontend Infrastructure Modules

- `apiClient`
  Responsibility: shared HTTP client configuration, auth headers for internal views, and error normalization.
- `queryCache`
  Responsibility: cache product search and store status requests.
- `formatters`
  Responsibility: currency, date, quantity, and store label formatting.
- `routeConfig`
  Responsibility: central route definitions and protected route metadata.

## Backend Components

### API Routers

- `products_router`
  Responsibility: product search and product detail endpoints.
- `basket_router`
  Responsibility: basket comparison input validation and response delivery.
- `imports_router`
  Responsibility: price imports, AH saved HTML imports, import run history.
- `offers_router`
  Responsibility: manual offer import and active offer listing.
- `stores_router`
  Responsibility: store listing and freshness status.
- `health_router`
  Responsibility: liveness, readiness, version, and import freshness summary.

### Service Layer

- `product_service`
  Responsibility: product search across canonical products and store coverage.
- `comparison_service`
  Responsibility: compute totals, apply valid offers, rank complete baskets, mark missing items.
- `import_service`
  Responsibility: validate imports, persist raw paths, normalize records, and upsert current data.
- `ah_import_service`
  Responsibility: parse saved AH HTML and produce normalized records.
- `offer_service`
  Responsibility: validate manual offer JSON, link offers, expose active discounts.
- `matcher_service`
  Responsibility: map store products to canonical products with strict confidence rules.
- `freshness_service`
  Responsibility: determine if store data is fresh, stale, or failed.
- `audit_service`
  Responsibility: write import lifecycle and decision events for debugging.

### Repository Layer

- `store_repository`
  Responsibility: fetch and update store records.
- `canonical_product_repository`
  Responsibility: search and create canonical products.
- `store_product_repository`
  Responsibility: persist store-specific product listings.
- `price_repository`
  Responsibility: current price upserts and store price lookup.
- `offer_repository`
  Responsibility: offer deduplication, validity filtering, and offer retrieval.
- `import_run_repository`
  Responsibility: import run start, completion, counts, and failure records.

### Data Processing Components

- `name_normalizer`
  Responsibility: clean raw product names into comparable normalized names.
- `quantity_parser`
  Responsibility: extract quantity value and unit.
- `price_parser`
  Responsibility: parse and validate price values.
- `category_mapper`
  Responsibility: map raw source categories to the MVP category taxonomy.
- `alias_map`
  Responsibility: maintain manual name equivalence for frequent matching problems.
- `manual_review_queue`
  Responsibility: hold uncertain matches and uncertain offers for later review.

### Background Jobs

- `run_aldi_import`
  Responsibility: collect, normalize, persist, and log ALDI data.
- `run_jumbo_import`
  Responsibility: collect, normalize, persist, and log Jumbo data.
- `run_vomar_import`
  Responsibility: collect, normalize, persist, and log Vomar data.
- `run_ah_html_import`
  Responsibility: parse a saved AH HTML file and persist results.
- `run_offer_import`
  Responsibility: validate and persist manual offers.
- `run_cleanup_job`
  Responsibility: rotate old temporary artifacts and expired files.
- `run_backup_job`
  Responsibility: generate and copy database and file backups.

## Responsibility Boundaries

### Frontend Is Responsible For

- search interactions
- basket state
- compare action
- displaying totals and offers
- making stale data visible
- internal ops screens for non-technical users

### Frontend Is Not Responsible For

- matching logic
- discount calculations beyond display
- truth of inventory or prices
- offer validation

### Backend Is Responsible For

- input validation
- matching logic
- offer application logic
- persistence and freshness
- internal endpoint protection
- deterministic compare results

### Backend Is Not Responsible For

- OCR automation
- split-basket optimization
- user accounts in MVP
- long-term analytics or history views

### Operations Is Responsible For

- daily automation for ALDI, Jumbo, Vomar
- manual AH and offer import workflows
- backups
- HTTPS
- uptime
- rollback path

## What Else The MVP Needs That Teams Often Miss

These are common gaps that should be designed up front.

### Internal Authentication

Even without end-user accounts, internal import endpoints must be protected.

Minimum acceptable MVP protection:

- API key for internal POST endpoints
- basic auth for internal ops pages
- secret stored in environment variables only

### Data Freshness Rules

The app must know whether data is fresh.

Suggested freshness policy:

- automated store data is fresh for 24 hours
- AH data is fresh until the next planned manual import window or 24 hours, whichever is shorter
- offers are valid only between `valid_from` and `valid_to`

### Failure Handling

The product must never silently replace good data with bad data.

Rules:

- if an import fails, keep last good current prices
- if matching confidence is low, keep product unmatched
- if offer confidence is low, keep offer inactive or pending
- if compare request sees missing data, return incomplete result explicitly

### Traceability

Every import should be traceable.

Minimum traceability requirements:

- raw source path
- normalized output path
- import run id
- counts for seen, valid, matched records
- failure reason if import failed

### Release Safety

Before each production release:

- migrations must be backward-safe for the current deploy
- smoke tests must pass
- rollback instructions must exist

### Backup and Restore Drill

You should not only back up data. You should verify restore once before public launch.

## Deployment Plan

## Cheapest Way To Go Live On Hetzner

Because you already have a Hetzner server, the cheapest acceptable production architecture is a single-server deployment.

### Recommended Setup

- use the existing Hetzner server
- run everything via Docker Compose
- serve frontend static assets from Caddy
- run FastAPI behind Caddy
- run PostgreSQL on the same server
- store raw imports and manifests on the server filesystem
- schedule imports with cron or systemd timers

### Why This Is Cheapest

- no extra cloud vendors
- no managed database monthly cost
- no separate Vercel or Render bill
- no Kubernetes overhead
- no multi-host network complexity

### Suggested Runtime Topology

```text
Public Internet
  -> Caddy
      -> Frontend static files
      -> FastAPI API
          -> PostgreSQL
          -> Local import storage
          -> Scheduled jobs
```

### Minimum Practical Server Size

Recommended minimum for a stable MVP:

- 2 vCPU
- 4 GB RAM
- SSD storage with room for raw files and backups

If your existing Hetzner server is smaller, you can still try it, but imports and PostgreSQL may contend for memory.

### Recommended Software Stack

- Ubuntu
- Docker Engine
- Docker Compose
- Caddy
- FastAPI with Uvicorn workers
- PostgreSQL
- cron or systemd timer

### Suggested Containers

- `caddy`
- `frontend`
- `backend`
- `postgres`
- optional `scheduler`

If you want the absolute cheapest setup, skip a separate scheduler container and use host cron.

### Static Frontend Strategy

To reduce cost and complexity:

- build the frontend into static assets
- serve those static files directly from Caddy
- avoid SSR in MVP unless required by SEO, which this product does not need initially

### Database Strategy

For MVP, keep PostgreSQL on the same server.

That is acceptable because:

- traffic is low
- data size is moderate
- operational simplicity matters more than isolation right now

### TLS and Domain

- point domain to Hetzner server
- use Caddy automatic TLS
- expose only ports 80 and 443 publicly
- keep PostgreSQL internal only

### Backups

Required backups:

- nightly `pg_dump`
- daily copy of raw imports and manifests
- at least 7 to 14 days retention

Cheapest off-server backup option:

- Hetzner Storage Box

### Logging and Monitoring

For MVP, use simple monitoring.

Minimum set:

- `/health` uptime check
- alert on failed import job
- alert on low disk space
- rotated logs on host

### Security Hardening

- SSH keys only
- firewall enabled
- fail2ban optional if you already use it
- internal endpoints behind API key or basic auth
- secrets in environment variables, never committed
- upload size limits for HTML and JSON

### Deployment Process

1. build frontend assets
2. build backend image
3. run automated tests
4. run migrations
5. deploy with Docker Compose
6. run health check
7. run smoke compare request
8. verify import status page

### Rollback Process

1. keep previous image tags
2. restore previous Compose version
3. revert migrations only if they are explicitly reversible and safe
4. restore latest backup if data corruption happened

## Testing Strategy

## Automated Tests

### Unit Tests

Required unit tests:

- name normalization
- quantity parsing
- price parsing
- offer discount calculation
- complete basket ranking
- incomplete basket ranking
- freshness calculation
- matching score thresholds

### Integration Tests

Required integration tests:

- price import writes store products and current prices
- AH saved HTML import produces normalized rows
- manual offer import writes only valid offers
- compare endpoint returns expected totals
- store status endpoint reflects import freshness

### Fixture Tests

Keep fixture files for:

- ALDI normalized import sample
- Jumbo normalized import sample
- Vomar normalized import sample
- AH saved HTML sample
- manual offer JSON sample
- expected compare result sample

### End-To-End Tests

Minimum E2E flows:

- search -> add to basket -> compare
- import offer -> compare with discount
- import AH HTML -> search imported product -> compare

## Manual QA

Manual QA is mandatory for this MVP.

### Manual QA Checklist

- verify 20 target products by hand across stores
- verify 5 sample offers by hand
- verify 1 basket per selected category by hand
- verify stale data warning appears when expected
- verify missing-product messaging is understandable
- verify public compare flow on mobile and desktop

## Release Gate

Before each sprint demo and production deployment, run:

1. unit tests
2. integration tests
3. one E2E basket comparison
4. manual QA sample basket
5. health endpoint check after deploy

## Acceptance Criteria

## Ingestion Acceptance Criteria

- ALDI import works end to end for selected categories
- Jumbo import works end to end for selected categories
- Vomar import works end to end for selected categories
- AH saved HTML import works end to end for selected categories
- every import writes import run metadata
- failed imports preserve previous current price data

## Data Quality Acceptance Criteria

- every live price row has a valid store, product, price, and timestamp
- low-confidence matches are not auto-linked
- at least the top target products are matched correctly across stores
- active offers are only applied when linkage is trusted

## Search Acceptance Criteria

- user can search by name
- user can filter by selected categories
- results show enough context to add the right product to basket
- search returns within acceptable speed for MVP data size

## Basket Acceptance Criteria

- user can add products to basket
- user can edit quantities
- user can remove products
- basket persists at least locally during session

## Comparison Acceptance Criteria

- compare returns totals for all four stores
- compare returns missing items per store
- compare returns applied offers per store
- cheapest store is selected only among complete baskets
- if no store has a complete basket, the UI explains that clearly

## Offer Acceptance Criteria

- internal user can import offer JSON without code changes
- invalid offers are rejected clearly
- expired offers are not applied
- trusted offers affect final totals correctly

## Operational Acceptance Criteria

- app is available over HTTPS
- health endpoint works
- daily automated imports run
- manual AH and offer imports are usable by an internal operator
- backups run nightly
- one restore test has been performed before public launch

## Demo Acceptance Criteria

At the end of the MVP cycle, the team must be able to demonstrate:

1. one automated store import
2. one AH saved HTML import
3. one manual offer import
4. product search
5. basket building
6. basket comparison across four stores
7. visible savings from active offers
8. cheapest complete basket selection

## Sprint Model

Use weekly sprints with a demo every week.

## Sprint 0: Architecture And Scope Freeze

### Goals

- lock categories
- lock contracts
- lock deployment target
- lock acceptance criteria

### Deliverables

- approved schema
- approved API contracts
- approved deployment topology
- prioritized backlog

### Demo

- architecture review and contract review

### Exit Criteria

- no open MVP scope ambiguity
- next sprint backlog ready

## Sprint 1: Ingestion Foundation

### Goals

- persist data from ALDI, Jumbo, Vomar, and AH into one schema

### Deliverables

- migrations
- import endpoints
- raw artifact storage
- manifest generation
- AH saved HTML import flow
- import status endpoint

### Demo

- successful import run for all four stores
- import history screen or API output

### Exit Criteria

- all four import paths working for selected categories
- failed import does not corrupt live data

## Sprint 2: Matching And Comparison Core

### Goals

- make product comparison trustworthy

### Deliverables

- canonical product mapping
- strict matching rules
- manual review queue model
- basket comparison service
- compare endpoint
- missing item handling

### Demo

- compare one real basket across four stores
- show incomplete basket handling

### Exit Criteria

- deterministic compare responses
- complete baskets ranked correctly

## Sprint 3: Offers And Frontend MVP

### Goals

- make the product usable by a real tester

### Deliverables

- offer import endpoint
- active offer retrieval
- search page
- basket page
- comparison page
- mobile-friendly layout

### Demo

- search -> basket -> compare -> savings displayed

### Exit Criteria

- core user journey works end to end
- trusted offers change final totals correctly

## Sprint 4: Hardening And Go Live

### Goals

- ship a stable MVP on Hetzner

### Deliverables

- production Compose deployment
- HTTPS and domain setup
- backup job
- health endpoint
- import scheduling
- smoke tests and QA pass
- basic ops page

### Demo

- live product demo from production environment

### Exit Criteria

- production deployment stable
- backups configured
- all MVP acceptance criteria met

## Sprint Demo Format

Each sprint demo should include:

1. planned scope
2. shipped scope
3. live walkthrough
4. issues discovered
5. decisions needed for next sprint

## Ticket Structure For Sprint Planning

Every ticket should contain:

- ticket goal
- business reason
- dependencies
- technical design impact
- acceptance criteria
- demo evidence expected

## MVP Workstreams For Backlog Creation

Organize backlog into these epics:

1. ingestion and raw artifacts
2. persistence and schema
3. matching and canonical products
4. AH manual import
5. offers import and validation
6. basket comparison engine
7. frontend product flow
8. deployment and operations
9. testing and QA

## Recommended Next Step

The best next step is to convert this handbook into a sprint backlog and then start with Sprint 0 deliverables.

The first implementation order should be:

1. schema and migrations
2. import contracts and validators
3. ALDI, Jumbo, Vomar persistence path
4. AH saved HTML import path
5. comparison engine
6. offer import path
7. frontend MVP
8. production deployment
