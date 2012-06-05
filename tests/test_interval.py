from unittest import TestCase

from astrolabe import Interval


class IntervalTest(TestCase):
    def test_started(self):
        interval = Interval()
        self.assertFalse(interval.started)
        interval.start()
        self.assertTrue(interval.started)

    def test_stopped(self):
        interval = Interval()
        interval.start()
        self.assertFalse(interval.stopped)
        interval.stop()
        self.assertTrue(interval.stopped)

    def test_running(self):
        interval = Interval()
        self.assertFalse(interval.running)
        interval.start()
        self.assertTrue(interval.running)
        interval.stop()
        self.assertFalse(interval.running)

    def test_duration(self):
        interval = Interval()
        interval.start()
        first = interval.duration
        second = interval.duration
        self.assertTrue(second > first)

    def test_now(self):
        interval = Interval.now()
        self.assertTrue(interval.started)
        self.assertFalse(interval.stopped)

    def test_split(self):
        interval = Interval()
        interval.start()
        splitted_interval = interval.split()
        self.assertEquals(interval.stop_instant, splitted_interval.start_instant)
