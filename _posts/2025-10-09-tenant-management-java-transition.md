---
title: "Tenant Management App: Spring Boot and React Transition"
date: 2025-10-09
categories: [Learning, Development, Java]
tags: [tenant-management, spring-boot, react, java, backend, frontend, full-stack, migration, learning]
content_type: "feature-development"
learning_focus: ["spring-boot", "react", "java-ecosystem", "full-stack-refactor"]
difficulty: "intermediate"
# Evolutionary Project Fields
project: "Tenant Management"
project_type: "evolutionary"
evolution: "Evolution 3: Java Enterprise Stack"
evolution_number: 3
evolution_focus: "Spring Boot Migration"
---

Today I kicked off a new chapter for the Tenant Management application by rebuilding it as a **React + Spring Boot** project. After exploring the Python/Flask versions, this move lets me lean into the Java ecosystem I know best while deliberately relearning Spring Boot with modern practices. This first increment focuses on getting the new stack stood up with real code, configs, and migrations—the feature parity work comes next.

> **Evolution Context**: This post is part of [Evolution 3: Java Enterprise Stack](/projects/tenant-management/evolution-3/) in the [Tenant Management Evolutionary Project](/projects/tenant-management/). This evolution focuses on enterprise patterns and Spring Boot migration, building upon the modular architecture established in [Evolution 2](/projects/tenant-management/evolution-2/).

> **Requirements Context**: This iteration still fulfills the functional goals from [Landlord-Tenant Management System: Requirements and Objectives](/learning/requirements/analysis/tenant-management-requirements/) while extending the architectural journey that started in [From Single-File to Modular Monolith: Refactoring the Tenant Management App](/learning/architecture/refactoring/tenant-management-modular-monolith/).

## Why the Stack Change Matters

- **Familiar Foundations**: Java and Spring Boot are the technologies I’ve used most professionally. Revisiting them with fresh eyes helps me sharpen fundamentals.
- **Ecosystem Depth**: Spring’s tooling (Actuator, Spring Data, validation) gives me room to explore production-ready patterns without reinventing the wheel.
- **Cross-Skill Growth**: Comparing the Flask implementation with Spring Boot highlights how similar concepts—routing, dependency injection, ORM—play out across ecosystems.

## Project Snapshot

The new repository lives at `tenant-management-java-app` and currently includes:
- **Spring Boot backend scaffolding** with Flyway migrations that recreate the Property, Tenant, and Transaction tables ready for future controllers.
- **React frontend (Create React App + MUI)** that preserves the UI flows from the modular monolith version and will call the new API once endpoints land.
- **Docker Compose wiring** that runs the Spring Boot app with H2 for development and can flip to PostgreSQL for production profiles.

## Spring Boot Modules in Play

- **spring-boot-starter-web** – Bootstraps the API application and readies the project for REST controllers as they are added.
- **spring-boot-starter-validation** – Enables Jakarta Bean Validation across incoming payloads once DTOs are in place.
- **spring-boot-starter-data-jpa** – Brings in Hibernate and paging support for the domain entities seeded by Flyway.
- **spring-boot-starter-actuator** – Provides health/metrics endpoints that already hook into the Compose setup.
- **flyway-core** – Applies the SQL migrations that recreate the schema and sample data from the previous implementation.
- **springdoc-openapi-starter-webmvc-ui** – Prepares the project for interactive API docs when the first controllers are exposed.

## Key Configuration Highlights

```properties
# backend/src/main/resources/application.properties
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.open-in-view=false
spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration
management.endpoints.web.exposure.include=health,info,metrics
server.port=8080
```

```properties
# backend/src/main/resources/application-dev.properties
spring.datasource.url=jdbc:h2:file:./data/dev-db;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.h2.console.enabled=true
```

```yaml
# docker-compose.yml (root)
services:
  api:
    build: ./backend
    environment:
      SPRING_PROFILES_ACTIVE: ${PROFILE:-dev}
      SPRING_DATASOURCE_URL: jdbc:postgresql://db:5432/tenantdb
      SPRING_DATASOURCE_USERNAME: tenant
      SPRING_DATASOURCE_PASSWORD: tenant
    ports:
      - "8080:8080"
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - api
  db:
    image: postgres:16
    profiles:
      - prod
```

