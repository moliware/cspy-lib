# -*- coding: utf-8 -*-
""" Simple event manager for cspy

Author: Miguel Olivares <miguel@moliware.com>
"""
class Singleton(object):
    """ Class that implements Singleton desing pattern. """
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

class EventManager(Singleton):
    """ Event manager that allows: 
            1. register events.
            2. subscribe to any event ( 1 event - many subscriptors)
            3. raise events
    """
    events = {}
    def __init__(self):
        """ Init method """
        super(EventManager, self).__init__()

    def register_event(self, id_event):
        """ Regist a event if not exists """
        if not id_event in self.events:
            self.events[id_event] = []


    def subscribe(self, id_event, function):
        """ Subscribe to id_event. """
        if callable(function) and id_event in self.events:
            self.events[id_event].append(function)

    def raise_event(self, id_event, **kwargs):
        """ raise 'id_event' event. """
        for function in self.events[id_event]:
            function(**kwargs)
