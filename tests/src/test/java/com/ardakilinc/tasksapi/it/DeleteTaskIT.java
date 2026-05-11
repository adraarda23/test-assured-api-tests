package com.ardakilinc.tasksapi.it;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static io.restassured.RestAssured.given;

class DeleteTaskIT extends BaseApiIT {

    @Test
    @DisplayName("DELETE /tasks/{id} returns 204 and removes the task, under SLA")
    void delete_returnsNoContent() {
        Integer id = given()
                .body(Map.of("title", "scenario-delete", "completed", false))
            .when()
                .post("/tasks")
            .then()
                .statusCode(201)
                .extract().path("id");

        given()
            .when()
                .delete("/tasks/{id}", id)
            .then()
                .statusCode(204)
                .time(ResponseTimeSla.under());

        given()
            .when()
                .get("/tasks/{id}", id)
            .then()
                .statusCode(404);
    }

    @Test
    @DisplayName("DELETE /tasks/{id} returns 404 for unknown id")
    void delete_unknownIdReturnsNotFound() {
        given()
            .when()
                .delete("/tasks/{id}", 99_999_999L)
            .then()
                .statusCode(404)
                .time(ResponseTimeSla.under());
    }
}
