# -*- coding: utf-8 -*-
""" Constraint interface and some tipical constraints 

Author: Miguel Olivares <miguel@moliware.com>
"""

class Constraint(object):

    def __init__(self, variables=[]):
        self.variables = {}
        self.add_variables(variables)
        pass

    def add_variables(self, variables):
        for variable in variables:
            self.variables[variable.id] = variable
            variable.subscribe(self.propagate)

    def propagate(self, **kwargs):
        pass

class NotEqualConstraint(Constraint):

    def __init__(self, variables=[]):
        super(NotEqualConstraint, self).__init__(variables)

    def propagate(self, **kwargs):
        id = kwargs['id']
        value = kwargs['value']
        for variable in self.variables.itervalues():
            if not variable.id is id:
                variable.remove_from_domain([value])
