from Predicate import Predicate


class PDG:
	# maps of (Tuple - (List[Tuple], List[Tuple])) because Predicate type couldn't be hashed
	control_flow = {}
	data_flow = {}

	def __init__(self, source_code):
		if source_code[2:5] == "gcd":
			# pdg for gcd here!
			self.control_flow = {}
			self.data_flow = {}
		if source_code[2:5] == "tri":
			P8 = (1, 8, "if i <= 0 or j <= 0 or k <= 0:", True, True)
			P13 = (2, 13, "if i == j", True, False)
			P15 = (3, 15, "if i == k", True, False)
			P17 = (4, 17, "if j == k", True, False)
			P20 = (5, 20, "if tri == 0", True, False)
			P21 = (6, 21, "if i + j < k or j + k < i or k + i < j:", True, False)
			P28 = (7, 28, "if tri > 3", True, False)
			P30 = (8, 30, "if tri == 1 and i + j > k", True, False)
			P32 = (9, 32, "if tri == 2 and i + k > j", True, False)
			P34 = (10, 34, "if tri == 3 and j + k > i", True, False)
			self.control_flow = {
				P8: ([], [P13, P15, P17, P20]),
				P13: ([], []),
				P15: ([], []),
				P17: ([], []),
				P20: ([P21], [P28]),
				P21: ([], []),
				P28: ([], [P30]),
				P30: ([], [P32]),
				P32: ([], [P34]),
				P34: ([], []),
			}
			# create data flow!
			self.data_flow = {}

	# to update a coverage status of predicate in pdg
	def update(self, predicate):
		tup = (predicate.number, predicate.program_line, predicate.predicate, predicate.branch, predicate.coverage_status)
		new_predicate = predicate
		new_predicate.coverage_status = True
		new_tup = (new_predicate.number, new_predicate.program_line, new_predicate.predicate, new_predicate.branch, new_predicate.coverage_status)
		value = self.control_flow[tup]
		del self.control_flow[tup]
		self.control_flow[new_tup] = value
		for t in self.control_flow:
			if tup in self.control_flow[t][0]:
				self.control_flow[t][0].remove(tup)
				self.control_flow[t][0].append(new_tup)
			if tup in self.control_flow[t][1]:
				self.control_flow[t][1].remove(tup)
				self.control_flow[t][1].append(new_tup)
		return
