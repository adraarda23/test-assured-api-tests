package com.ardakilinc.tasksapi.it;

import com.ardakilinc.tasksapi.it.support.ResponseTimeSla;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.notNullValue;

class GetTaskByIdIT extends BaseApiIT {

    @Test
    @DisplayName("GET /tasks/{id} returns 200 with the matching task under SLA")
    void getById_returnsCreatedTask() {
        String title = "scenario-get-by-id-" + System.nanoTime();

        Integer id = given()
                .body(Map.of(
                        "title", title,
                        "completed", false,
                        "dueDate", "2026-12-31"))
            .when()
                .post("/tasks")
            .then()
                .statusCode(201)
                .extract().path("id");

        given()
            .when()
                .get("/tasks/{id}", id)
            .then()
                .statusCode(200)
                .body("id", equalTo(id))
                .body("title", equalTo(title))
                .body("completed", equalTo(false))
                .body("dueDate", notNullValue())
                .time(ResponseTimeSla.under());
    }

    @Test
    @DisplayName("GET /tasks/{id} returns 404 for an unknown id")
    void getById_returnsNotFound() {
        given()
            .when()
                .get("/tasks/{id}", 99_999_999L)
            .then()
                .statusCode(404)
                .time(ResponseTimeSla.under());
    }
}
