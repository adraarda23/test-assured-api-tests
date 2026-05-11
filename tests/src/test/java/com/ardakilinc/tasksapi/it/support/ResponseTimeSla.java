package com.ardakilinc.tasksapi.it.support;

import org.hamcrest.Matcher;

import static org.hamcrest.Matchers.lessThan;

/**
 * Centralizes the response-time SLA every test asserts against, so the
 * threshold can be tuned in one place. Used with REST Assured's
 * {@code .time(...)} validation, e.g. {@code .time(ResponseTimeSla.under())}.
 */
public final class ResponseTimeSla {

    public static final long DEFAULT_SLA_MILLIS = 2000L;

    private ResponseTimeSla() {
    }

    public static Matcher<Long> under() {
        return lessThan(DEFAULT_SLA_MILLIS);
    }

    public static Matcher<Long> under(long millis) {
        return lessThan(millis);
    }
}
