package com.ardakilinc.tasksapi.it;

import com.ardakilinc.tasksapi.it.support.ResponseTimeSla;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;

class UpdateTaskIT extends BaseApiIT {

    @Test
    @DisplayName("PUT /tasks/{id} updates an existing task and returns 200 under SLA")
    void update_returnsUpdatedTask() {
        Integer id = given()
                .body("{\"title\":\"original-title\",\"completed\":false}")
            .when()
                .post("/tasks")
            .then()
                .statusCode(201)
                .extract().path("id");

        given()
            .body("{\"title\":\"updated-title\",\"completed\":true,\"dueDate\":\"2027-01-01\"}")
            .when()
                .put("/tasks/{id}", id)
            .then()
                .statusCode(200)
                .body("id", equalTo(id))
                .body("title", equalTo("updated-title"))
                .body("completed", equalTo(true))
                .body("dueDate", equalTo("2027-01-01"))
                .time(ResponseTimeSla.under());
    }

    @Test
    @DisplayName("PUT /tasks/{id} returns 404 for unknown id")
    void update_unknownIdReturnsNotFound() {
        given()
            .body("{\"title\":\"whatever\",\"completed\":false}")
            .when()
                .put("/tasks/{id}", 99_999_999L)
            .then()
                .statusCode(404)
                .time(ResponseTimeSla.under());
    }

    @Test
    @DisplayName("PUT /tasks/{id} with blank title returns 400")
    void update_blankTitleReturnsBadRequest() {
        Integer id = given()
                .body("{\"title\":\"will-be-rejected-on-update\",\"completed\":false}")
            .when()
                .post("/tasks")
            .then()
                .statusCode(201)
                .extract().path("id");

        given()
            .body("{\"title\":\"\",\"completed\":false}")
            .when()
                .put("/tasks/{id}", id)
            .then()
                .statusCode(400)
                .time(ResponseTimeSla.under());
    }
}
