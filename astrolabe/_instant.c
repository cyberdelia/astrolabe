#include <Python.h>
#include "structmember.h"

#define NANOSECONDS_PER_SECOND 1e9l

#if __APPLE__
 #include <CoreServices/CoreServices.h>
 #define INSTANT_LONG unsigned long long int
 #define INSTANT_CONVERSION_FACTOR 1e9l
#elif _WIN32
 #define INSTANT_LONG unsigned __int64
 #define INSTANT_CONVERSION_FACTOR conversion_factor()
 long double conversion_factor() {
     LARGE_INTEGER ticks_per_second;
     QueryPerformanceFrequency(&ticks_per_second);
     return (double)ticks_per_second.QuadPart;
 }
#elif __unix
 #include <time.h>
 #ifndef CLOCK_MONOTONIC
  #include <sys/time.h>
  #ifndef CLOCK_MONOTONIC
   #ifdef __linux__
    #include <linux/time.h>
   #endif
  #endif
 #endif
 #define INSTANT_LONG unsigned long long int
 #define INSTANT_CONVERSION_FACTOR 1e9l
#endif

typedef INSTANT_LONG instant_t;

static PyObject * instant_exception;

static PyObject * instant(PyObject *self, PyObject *args) {
#if __APPLE__
  Nanoseconds nano = AbsoluteToNanoseconds(UpTime());
  return PyLong_FromUnsignedLongLong(*(instant_t *) &nano);
#elif _WIN32
  LARGE_INTEGER tick;
  QueryPerformanceCounter(&tick);
  return PyLong_FromUnsignedLongLong(tick.QuadPart);
#elif __unix
  struct timespec time;
  int err;
  err = clock_gettime( CLOCK_MONOTONIC, &time);
  if (err != 0)  {
    char * message = strerror(err);
    return PyErr_Format(instant_exception, "Unable to retrieve instant : %s", message);
  }
  return PyLong_FromUnsignedLongLong((NANOSECONDS_PER_SECOND * (long)time.tv_sec) + time.tv_nsec);
#else
#error No high precision timers available for this platform
#endif
}

static PyMethodDef instant_methods[] = {
    {"instant",  instant, METH_NOARGS, "Return current instant."},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
  #define MOD_ERROR_VAL NULL
  #define MOD_SUCCESS_VAL(val) val
  #define MOD_INIT(name) PyMODINIT_FUNC PyInit__##name(void)
  #define MOD_DEF(ob, name, doc, methods) \
    static struct PyModuleDef moduledef = { \
      PyModuleDef_HEAD_INIT, name, doc, -1, methods, }; \
    ob = PyModule_Create(&moduledef);
#else
  #define MOD_ERROR_VAL
  #define MOD_SUCCESS_VAL(val)
  #define MOD_INIT(name) void init_##name(void)
  #define MOD_DEF(ob, name, doc, methods) \
    ob = Py_InitModule3(name, methods, doc);
#endif

MOD_INIT(instant) {
  PyObject *m;

  MOD_DEF(m, "_instant", "High resolution timer library", instant_methods);
  if (m == NULL) {
    return MOD_ERROR_VAL;
  }

  instant_exception = PyErr_NewException("astrolabe._instant.InstantException", NULL, NULL);
  Py_INCREF(instant_exception);
  PyModule_AddObject(m, "InstantException", instant_exception);
  
  PyModule_AddObject(m, "CONVERSION_FACTOR", PyLong_FromLong(INSTANT_CONVERSION_FACTOR));
  return MOD_SUCCESS_VAL(m);
}