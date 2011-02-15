# -*- coding: utf-8 -*-
""" Unit tests for class EventManager

Author: Miguel Olivares <miguel@moliware.com>
"""
import unittest

from event import EventManager


class TestEventManager(unittest.TestCase):
    """ Class for testing event.EventManager from cspy """

    def setUp(self):
        """ Prepare the test """
        self.e_mgr = EventManager()

    def test_singleton(self):
        """ Design pattern implemented correctly? """
        self.assertEqual(self.e_mgr._Singleton__instance, EventManager()._Singleton__instance)

    def test_subscription(self):
        """ Events are created correctly a recieved? """
        def function(**kwargs):
            """ Test function """
            self.assertEqual(1, kwargs['test'])
        self.e_mgr.register_event('test_event')
        self.e_mgr.subscribe('test_event', function)
        self.e_mgr.raise_event('test_event', test=1)


if __name__ == "__main__":
    # Run tests
    unittest.main()
