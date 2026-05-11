# Test Assured API Tests

A small Spring Boot Tasks API together with a REST Assured regression test
suite. Built as a software testing engineering class project.

## Stack

- Java 21
- Maven (multi-module)
- Spring Boot — Tasks API under test
- REST Assured + JUnit 5 + Mockito — test suite

## Layout

```
.
├── api/                    Spring Boot Tasks service
│   └── src/main/java/com/ardakilinc/tasksapi
│       ├── TasksApiApplication.java
│       ├── error/          Global exception handler and error payload
│       └── task/           Task record, repository, service, controller
└── tests/                  Test suite
    └── src/test/java/com/ardakilinc/tasksapi
        ├── it/             REST Assured integration tests (*IT, Failsafe)
        └── task/           Unit tests (*Test, Surefire, Mockito)
```

## API

In-memory CRUD over `/api/tasks`.

| Method | Path             | Description           | Success      | Errors        |
| ------ | ---------------- | --------------------- | ------------ | ------------- |
| GET    | `/api/tasks`     | list all              | 200 + array  | —             |
| GET    | `/api/tasks/{id}`| fetch one             | 200 + task   | 404           |
| POST   | `/api/tasks`     | create (request body) | 201 + task + Location | 400 |
| PUT    | `/api/tasks/{id}`| replace               | 200 + task   | 404, 400      |
| DELETE | `/api/tasks/{id}`| remove                | 204          | 404           |

`Task` payload:

```json
{
  "id": 1,
  "title": "Buy milk",
  "completed": false,
  "dueDate": "2026-12-31"
}
```

Validation: `title` must not be blank and is at most 200 characters.
Validation failures return 400 with an `ApiError` body listing the offending
fields.

## Running

Prerequisites: JDK 21+, Maven 3.9+.

Run the API:

```bash
mvn -pl api spring-boot:run
```

API listens on `http://localhost:8080`.

Run all tests (unit + integration):

```bash
mvn verify
```

Run only unit tests (Surefire):

```bash
mvn test
```

## Test reports

Surefire and Failsafe produce JUnit XML reports:

- `tests/target/surefire-reports/` — unit test results
- `tests/target/failsafe-reports/` — integration test results

CI uploads both as a workflow artifact named `test-reports`.

## What every test asserts

Every integration test validates the three things required by the assignment:

- HTTP status code
- response body content (JSON path matchers)
- response time under an SLA threshold (`ResponseTimeSla.under()`, 2000 ms)
