package com.ardakilinc.tasksapi.task;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
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
        assertThat(captor.getValue().getId())
                .as("service must not let the caller pick the id")
                .isNull();
        assertThat(result).isSameAs(persisted);
        assertThat(result.getId()).isEqualTo(1L);
    }
}
