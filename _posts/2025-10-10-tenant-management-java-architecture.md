---
title: "Tenant Management Java Stack: System Architecture"
date: 2025-10-10
categories: [Learning, Architecture, System Design]
tags: [spring-boot, react, system-architecture, layered-architecture, modular-monolith, api-design, postgres, docker, deployment]
content_type: "architecture-analysis"
learning_focus: ["spring-boot-architecture", "react-integration", "layered-architecture", "deployment-strategy"]
difficulty: "intermediate"
mermaid: true
# Evolutionary Project Fields
project: "Tenant Management"
project_type: "evolutionary"
evolution: "Evolution 3: Java Enterprise Stack"
evolution_number: 3
evolution_focus: "Spring Boot Migration"
---

Building on the hands-on migration I shared in [Tenant Management App: Spring Boot and React Transition](/learning/development/java/tenant-management-java-transition/), this post documents the **current architecture baseline** for the new Java-based system. Right now the focus is scaffolding: wiring Spring Boot, Flyway, and the React frontend so the upcoming feature work has a solid foundation, while still keeping the modular principles from the earlier [modular monolith evolution](/learning/architecture/refactoring/tenant-management-modular-monolith/) in sight.

> **Evolution Context**: This post is part of [Evolution 3: Java Enterprise Stack](/projects/tenant-management/evolution-3/) in the [Tenant Management Evolutionary Project](/projects/tenant-management/). This evolution focuses on enterprise patterns and Spring Boot migration, building upon the modular architecture established in [Evolution 2](/projects/tenant-management/evolution-2/).

## System Architecture Overview

The application is still a single deployable unit, but each layer now has its own responsibilities. Spring Boot handles the API shell, Flyway protects the schema, and the React client keeps the presentation layer independent while the Java endpoints come online.

```mermaid
graph TB
    subgraph "Client Layer"
        react["React SPA"]
    end

    subgraph "API Layer"
        spring["Spring Boot Application"]
        flyway["Flyway Migrations"]
        jpa["Spring Data JPA"]
    end

    subgraph "Database Layer"
        h2["H2 (dev profile)"]
        postgres["PostgreSQL (prod profile)"]
    end

    subgraph "Infrastructure Layer"
        actuator["Spring Boot Actuator"]
        compose["Docker Compose"]
    end

    react -->|HTTP/JSON| spring
    spring --> jpa
    flyway --> h2
    flyway --> postgres
    jpa --> h2
    jpa --> postgres
    spring --> actuator
    compose --> spring
    compose --> react
    compose --> postgres

    %% Styling
    classDef frontend fill:#4fc3f7,stroke:#0277bd,stroke-width:3px,color:#000
    classDef backend fill:#66bb6a,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef database fill:#42a5f5,stroke:#1565c0,stroke-width:3px,color:#fff
    classDef infrastructure fill:#ff7043,stroke:#d84315,stroke-width:3px,color:#fff

    class react frontend
    class spring,jpa,flyway backend
    class h2,postgres database
    class actuator,compose infrastructure
```

## Layered Architecture Principles

1. **Presentation Layer (React SPA)** – Create React App with Material UI mirrors the existing UX and communicates via axios while the new endpoints are being built.
2. **API Layer (Spring Boot)** – The `TenantManagementApplication` bootstrap loads Spring Web, Validation, Data JPA, Actuator, Flyway, and Springdoc so controllers can be dropped in with minimal ceremony.
3. **Persistence Layer** – Flyway migrations rebuild the schema and seed data; Spring Data JPA is ready for repositories once the domain is ported.
4. **Database Layer** – H2 backs development runs, while Docker Compose can attach PostgreSQL when a production-like environment is needed.
5. **Infrastructure Layer** – Docker Compose orchestrates the services; Actuator exposes `/actuator/health` and friends for container checks and future monitoring.

## Application Architecture

```mermaid
graph TD
    subgraph Web Layer
        controllers["Controllers<br/>tenant/property/transaction"]
        advice["GlobalExceptionHandler"]
    end

    subgraph Service Layer
        tenantSvc["TenantService"]
        propertySvc["PropertyService"]
        transactionSvc["TransactionService"]
    end

    subgraph Persistence Layer
        tenantRepo["TenantRepository"]
        propertyRepo["PropertyRepository"]
        transactionRepo["TransactionRepository"]
        domain["Domain Entities"]
    end

    controllers --> tenantSvc
    controllers --> propertySvc
    controllers --> transactionSvc
    advice --> controllers

    tenantSvc --> tenantRepo
    tenantSvc --> propertyRepo
    tenantSvc --> transactionRepo

    propertySvc --> propertyRepo
    transactionSvc --> transactionRepo

    tenantRepo --> domain
    propertyRepo --> domain
    transactionRepo --> domain

    %% Styling
    classDef web fill:#4fc3f7,stroke:#0277bd,stroke-width:3px,color:#000
    classDef service fill:#66bb6a,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef repo fill:#42a5f5,stroke:#1565c0,stroke-width:3px,color:#fff

    class controllers,advice web
    class tenantSvc,propertySvc,transactionSvc service
    class tenantRepo,propertyRepo,transactionRepo,domain repo
```

This mirrors the current package layout: `web/` hosts controllers and exception handling, `service/` contains transactional logic, and `repository/` bridges into the domain entities generated by Flyway.

## Component Connections

