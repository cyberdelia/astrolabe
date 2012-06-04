from time import sleep
from unittest import TestCase

try:
    try:
        from com.lapanthere.astrolabe import Instant
        instant, CONVERSION_FACTOR = Instant.instant, Instant.CONVERSION_FACTOR
    except ImportError:
        from astrolabe._instant import instant, CONVERSION_FACTOR
except ImportError as e:
    from astrolabe.instant import instant, CONVERSION_FACTOR  # noqa


class TestInstant(TestCase):
    def test_duration(self):
        first = instant()
        sleep(0.1)
        second = instant()
        self.assertTrue(second > first)
