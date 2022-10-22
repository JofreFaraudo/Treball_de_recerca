import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

# Travel times per branch
TRAVEL_TIMES = {"PE":0,"MG":2,"IC":2,"EU":2,"GO":2,"SP":2,"LH":1,"AL":3,"CO":2,"BO":3,"ML":2,"CG":1.5,"CL":1.5,"VH":3,"CR":2,"QC":2,"PA":2,"SA":4,"PL":2,"MV":4,"MC":2,"ME":2,"AB":6,"OL":3,"AE":8,"MO":4,"CB":5,"SV":5,"VI":7,"MA":3,"MB":1,"SE":6,"BE":6,"CP":2,"MQ":2,"PI":6,"VA":6,"CA":3,"PO":6,"VN":5,"IG":2}
STOP_TIMES = {"MG":50,"IC":55,"EU":55,"GO":50,"SP":55,"AL":65,"CO":65,"ML":70,"CG":65,"CL":65,"VH":70,"CR":65,"QC":70,"PA":60,"PL":70,"MV":65,"ME":45,"AB":70}
STATION_LIST_SORTED = ["PE","MG","IC","EU","GO","SP","LH","AL","CO","BO","ML","CG","CL","VH","CR","QC","PA","SA","PL","MV","MC","ME","AB","OL","AE","MO","CB","SV","VI","MA","MB", "SE","BE","CP","MQ","PI","VA","CA","PO","VN","IG"]
IG_BRANCH_THRESHOLD = STATION_LIST_SORTED.index("MB") # 30
MB_BRANCH_THRESHOLD = STATION_LIST_SORTED.index("ME")

class Train_TT:
	STOP_TIME = 25
	def __init__(self, st = 0, _name = "Unnamed"):
		self.sts = []
		self.tms = []
		self.total_time = st
		self.name = _name
	def merge(self, _other):
		self.sts += _other.sts
		self.tms += _other.tms
	def add(self, _st, _it, _sk = None, _ob = False):
		self.sts.append(_st)
		if _ob:
			self.tms.append(None)
			return
		self.total_time += _it*60
		if _sk == None or _sk < 0:
			self.tms.append(self.total_time - self.STOP_TIME)
			self.sts.append(_st)
		if _sk != None:
			self.total_time -= _sk
		self.tms.append(self.total_time)
	def toTuple(self):
		return (self.sts, self.tms)
	def __str__(self):
		return str(self.sts) + "//" + str(self.tms)

# IT Class
class Itinerary:
	DIRECTION_ASCENDING = True
	DIRECTION_DESCENDING = False
	
	def __init__(self, _start, _end, _dir = DIRECTION_ASCENDING, _skip = []):
		if _start in STATION_LIST_SORTED and _end in STATION_LIST_SORTED:
			self.direction = _dir
			self.begin = STATION_LIST_SORTED.index(_start)
			self.end = STATION_LIST_SORTED.index(_end)
			self.skip = _skip
			self.ig_branch = max(self.begin, self.end) > IG_BRANCH_THRESHOLD
	def __str__(self):
		return "It Instance. D: {}, B: {}, E: {}, S: {}".format(self.direction, self.begin, self.end, self.skip)

	def copy(self, _other, _keep_dir = True):
		self.__init__(_other.direction == _keep_dir, _other.begin if _keep_dir else _other.end, _other.end if _keep_dir else _other.begin)
	def timetable(self, _ts = 0, _name = "Unnamed", _extras = {}):
		_res = Train_TT(_ts, _name)
		if self.direction == self.DIRECTION_ASCENDING:
			i = self.begin
			while i <= self.end:
				s = STATION_LIST_SORTED[i]
				sk = None
				if s in _extras:
					sk = -_extras[s]
				elif s in self.skip:
					sk = STOP_TIMES[s]
				elif i in [self.begin, self.end]:
					sk = 0
				_res.add(s, TRAVEL_TIMES[s], sk, self.ig_branch and MB_BRANCH_THRESHOLD < i <= IG_BRANCH_THRESHOLD)
				i += 1
		else:
			i = self.begin
			while i >= self.end:
				s = STATION_LIST_SORTED[i]
				sk = None
				if s in _extras:
					sk = -_extras[s]
				elif s in self.skip:
					sk = STOP_TIMES[s]
				elif i in [self.begin, self.end]:
					sk = 0
				_res.add(s, 0 if i == self.begin else TRAVEL_TIMES[STATION_LIST_SORTED[i+1]], sk, self.ig_branch and MB_BRANCH_THRESHOLD < i <= IG_BRANCH_THRESHOLD)
				i -= 1
		return _res

def createCSV(data, secs = True):
	r = "Station"
	for t in data:
		r += ","+t.name
	for s in STATION_LIST_SORTED:
		for j in ["A", "D"]:
			r += "\n{} {}".format(s, j)
			for t in data:
				r += ","
				if (j == "A" and t.sts[0] == s) or (j == "D" and t.sts[-1] == s):
					continue
				n = t.sts.count(s)
				if n > 0:
					i = t.sts.index(s)
					if n == 2 and j == "D":
						i += 1
					if secs:
						r += str(t.tms[i]) if t.tms[i] != None else ""
					else:
						r += "{:02d}:{:02d}:{:02d}".format(int(t.tms[i]//3600), int(t.tms[i]%3600//60), int(t.tms[i]%60)) if t.tms[i] != None else ""
	return r
