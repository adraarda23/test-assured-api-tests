package com.ardakilinc.tasksapi.task;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;

class TaskRepositoryTest {

    private TaskRepository repository;

    @BeforeEach
    void setUp() {
        repository = new TaskRepository();
    }

    @Test
    @DisplayName("findAll() returns an empty list on a fresh repository")
    void findAll_emptyByDefault() {
        assertThat(repository.findAll()).isEmpty();
    }

    @Test
    @DisplayName("save() assigns incrementing ids when none is supplied")
    void save_assignsIncrementingIds() {
        Task first = repository.save(new Task(null, "first", false, null));
        Task second = repository.save(new Task(null, "second", false, null));

        assertThat(first.id()).isEqualTo(1L);
        assertThat(second.id()).isEqualTo(2L);
    }

    @Test
    @DisplayName("save() keeps the id when one is already set")
    void save_preservesExistingId() {
        Task task = new Task(42L, "keep-id", false, null);

        Task saved = repository.save(task);

        assertThat(saved.id()).isEqualTo(42L);
        assertThat(repository.findById(42L)).isPresent();
    }

    @Test
    @DisplayName("findById() returns the saved task")
    void findById_returnsSaved() {
        Task saved = repository.save(new Task(null, "fetch-me", true, LocalDate.of(2026, 6, 6)));

        assertThat(repository.findById(saved.id()))
                .contains(new Task(saved.id(), "fetch-me", true, LocalDate.of(2026, 6, 6)));
    }

    @Test
    @DisplayName("findById() returns empty for an unknown id")
    void findById_emptyForUnknown() {
        assertThat(repository.findById(404L)).isEmpty();
    }

    @Test
    @DisplayName("deleteById() removes the entry and reports true")
    void deleteById_removesEntry() {
        Task saved = repository.save(new Task(null, "delete-me", false, null));

        assertThat(repository.deleteById(saved.id())).isTrue();
        assertThat(repository.findById(saved.id())).isEmpty();
        assertThat(repository.existsById(saved.id())).isFalse();
    }

    @Test
    @DisplayName("deleteById() returns false when the id is unknown")
    void deleteById_falseForUnknown() {
        assertThat(repository.deleteById(404L)).isFalse();
    }

    @Test
    @DisplayName("existsById() reflects current storage state")
    void existsById_reflectsState() {
        Task saved = repository.save(new Task(null, "check-me", false, null));

        assertThat(repository.existsById(saved.id())).isTrue();
        assertThat(repository.existsById(saved.id() + 1)).isFalse();
    }
}
