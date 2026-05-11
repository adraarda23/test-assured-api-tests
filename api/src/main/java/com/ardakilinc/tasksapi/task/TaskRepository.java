package com.ardakilinc.tasksapi.task;

import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Repository
public class TaskRepository {

    private final ConcurrentHashMap<Long, Task> store = new ConcurrentHashMap<>();
    private final AtomicLong sequence = new AtomicLong(0);

    public List<Task> findAll() {
        return new ArrayList<>(store.values());
    }

    public Optional<Task> findById(Long id) {
        return Optional.ofNullable(store.get(id));
    }

    public Task save(Task task) {
        if (task.getId() == null) {
            task.setId(sequence.incrementAndGet());
        }
        store.put(task.getId(), task);
        return task;
    }

    public boolean deleteById(Long id) {
        return store.remove(id) != null;
    }

    public boolean existsById(Long id) {
        return store.containsKey(id);
    }
}
