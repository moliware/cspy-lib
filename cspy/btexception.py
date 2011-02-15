# -*- coding: utf-8 -*-
""" Exception class for cspy project. It is called to produce a backtrack

Author: Miguel Olivares <miguel@moliware.com>
"""

class BTException(BaseException):
    """ Raise this exception when backtracking is needed """

    def __init__(self, msg=''):
        """ Init method. """
        self.msg = msg

    def __str__(self):
        """ String representation """
        return 'Backtracking exception: %s' % self.msg
