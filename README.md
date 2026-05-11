# Test Assured API Tests

A small Spring Boot Tasks API together with a REST Assured regression test
suite. Built as a software testing engineering class project.

## Goal

Demonstrate REST Assured + JUnit 5 + Maven as a regression testing stack
against a minimal but realistic HTTP API. Each test validates:

- HTTP status code
- response body content
- response time under a threshold

## Stack

- Java 21
- Maven (multi-module)
- Spring Boot — Tasks API under test
- REST Assured + JUnit 5 — test suite

## Modules

- `api/` — the Spring Boot service exposing `/api/tasks` endpoints
- `tests/` — the REST Assured regression test suite

## Status

Project scaffolding in progress. See commit history for incremental setup.
