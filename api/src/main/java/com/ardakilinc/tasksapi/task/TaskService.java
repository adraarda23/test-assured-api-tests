package com.ardakilinc.tasksapi.task;

import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class TaskService {

    private final TaskRepository repository;

    public TaskService(TaskRepository repository) {
        this.repository = repository;
    }

    public List<Task> listAll() {
        return repository.findAll();
    }

    public Optional<Task> findById(Long id) {
        return repository.findById(id);
    }

    public Task create(Task task) {
        task.setId(null);
        return repository.save(task);
    }

    public Optional<Task> update(Long id, Task updated) {
        return repository.findById(id).map(existing -> {
            existing.setTitle(updated.getTitle());
            existing.setCompleted(updated.isCompleted());
            existing.setDueDate(updated.getDueDate());
            return repository.save(existing);
        });
    }

    public boolean delete(Long id) {
        return repository.deleteById(id);
    }
}
