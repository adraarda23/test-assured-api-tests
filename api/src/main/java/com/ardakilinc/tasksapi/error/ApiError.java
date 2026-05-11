package com.ardakilinc.tasksapi.error;

import java.time.Instant;
import java.util.List;

public class ApiError {

    private final Instant timestamp = Instant.now();
    private final int status;
    private final String error;
    private final List<String> messages;

    public ApiError(int status, String error, List<String> messages) {
        this.status = status;
        this.error = error;
        this.messages = messages;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public int getStatus() {
        return status;
    }

    public String getError() {
        return error;
    }

    public List<String> getMessages() {
        return messages;
    }
}
