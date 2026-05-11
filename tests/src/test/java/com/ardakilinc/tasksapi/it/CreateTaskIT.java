package com.ardakilinc.tasksapi.it;

import com.ardakilinc.tasksapi.it.support.ResponseTimeSla;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.greaterThan;
import static org.hamcrest.Matchers.hasItem;
import static org.hamcrest.Matchers.matchesPattern;
import static org.hamcrest.Matchers.notNullValue;

class CreateTaskIT extends BaseApiIT {

    @Test
    @DisplayName("POST /tasks creates a task and returns 201 with Location header under SLA")
    void create_returnsCreated() {
        String title = "scenario-create-" + System.nanoTime();

        given()
            .body(Map.of(
                    "title", title,
                    "completed", false,
                    "dueDate", "2026-12-31"))
            .when()
                .post("/tasks")
            .then()
                .statusCode(201)
                .header("Location", matchesPattern(".*/api/tasks/\\d+"))
                .body("id", notNullValue())
                .body("id", greaterThan(0))
                .body("title", equalTo(title))
                .body("completed", equalTo(false))
                .body("dueDate", equalTo("2026-12-31"))
                .time(ResponseTimeSla.under());
    }

    @Test
    @DisplayName("POST /tasks with blank title returns 400 with field-level message")
    void create_blankTitleReturnsBadRequest() {
        given()
            .body(Map.of("title", "", "completed", false))
            .when()
                .post("/tasks")
            .then()
                .statusCode(400)
                .body("status", equalTo(400))
                .body("error", equalTo("Bad Request"))
                .body("messages", hasItem(containsString("title")))
                .time(ResponseTimeSla.under());
    }

    @Test
    @DisplayName("POST /tasks with malformed JSON returns 400")
    void create_malformedBodyReturnsBadRequest() {
        given()
            .body("{not-json")
            .when()
                .post("/tasks")
            .then()
                .statusCode(400)
                .time(ResponseTimeSla.under());
    }
}
