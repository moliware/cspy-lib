# -*- coding: utf-8 -*-
""" Implements CSP solver

Author: Miguel Olivares <miguel@moliware.com>
"""
from btexception import BTException
from event import EventManager
from Queue import LifoQueue

class Solver(object):
    """ Solve CSP problems getting all solutions """
    PHASES = ['INIT', 'SOLVING', 'FINISHED']
    def __init__(self):
        """ Init method """
        self.constraints = []
        self.variables = {}
        self.public_solutions = []
        self.qstate = LifoQueue()
        self.phase = 'INIT'
        self.e_mgr = EventManager()
        self.e_mgr.register_event('solver_on_init')
        self.e_mgr.register_event('solver_on_end')
        self.e_mgr.register_event('solver_on_solution')
        self.e_mgr.register_event('solver_on_backtrack')
        self.e_mgr.register_event('solver_before_set_value')
        self.e_mgr.register_event('solver_after_set_value')
        self.e_mgr.raise_event('solver_on_init')

    def _push_state(self, variable, value):
        """ Store in qstate the value of the variable it going to be set next
        and the state of the all domains
        """
        domain_dump = {}
        for var in self.variables.itervalues():
            # store a copy of the domain
            domain_dump[var.id] = var.domain[:]
        self.qstate.put((variable.id, value, domain_dump))

    def _pop_state(self):
        """ Restore previous state """
        return self.qstate.get(False)
    
    def _back_to_previous_state(self):
        """ Go back to a previous valid state removing invalid values.
        If qstate become empty (there is no valid state) return false 
        else true.
        """
        while not self.qstate.empty():
            state = self._pop_state()
            id_var = state[0]
            value = state[1]
            domain_dump = state[2]
            # Restore domains
            for id, domain in domain_dump.iteritems():
                self.variables[id]._restore(domain)
            # Delete invalid value
            try:
                self.variables[id_var].remove_from_domain([value])
                return True
            except:
                pass
        return False

    def reg_variable(self, variable):
        """ Register a variable to the problem. """
        self.variables[variable.id] = variable

    def _public_solution(self):
        """ Store in public_solutions a id_variable -> value hash """
        solution = {}
        for id_var, variable in self.variables.iteritems():
            solution[id_var] = variable.value
        self.public_solutions.append(solution)
        return solution

    def next_variable(self):
        """ Choose what variable is the best to be instancied. """
        for variable in self.variables.values():
            if not variable.instancied:
                return variable

    def value(self, variable):
        """ Choose the better value to the variable. """
        return variable.min()

    def solve(self):
        """ Get all solutions to the problem. """
        while self.iter_solve():
            pass
        return self.public_solutions

    def iter_solve(self):
        """ Get all the solutions one by one using a backtracking strategy."""
        if self.phase == 'INIT':
            self.phase = 'SOLVING'
        elif not self._back_to_previous_state():
            # No more solutions
            self.e_mgr.raise_event('solver_on_end')
            self.phase = 'FINISHED'
            return None
        while not self.all_instancied():
            try:
                # Heuristic
                var = self.next_variable()
                value = self.value(var)
                self.e_mgr.raise_event('solver_before_set_value')
                self._push_state(var, value)
                var.set(value)
                self.e_mgr.raise_event('solver_after_set_value')
            except BTException, bte:
                if not self._back_to_previous_state():
                    # No more solutions
                    self.phase = 'FINISHED'
                    self.e_mgr.raise_event('solver_on_end')
                    return None
                else:
                    self.e_mgr.raise_event('solver_on_backtrack')
        # Solution
        solution = self._public_solution()
        self.e_mgr.raise_event('solver_on_solution')
        return solution


    def all_instancied(self):
        """ are all variables instancied?"""
        for variable in self.variables.values():
            if not variable.instancied:
                return False
        return True


class SolverVariable():
    """ Varible class for cspy Solver. Each Variable has a domain. When a variable
    is set an unique event is raised.
    """

    def __init__(self, id, domain):
        """ Init method """
        self.id = id
        self.instancied = False
        self.event_name = "%s_on_set_value" % id
        self.e_mgr = EventManager()
        self.e_mgr.register_event(self.event_name)
        if len(domain) == 0:
            raise BTException()
        self.domain = domain
        
        if len(domain) == 1:
            self.set(domain[0])
        else:
            self.value = None

    def _restore(self, domain):
        """ Restore domain to a previous domain """
        self.domain = domain
        if len(domain) > 1:
            self.instancied = False
            self.value = None

    def set(self, val):
        """ Set the value to val and raise a event """
        self.domain = [val]
        self.value = val
        self.instancied = True
        self.e_mgr.raise_event(self.event_name, id=self.id, value=val)

    def remove_from_domain(self, values):
        """ Remove values from domain. If domain had more than one value
        and after remove only have one the variable become set.
        """
        # len before removing
        domain_len = len(self.domain)
        for value in values:
            if self.in_domain(value):
                self.domain.remove(value)
        # No values is an invalid states
        if len(self.domain) == 0:
            raise BTException()
        # Now the variable is set
        elif len(self.domain) == 1 and domain_len > 1:
            self.set(self.domain[0])

    def subscribe(self, function):
        """ Subscribe to variable event """
        self.e_mgr.subscribe(self.event_name, function)

    def in_domain(self, value):
        """ Is the value in the domain?  """
        return value in self.domain

    def min(self):
        """ Min posible value of the variable"""
        return min(self.domain)

    def max(self):
        """ Max posible value of the variable"""
        return max(self.domain)

    def __str__(self):
        """ String representation of the variable """
        return str(self.domain)
