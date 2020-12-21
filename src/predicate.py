class Predicate:
    number = 0
    program_line = 0
    predicate = ""
    branch = True
    coverage_status = False
    dropped = False

    def __init__(
        self, number, program_line, predicate, branch, coverage_status
    ):
        self.number = number
        self.program_line = program_line
        self.predicate = predicate
        self.branch = branch
        self.coverage_status = coverage_status
        self.dropped = False

    def get_coverage_status(self):
        return self.coverage_status

    def is_dropped(self):
        return self.dropped

    def __eq__(self, other):
        ans = True
        ans = ans and self.number == other.number
        ans = ans and self.program_line == other.program_line
        ans = ans and self.predicate == other.predicate
        ans = ans and self.branch == other.branch
        ans = ans and self.coverage_status == other.coverage_status
        return ans

    def __str__(self):
        return (
            str(self.number)
            + "  #"
            + str(self.program_line)
            + "  ("
            + str(self.predicate)
            + ")  "
            + str(self.branch)
            + "  "
            + str(self.coverage_status)
        )
