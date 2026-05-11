package com.ardakilinc.tasksapi.it;

import org.hamcrest.Matcher;

import static org.hamcrest.Matchers.lessThan;

public final class ResponseTimeSla {

    public static final long DEFAULT_SLA_MILLIS = 2000L;

    private ResponseTimeSla() {
    }

    public static Matcher<Long> under() {
        return lessThan(DEFAULT_SLA_MILLIS);
    }
}