```mermaid
graph LR
    react["React Components<br/>(Navigation, Tenants, Properties, Transactions)"]
    axiosClient["Axios HTTP Calls"]
    restApi["/api/** Endpoints<br/>(Tenant/Property/Transaction)"]
    services["Business Services"]
    repositories["Spring Data Repositories"]
    flyway["Flyway Seeded Schema"]
    database["H2 / PostgreSQL"]

    react --> axiosClient --> restApi --> services --> repositories --> database
    flyway --> database

    %% Styling
    classDef frontend fill:#4fc3f7,stroke:#0277bd,stroke-width:3px,color:#000
    classDef backend fill:#66bb6a,stroke:#2e7d32,stroke-width:3px,color:#fff
    classDef database fill:#42a5f5,stroke:#1565c0,stroke-width:3px,color:#fff

    class react,axiosClient frontend
    class restApi,services,repositories,flyway backend
    class database database
```

The diagram highlights the runtime flow: React screens call the axios client, which targets the REST controllers. Those controllers delegate to Spring services and repositories, while Flyway keeps the database schema aligned across H2 and PostgreSQL profiles.

## Backend Architecture Details

```java
// backend/src/main/java/com/example/tenantmanagement/TenantManagementApplication.java
@SpringBootApplication
public class TenantManagementApplication {
    public static void main(String[] args) {
        SpringApplication.run(TenantManagementApplication.class, args);
    }
}
```

- **Auto-configuration** brings the required Spring starters online so the next increment (controllers, services, repositories) only has to focus on domain logic.
- **Profile-aware Bootstrapping** lets the same binary target H2 or PostgreSQL by toggling the `SPRING_PROFILES_ACTIVE` environment variable.
- **Flyway-first approach** ensures schema consistency before any Java entities are introduced.

## Frontend Integration

```jsx
// frontend/src/components/Tenants.js
const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const payload = toPayload(form);
    if (editingId) {
      await axios.put(`/api/tenants/${editingId}`, payload);
      toast.success('Tenant updated');
    } else {
      await axios.post('/api/tenants', payload);
      toast.success('Tenant added');
    }
    setForm(initialForm);
    setEditingId(null);
    setOpenForm(false);
    fetchTenants();
  } catch (e) {
    toast.error('Save failed');
  }
};
```

- **Axios-powered CRUD**: The frontend now performs full create/update operations through the Spring Boot API (`POST`/`PUT` calls) and refreshes the tenant list via `fetchTenants`.
- **Material UI UX**: Tables, dialogs, pagination, and icons from `@mui/material` and `@mui/icons-material` remain the backbone of the interface, aligning with the existing design system.
- **Toast-driven Feedback**: `react-hot-toast` surfaces success and error states for every API interaction, matching the patterns established in earlier versions.

## Deployment and Operations

```yaml
# docker-compose.yml
services:
  api:
    build: ./backend
    container_name: tenantmgmt_api
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: ${PROFILE:-dev}
      SPRING_DATASOURCE_URL: jdbc:postgresql://db:5432/tenantdb
      SPRING_DATASOURCE_USERNAME: tenant
      SPRING_DATASOURCE_PASSWORD: tenant
    volumes:
      - h2-data:/app/data
  frontend:
    build: ./frontend
    container_name: tenant-management-frontend
    ports:
      - "3000:3000"
    depends_on:
      - api
  db:
    image: postgres:16
    container_name: tenantmgmt_db
    profiles:
      - prod
    environment:
      POSTGRES_DB: tenantdb
      POSTGRES_USER: tenant
      POSTGRES_PASSWORD: tenant
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
  h2-data:
```

- **Profile Switching** – Running `docker compose up` defaults to the dev/H2 profile; setting `PROFILE=prod` introduces the Postgres container.
- **Actuator Health Checks** – `/actuator/health` is exposed by default so Compose (or a future orchestrator) can monitor the API container.
- **Shared Volume for H2** – The `h2-data` volume keeps the embedded H2 database files available between runs.

## Looking Ahead

- **Expose REST Controllers** – Port the Flask CRUD endpoints to Spring MVC and wire them to repositories.
- **springdoc OpenAPI UI** – Configure the already-added dependency so API docs spin up automatically with the new endpoints.
- **Automated Tests** – Add Testcontainers-based integration tests to validate the Flyway migrations and repository interactions.
- **Observability Enhancements** – Layer in Micrometer with Prometheus/Grafana once the service starts processing real workload metrics.

This baseline keeps the independence and discoverability goals of the blog framework while pushing the Tenant Management project toward an enterprise-ready Java stack. Upcoming posts will cover domain-driven refinements, CI/CD automation, and production deployment experiments.

## Key Learnings

- **Layered Architecture**: Spring Boot's layered approach provides clear separation of concerns while maintaining flexibility
- **Database Migration**: Flyway ensures schema consistency across development and production environments
- **Containerization**: Docker Compose orchestration enables consistent development and deployment workflows
- **Profile Management**: Environment-specific configurations support different deployment scenarios
- **Enterprise Patterns**: Spring Boot's convention-over-configuration approach accelerates development while maintaining quality

## Evolution Progression

This architecture represents a significant advancement in the evolutionary journey:
- **From Evolution 2**: Built upon the modular monolith architecture and service layer patterns
- **To Evolution 3**: Introduced enterprise-ready patterns, containerization, and Java ecosystem depth
- **Next Steps**: Focus on REST API implementation, testing strategies, and production deployment

{% include evolution/evolution-posts.html %}

{% include evolution/post-navigation.html %}

## Conclusion

This architecture keeps the independence and discoverability goals of the blog framework while pushing the Tenant Management project into an enterprise-ready Java stack. Upcoming posts will cover domain-driven refinements, CI/CD automation, and production deployment experiments.
