package com.ardakilinc.tasksapi.task;

import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Repository
public class TaskRepository {

    private final ConcurrentHashMap<Long, Task> store = new ConcurrentHashMap<>();
    private final AtomicLong sequence = new AtomicLong(0);

    public List<Task> findAll() {
        return List.copyOf(store.values());
    }

    public Optional<Task> findById(Long id) {
        return Optional.ofNullable(store.get(id));
    }

    public Task save(Task task) {
        Task toStore = task.id() == null ? task.withId(sequence.incrementAndGet()) : task;
        store.put(toStore.id(), toStore);
        return toStore;
    }

    public boolean deleteById(Long id) {
        return store.remove(id) != null;
    }

    public boolean existsById(Long id) {
        return store.containsKey(id);
    }
}
