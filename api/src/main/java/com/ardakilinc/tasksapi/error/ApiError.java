package com.ardakilinc.tasksapi.error;

import java.time.Instant;
import java.util.List;

public record ApiError(Instant timestamp, int status, String error, List<String> messages) {

    public ApiError(int status, String error, List<String> messages) {
        this(Instant.now(), status, error, messages);
    }
}
