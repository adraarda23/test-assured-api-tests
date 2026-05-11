package com.ardakilinc.tasksapi.task;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.net.URI;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TaskControllerTest {

    @Mock
    TaskService service;

    @InjectMocks
    TaskController controller;

    @Test
    @DisplayName("list() returns whatever the service returns")
    void list_delegatesToService() {
        List<Task> tasks = List.of(new Task(1L, "a", false, null));
        when(service.listAll()).thenReturn(tasks);

        assertThat(controller.list()).isEqualTo(tasks);
    }

    @Test
    @DisplayName("getById() returns 200 with body when the task is present")
    void getById_returnsOk() {
        Task task = new Task(1L, "found", false, null);
        when(service.findById(1L)).thenReturn(Optional.of(task));

        ResponseEntity<Task> response = controller.getById(1L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isSameAs(task);
    }

    @Test
    @DisplayName("getById() returns 404 when the task is missing")
    void getById_returnsNotFound() {
        when(service.findById(99L)).thenReturn(Optional.empty());

        ResponseEntity<Task> response = controller.getById(99L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
        assertThat(response.getBody()).isNull();
    }

    @Test
    @DisplayName("create() returns 201 with Location header pointing at the new task")
    void create_returnsCreatedWithLocation() {
        Task incoming = new Task(null, "new", false, null);
        Task persisted = new Task(7L, "new", false, null);
        when(service.create(incoming)).thenReturn(persisted);

        ResponseEntity<Task> response = controller.create(incoming);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getHeaders().getLocation()).isEqualTo(URI.create("/api/tasks/7"));
        assertThat(response.getBody()).isSameAs(persisted);
    }

    @Test
    @DisplayName("update() returns 200 with body when the task is updated")
    void update_returnsOk() {
        Task incoming = new Task(null, "new", true, null);
        Task updated = new Task(5L, "new", true, null);
        when(service.update(5L, incoming)).thenReturn(Optional.of(updated));

        ResponseEntity<Task> response = controller.update(5L, incoming);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isSameAs(updated);
    }

    @Test
    @DisplayName("update() returns 404 when the task does not exist")
    void update_returnsNotFound() {
        Task incoming = new Task(null, "x", false, null);
        when(service.update(99L, incoming)).thenReturn(Optional.empty());

        ResponseEntity<Task> response = controller.update(99L, incoming);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }

    @Test
    @DisplayName("delete() returns 204 when the task is removed")
    void delete_returnsNoContent() {
        when(service.delete(3L)).thenReturn(true);

        ResponseEntity<Void> response = controller.delete(3L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NO_CONTENT);
    }

    @Test
    @DisplayName("delete() returns 404 when the task does not exist")
    void delete_returnsNotFound() {
        when(service.delete(99L)).thenReturn(false);

        ResponseEntity<Void> response = controller.delete(99L);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }
}
