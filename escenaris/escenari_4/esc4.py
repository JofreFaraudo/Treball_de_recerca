import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

# Travel times per branch
TRAVEL_TIMES = {"PE":0,"MG":2,"IC":2,"EU":2,"GO":2,"SP":2,"LH":1,"AL":3,"CO":2,"BO":3,"ML":2,"CG":1.5,"CL":1.5,"VH":3,"CR":2,"QC":2,"PA":2,"SA":4,"PL":2,"MV":4,"MC":2,"ME":2,"AB":6,"OL":3,"AE":8,"MO":4,"CB":5,"SV":5,"VI":7,"MA":3,"MB":1,"SE":6,"BE":6,"CP":2,"MQ":2,"PI":6,"VA":6,"CA":3,"PO":6,"VN":5,"IG":2}
STOP_TIMES = {"MG":50,"IC":55,"EU":55,"GO":50,"SP":55,"AL":65,"CO":65,"ML":70,"CG":65,"CL":65,"VH":70,"CR":65,"QC":70,"PA":60,"PL":70,"MV":65,"ME":45,"AB":70,"BE":55,"CP":55}
STATION_LIST_SORTED = ["PE","MG","IC","EU","GO","SP","LH","AL","CO","BO","ML","CG","CL","VH","CR","QC","PA","SA","PL","MV","MC","ME","AB","OL","AE","MO","CB","SV","VI","MA","MB","SE","BE","CP","MQ","PI","VA","CA","PO","VN","IG"]
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
	def timetable(self, offset = 0, _name = "Unnamed", _extras = {}):
		_res = Train_TT(offset, _name)
		if self.direction == self.DIRECTION_ASCENDING:
			i = self.begin
			while i <= self.end:
				s = STATION_LIST_SORTED[i]
				sk = None
				if s in _extras:
					sk = -_extras[s]
				elif s in self.skip:
					sk = STOP_TIMES[s] if s in STOP_TIMES else 0
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
					sk = STOP_TIMES[s] if s in STOP_TIMES else 0
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
					elif secs == None:
						r += "{:02d}:{:02d}:{:02d}".format(int(t.tms[i]//3600), int(t.tms[i]%3600//60), int(t.tms[i]%60)) if t.tms[i] != None else ""
					else:
						r += "{:02d}:{:02d}".format(int(t.tms[i]%3600//60), int(t.tms[i]%60)) if t.tms[i] != None else ""
	return r

# Lines and stops
S_L8_A = Itinerary("PE", "ML") # L8 towards ML (local)
S_L8_D = Itinerary("ML", "PE", Itinerary.DIRECTION_DESCENDING)
S_S4_A = Itinerary("PE", "OL") # S4 towards OL (local)
S_S4_D = Itinerary("OL", "PE", Itinerary.DIRECTION_DESCENDING)
S_S8_A = Itinerary("PE", "ME") # S8 towards ME (local)
S_S8_D = Itinerary("ME", "PE", Itinerary.DIRECTION_DESCENDING)
S_R5_A = Itinerary("PE", "MB", _skip = ["MG","IC","EU","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV","ME","AB"]) # Rapid service
S_R5_D = Itinerary("MB", "PE", _skip = ["MG","IC","EU","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV","ME","AB"], _dir = Itinerary.DIRECTION_DESCENDING)
S_R6_A = Itinerary("PE", "IG", _skip = ["MG","IC","EU","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV"])
S_R6_D = Itinerary("IG", "PE", _skip = ["MG","IC","EU","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV"], _dir = Itinerary.DIRECTION_DESCENDING)
S_R5B_A = Itinerary("PE", "MB", _skip = ["MG","EU","GO","SP","AL","CO","ML","CG","CL","VH","QC","PA","MV"]) # Semirapid service
S_R5B_D = Itinerary("MB", "PE", _skip = ["MG","EU","GO","SP","AL","CO","ML","CG","CL","VH","QC","PA","MV"], _dir = Itinerary.DIRECTION_DESCENDING)
S_R6B_A = Itinerary("PE", "IG", _skip = ["MG","EU","GO","SP","AL","CO","ML","CG","CL","CR","QC","PL","MV"])
S_R6B_D = Itinerary("IG", "PE", _skip = ["MG","EU","GO","SP","AL","CO","ML","CG","CL","CR","QC","PL","MV"], _dir = Itinerary.DIRECTION_DESCENDING)
S_R5C_A = Itinerary("PE", "MB", _skip = ["MG","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV"]) # Rapid service between MC - PE, calling at IC and EU
S_R5C_D = Itinerary("MB", "PE", Itinerary.DIRECTION_DESCENDING, ["MG","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV"])
#S_R6C_A = Itinerary("PE", "IG", _skip = ["MG","IC","EU","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV","BE"]) # Rapid service, not calling at BE
#S_R6C_D = Itinerary("IG", "PE", _skip = ["MG","IC","EU","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV","BE"], _dir = Itinerary.DIRECTION_DESCENDING)
S_R5D_A = Itinerary("PE", "MB", _skip = ["MG","EU","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV","ME","AB"]) # Rapid service calling at IC
S_R5D_D = Itinerary("MB", "PE", Itinerary.DIRECTION_DESCENDING, ["MG","EU","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV","ME","AB"])
S_R6D_A = Itinerary("PE", "IG", _skip = ["MG","IC","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV","CP"]) # Rapid service, not calling at CP, calling at EU
S_R6D_D = Itinerary("IG", "PE", _skip = ["MG","IC","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV","CP"], _dir = Itinerary.DIRECTION_DESCENDING)
S_R6M_A = Itinerary("MC", "IG", _skip = ["BE"]) # Local partial service
S_R6M_D = Itinerary("IG", "MC", Itinerary.DIRECTION_DESCENDING, _skip = ["BE"])
S_R6L_A = Itinerary("PE", "IG", _skip = ["BE"])
S_R6L_D = Itinerary("IG", "PE", Itinerary.DIRECTION_DESCENDING, _skip = ["BE"])
S_POT_D = Itinerary("MA", "BO", Itinerary.DIRECTION_DESCENDING, ["ML","CG","CL","VH","CR","QC","PA","SA","PL","MV","MC","ME","AB","OL","AE","MO","CB","SV","VI"])
S_POT_A = Itinerary("BO", "MA", _skip = ["ML","CG","CL","VH","CR","QC","PA","SA","PL","MV","MC","ME","AB","OL","AE","MO","CB","SV","VI"])
S_IM_A = Itinerary("MC", "ME")
S_test = Itinerary("ME", "PE", _skip=["MG","IC","EU","GO","SP","AL","CO","ML","CG","CL","VH","CR","QC","PA","PL","MV"], _dir = Itinerary.DIRECTION_DESCENDING)


data = []
count = 4
i = 0
while i < count:
	tmp = [
		S_R5C_A.timetable(640+i*3600, "R5 1"),
		S_R5D_A.timetable(2010+i*3600, "R5 3"),
		S_R6D_A.timetable(2855+i*3600, "R6B 1"),
		S_R6M_D.timetable(1080+i*3600, "R6M 2"),
		S_R5C_D.timetable(1375+i*3600, "R5 4"),
		S_S8_D.timetable(420+i*3600, "S8 8"),
		S_S8_D.timetable(750+i*3600, "S8 10"),
		S_POT_D.timetable(2635+i*3600, "MERC 2", _extras = {"CG":0,"ML":0}),
		S_S8_D.timetable(1500+i*3600, "S8 2", _extras = {"QC":250,"LH":270}),
		S_R6D_D.timetable(2880+i*3600, "R6B 2"),
		S_S4_D.timetable(1620+i*3600, "S4 2", _extras = {"QC":250}),
		S_R5D_D.timetable(175+i*3600, "R5 2"),
		S_S4_D.timetable(2280+i*3600, "S4 4"),
		S_S8_D.timetable(3480+i*3600, "S8 6", _extras = {"QC":250}),
		S_L8_D.timetable(1500+i*3600, "L8 2"),
		S_S8_D.timetable(3000+i*3600, "S8 4", _extras = {"LH":270}),
		S_L8_D.timetable(2580+i*3600, "L8 4", _extras = {"LH":250}),
		S_L8_D.timetable(3000+i*3600, "L8 6"),
		S_S4_A.timetable(2100+i*3600, "S4 3", _extras = {"QC":230}),
		S_S8_A.timetable(2580+i*3600, "S8 5", _extras = {"LH":270}),
		S_L8_A.timetable(2340+i*3600, "L8 5"),
		S_S8_A.timetable(3120+i*3600, "S8 7"),
		S_R6L_A.timetable(3465+i*3600, "R6L 1", _extras = {"QC":250}),
		S_L8_A.timetable(60+i*3600, "L8 1"),
		S_S8_A.timetable(360+i*3600, "S8 1", _extras = {"LH":270}),
		S_S4_A.timetable(840+i*3600, "S4 1"),
		S_S8_A.timetable(1200+i*3600, "S8 3", _extras = {"QC":250}),
		S_L8_A.timetable(1440+i*3600, "L8 3"),
		S_IM_A.timetable(1080+i*3600, "MCME 1"),
		S_POT_A.timetable(2820+i*3600, "MERC 1", _extras = {"ML":0,"CG":0,"SV":0,"CR":0,"QC":0,"PA":0,"SA":0,"PL":0,"AB":0,"OL":540})
	]
	i += 1
	data += tmp;
#data.sort(key=lambda x: x.tms[0 if x.sts[0] == "PE" else -1]%3600)

fig, ax = plt.subplots()
for d in data:
	ax.plot(d.tms, d.sts)
plt.ylabel('Posició (estacions)')
plt.xlabel('Temps (segons)')
ax.grid()
ax.xaxis.set_major_locator(plticker.MultipleLocator(base=600))
ax.xaxis.set_minor_locator(plticker.MultipleLocator(base=60))
plt.show()

#print(createCSV(data, False))