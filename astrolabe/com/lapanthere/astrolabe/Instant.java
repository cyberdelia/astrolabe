package com.lapanthere.astrolabe;

import org.python.core.PyObject;


public class Instant {
    public static final double CONVERSION_FACTOR = 1000000000d;

    public static long instant() {
        return System.nanoTime();
    }
}