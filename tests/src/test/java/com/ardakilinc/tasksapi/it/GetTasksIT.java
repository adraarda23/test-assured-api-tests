package com.ardakilinc.tasksapi.it;

import com.ardakilinc.tasksapi.it.support.ResponseTimeSla;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.hasItem;
import static org.hamcrest.Matchers.notNullValue;

class GetTasksIT extends BaseApiIT {

    @Test
    @DisplayName("GET /tasks returns 200 with a JSON array under SLA")
    void list_returnsOkAndArray() {
        given()
            .when()
                .get("/tasks")
            .then()
                .statusCode(200)
                .contentType("application/json")
                .body("$", notNullValue())
                .time(ResponseTimeSla.under());
    }

    @Test
    @DisplayName("GET /tasks reflects a previously created task")
    void list_containsCreatedTask() {
        String uniqueTitle = "scenario-list-" + System.nanoTime();

        given()
            .body("{\"title\":\"" + uniqueTitle + "\",\"completed\":false}")
            .when()
                .post("/tasks")
            .then()
                .statusCode(201);

        given()
            .when()
                .get("/tasks")
            .then()
                .statusCode(200)
                .body("title", hasItem(equalTo(uniqueTitle)))
                .time(ResponseTimeSla.under());
    }
}
