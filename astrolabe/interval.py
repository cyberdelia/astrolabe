from __future__ import division

try:
    try:
        from com.lapanthere.astrolabe import Instant
        instant, CONVERSION_FACTOR = Instant.instant, Instant.CONVERSION_FACTOR
    except ImportError:
        from astrolabe._instant import instant, CONVERSION_FACTOR
except ImportError:
    from astrolabe.instant import instant, CONVERSION_FACTOR  # noqa

from astrolabe.exceptions import IntervalException


class Interval(object):
    """This is the lowest level timing mechanism available.

    It allows for easy measuring based upon a block: ::

        interval = Interval()
        with interval:
            ...

    Or measuring something specifically: ::

        interval = Interval()
        interval.start()
        duration = interval.stop()

    Allocating and starting an interval can be done in one method call with: ::

        interval = Interval.now()

    """
    def __init__(self):
        self._start_instant = None
        self._stop_instant = None
        self._duration = None

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.stop()

    @classmethod
    def now(cls):
        """Create an interval that has already started"""
        interval = Interval()
        interval.start()
        return interval

    def split(self):
        """Immediately stop the current interval and start a new interval that
        has a start_instant equivalent to the stop_interval of self"""
        self.stop()
        interval = Interval()
        interval._start_instant = self.stop_instant
        return interval 

    def start(self):
        """Mark the start of the interval.

        Calling start on an already started interval has no effect.
        An interval can only be started once.

        :returns: ``True`` if the interval is truely started True otherwise ``False``.
        """
        if self._start_instant is None:
            self._start_instant = instant()
            return True
        return False

    def stop(self):
        """Mark the stop of the interval.

        Calling stop on an already stopped interval has no effect.
        An interval can only be stopped once.

        :returns: the duration if the interval is truely stopped otherwise ``False``.
        """
        if self._start_instant is None:
            raise IntervalException("Attempt to stop an interval that has not started.")
        if self._stop_instant is None:
            self._stop_instant = instant()
            self._duration = (self._stop_instant - self._start_instant) / CONVERSION_FACTOR
            return self._duration
        return False

    @property
    def duration_so_far(self):
        """Return how the duration so far.

        :returns: the duration from the time the Interval was started if the
            interval is running, otherwise ``False``.
        """
        if self._start_instant is None:
            return False
        if self._stop_instant is None:
            return (instant() - self._start_instant) / CONVERSION_FACTOR
        return False

    @property
    def started(self):
        """Returns whether or not the interval has been started."""
        return self._start_instant is not None

    @property
    def stopped(self):
        """Returns whether or not the interval has been stopped."""
        return self._stop_instant is not None

    @property
    def running(self):
        """Returns whether or not the interval is running or not.

        This means that it has started, but not stopped.
        """
        return (self._start_instant is not None) and (self._stop_instant is None)

    @property
    def start_instant(self):
        """The integer representing the start instant of the Interval.

        This value is not useful on its own.
        It is a platform dependent value.
        """
        return self._start_instant

    @property
    def stop_instant(self):
        """The integer representing the stop instant of the Interval.

        This value is not useful on its own.
        It is a platform dependent value.
        """
        return self._stop_instant

    @property
    def duration(self):
        """Returns the Float value of the interval, the value is in seconds.

        If the interval has not had stop called yet,
        it will report the number of seconds in the interval up to the current point in time.
        """
        if self._stop_instant is None:
            return (instant() - self._start_instant) / CONVERSION_FACTOR
        if self._duration is None:
            self._duration = (self._stop_instant - self._start_instant) / CONVERSION_FACTOR
        return self._duration
