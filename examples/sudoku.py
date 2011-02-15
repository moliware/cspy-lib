# -*- coding: utf-8 -*-
""" Sudoku problem

Author: Miguel Olivares <miguel@moliware.com>
"""
import cspy

from cspy.constraint import NotEqualConstraint

class SudokuSolver(cspy.Solver):

    def __init__(self, sudoku):
        super(SudokuSolver,self).__init__()

        # Create variables of the sudoku
        self.sudoku_matrix = {}
        for i in range(9):
            self.sudoku_matrix[i] = {}
            for j in range(9):
                self.sudoku_matrix[i][j] = cspy.SolverVariable(i*9 + j ,range(1, 10))
                self.reg_variable(self.sudoku_matrix[i][j])

        # constraints
        for i in range(9):
            # Each value of a row must be different
            NotEqualConstraint(self.sudoku_matrix[i].values())
            # Each value of a column must be different
            NotEqualConstraint([self.sudoku_matrix[j][i] for j in range(9)])
            # Cuadrant constraint
            NotEqualConstraint(self.calculate_cuadrant(i))
            
        # init
        for i in range(len(sudoku)):
            for j in range(len(sudoku[i])):
                if not sudoku[i][j] is -1:
                    self.sudoku_matrix[i][j].set(sudoku[i][j])

        self.e_mgr.subscribe('solver_after_set_value', self.print_sudoku)
        self.e_mgr.subscribe('solver_on_solution', self.print_solution)
        self.e_mgr.subscribe('solver_on_end', self.print_end)

    def calculate_cuadrant(self, c):
        squares = []
        # First square of the cuadrant
        first_i = c / 3 * 3
        first_j = c % 3 * 3
        for i in range(first_i, first_i + 3):
            for j in range(first_j, first_j + 3):
                squares.append(self.sudoku_matrix[i][j])
        return squares

    def print_sudoku(self, **kwarg):
        print '=' * 50
        i = 0
        result = ''
        for k, row in self.sudoku_matrix.iteritems():
            if i % 9 == 0:
                print result
                result = ''
            result += '|'
            for v in row.itervalues():
                if (v.instancied):
                    result += str(v)
                else:
                    result += '___'
                result += ' '
                i = i+1
        print result

    def print_solution(self, **kwarg):
        print '%sSolution:%s' % ('=' * 20, '=' * 20)
        i = 0
        result = ''
        solution = self.public_solutions[-1]
        for k,v in solution.iteritems():
            if i % 9 == 0:
                print result
                result = ''
            result += str([v])
            result += ' '
            i = i+1
        print result

    def print_end(self, **kwarg):
        print '%sFinish:%s' % ('=' * 20, '=' * 20)
        print 'Found %d solutions' % len(self.public_solutions)
        

def main():
    # Example sudoku
    sudoku = [[-1, -1, 6, -1, -1, 3, 5, -1, 4],
              [4, -1, 7, 6, -1, -1, -1, -1, 8],
              [-1, -1, -1, -1, 8, -1, 2, 6, -1],
              [-1, -1, 8, -1, 6, -1, -1, -1, 2],
              [-1, -1, -1, 2, 4, -1, -1, -1, 9],
              [-1, 2, -1, 5, 7, -1, 3, -1, -1],
              [-1, -1, -1, -1, -1, 4, -1, 3, 5],
              [8, 5, -1, -1, -1, -1, -1, 2, -1],
              [6, -1, -1, -1, 3, 5, -1, -1, 7]]

    s = SudokuSolver(sudoku)
    s.solve()

if __name__ == '__main__':
    main()
