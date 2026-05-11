package com.ardakilinc.tasksapi.task;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TaskServiceTest {

    @Mock
    TaskRepository repository;

    @InjectMocks
    TaskService service;

    @Test
    @DisplayName("create() clears any client-supplied id and delegates to the repository")
    void create_clearsIdBeforeSaving() {
        Task incoming = new Task(999L, "Buy milk", false, LocalDate.of(2026, 12, 31));
        Task persisted = new Task(1L, "Buy milk", false, LocalDate.of(2026, 12, 31));
        when(repository.save(any(Task.class))).thenReturn(persisted);

        Task result = service.create(incoming);

        ArgumentCaptor<Task> captor = ArgumentCaptor.forClass(Task.class);
        verify(repository).save(captor.capture());
        assertThat(captor.getValue().id())
                .as("service must not let the caller pick the id")
                .isNull();
        assertThat(result).isSameAs(persisted);
        assertThat(result.id()).isEqualTo(1L);
    }

    @Test
    @DisplayName("listAll() returns whatever the repository returns")
    void listAll_delegatesToRepository() {
        List<Task> stored = List.of(
                new Task(1L, "a", false, null),
                new Task(2L, "b", true, null));
        when(repository.findAll()).thenReturn(stored);

        assertThat(service.listAll()).isEqualTo(stored);
    }

    @Test
    @DisplayName("findById() returns the task when present")
    void findById_returnsTaskWhenPresent() {
        Task task = new Task(7L, "found", false, null);
        when(repository.findById(7L)).thenReturn(Optional.of(task));

        assertThat(service.findById(7L)).contains(task);
    }

    @Test
    @DisplayName("findById() returns empty when missing")
    void findById_returnsEmptyWhenMissing() {
        when(repository.findById(99L)).thenReturn(Optional.empty());

        assertThat(service.findById(99L)).isEmpty();
    }

    @Test
    @DisplayName("update() saves a replacement task with the existing id and the new fields")
    void update_replacesAndSaves() {
        Task existing = new Task(5L, "old", false, LocalDate.of(2026, 1, 1));
        Task incoming = new Task(null, "new", true, LocalDate.of(2027, 6, 6));
        Task expected = new Task(5L, "new", true, LocalDate.of(2027, 6, 6));
        when(repository.findById(5L)).thenReturn(Optional.of(existing));
        when(repository.save(expected)).thenReturn(expected);

        Optional<Task> result = service.update(5L, incoming);

        assertThat(result).contains(expected);
    }

    @Test
    @DisplayName("update() returns empty and does not save when target is missing")
    void update_returnsEmptyWhenMissing() {
        when(repository.findById(404L)).thenReturn(Optional.empty());

        Optional<Task> result = service.update(404L, new Task(null, "x", false, null));

        assertThat(result).isEmpty();
        verify(repository, never()).save(any());
    }

    @Test
    @DisplayName("delete() returns true when repository removed something")
    void delete_returnsTrueWhenRemoved() {
        when(repository.deleteById(3L)).thenReturn(true);

        assertThat(service.delete(3L)).isTrue();
    }

    @Test
    @DisplayName("delete() returns false when nothing was removed")
    void delete_returnsFalseWhenMissing() {
        when(repository.deleteById(3L)).thenReturn(false);

        assertThat(service.delete(3L)).isFalse();
    }
}
