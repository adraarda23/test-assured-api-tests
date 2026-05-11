package com.ardakilinc.tasksapi.task;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.time.LocalDate;

public record Task(
        Long id,
        @NotBlank(message = "title must not be blank")
        @Size(max = 200, message = "title must be at most 200 characters")
        String title,
        boolean completed,
        LocalDate dueDate
) {
    public Task withId(Long id) {
        return new Task(id, title, completed, dueDate);
    }
}
