"""Class to handle all Sage activities"""
#!/usr/bin/env python3

class Contest:

    def __init__(self):
        self.problems = []
        self.test_cases = []
        self.solutions = []
        self.leaderboard = []

    def add_problem(self, problem, test_cases, solutions):
        self.problems.append(problem)
        self.test_cases.append(test_cases)
        self.solutions.append(solutions)

    def remove_problem(self, problem, index):
        if index < len(self.problems):
            del self.problems[index]
            del self.test_cases[index]
            del self.solutions[index]

    def get_problems(self):
        return self.problems

    def get_test_cases(self):
        return self.test_cases

    def get_test_solutions(self):
        return self.solutions

    def update_leaderboard(self, leaderboard):
        self.leaderboard = leaderboard