## What I’m Learning Next

1. **Modern Spring Boot Patterns** – Leaning into annotations, configuration profiles, and layered architecture that scales beyond the tutorial level.
2. **React + Java Integration** – Handling auth, CRUD flows, and validation while keeping the frontend clean and responsive.
3. **Deployment Pathways** – Exploring containerized builds where a Spring Boot jar and React bundle live side-by-side in production.

## Requirement Alignment

- **Schema Parity**: Flyway migrations recreate the Property, Tenant, and Transaction tables, keeping the Java stack aligned with the original business model.
- **Seed Data**: `V2__seed.sql` loads realistic records so the frontend can keep rendering meaningful information while the API layer comes together.
- **Export + Reporting Hooks**: Docker Compose profiles and shared configuration mirror the earlier project’s deployment goals, so future reporting endpoints can plug in easily.
- **Scalable Foundation**: Container-ready wiring and Actuator health checks maintain the operational quality bars set during the modular monolith refactor.

## Key Learning Moments

```java
// backend/src/main/java/com/example/tenantmanagement/TenantManagementApplication.java
@SpringBootApplication
public class TenantManagementApplication {
    public static void main(String[] args) {
        SpringApplication.run(TenantManagementApplication.class, args);
    }
}
```

```jsx
// frontend/src/components/Tenants.js
const fetchTenants = useCallback(async () => {
  setLoading(true);
  try {
    const res = await axios.get(`/api/tenants?page=${page}&per_page=${perPage}`);
    const tenantsArr = Array.isArray(res.data) ? res.data : (res.data.tenants || []);
    setTenants(tenantsArr);
    setTotalPages(res.data.pages || 1);
  } catch (e) {
    toast.error('Failed to fetch tenants');
  }
  setLoading(false);
}, [page]);
```

## Additional Spring Boot Insights

- **Environment Profiles via Properties**: Separate `application-dev` and `application-prod` files let me switch between H2 and PostgreSQL without touching code—Compose simply passes `SPRING_PROFILES_ACTIVE`.
- **Flyway-Led Schema Migration**: Recreating the previous schema in `V1__init.sql` (with sample data in `V2__seed.sql`) validated the new stack end-to-end, even before controllers exist.
- **React Parity Work**: Keeping the CRA-based frontend in sync ensures I can reuse the same UI screens once the Spring Boot endpoints are ready.
- **Actuator Readiness**: Health and metrics endpoints are already exposed, so adding Prometheus/Grafana later won’t require dependency changes.

## Early Benefits I Already See

- Strong typing and annotation-driven validation catch mistakes before runtime.
- Spring Data JPA reduces boilerplate, keeping the focus on domain rules.
- React’s component model makes it easier to iterate on UX without disturbing backend concerns.
- The migration narrative itself is a great story for interviews and future architecture posts.

## Key Learnings

- **Enterprise Patterns**: Spring Boot's convention-over-configuration approach provides a solid foundation for production-ready applications
- **Profile Management**: Environment-specific configurations enable seamless development and production deployments
- **Migration Strategy**: Flyway migrations ensure schema consistency across different database environments
- **Containerization**: Docker Compose orchestration simplifies development and deployment workflows
- **Technology Evolution**: Moving from Python/Flask to Java/Spring Boot demonstrates how similar concepts translate across ecosystems

## Evolution Progression

This transition represents a significant step in the evolutionary journey:
- **From Evolution 2**: Built upon the modular architecture and service layer patterns
- **To Evolution 3**: Introduced enterprise-ready patterns and Java ecosystem depth
- **Next Steps**: Focus on REST API implementation, testing, and production deployment strategies

{% include evolution/evolution-posts.html %}

{% include evolution/post-navigation.html %}

## Conclusion

This transition isn't just a tech swap—it's a deliberate chance to evaluate the Tenant Management domain through a stack I want to master long-term. Over the next posts I'll break down architecture decisions, deployment setup, and lessons learned as this Java/Spring Boot version evolves.
