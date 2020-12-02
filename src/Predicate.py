class Predicate:
    number = 0
    program_line = 0
    predicate = ""
    branch = True
    coverage_status = False

    def __init__(self, number, program_line, predicate, branch, coverage_status):
        self.number = number
        self.program_line = program_line
        self.predicate = predicate
        self.branch = branch
        self.coverage_status = coverage_status

    def __str__(self):
        return str(self.number) + "  #" + str(self.program_line) + "  (" + str(self.predicate) + ")  " + str(self.branch) + "  " + str(self.coverage_status)
