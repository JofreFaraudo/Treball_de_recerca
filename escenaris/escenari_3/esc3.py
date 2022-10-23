## RUN GENERATOR.PY BEFORE THIS POINT

data = []
count = 4
i = 0
while i < count:
	tmp = [
		S_R5B_A.timetable(260+i*3600, "R5 1_"+str(i)),
		S_S4_A.timetable(420+i*3600, "S4 1_"+str(i)),
		S_L8_A.timetable(1020+i*3600, "L8 1_"+str(i)),
		S_R6B_A.timetable(1590+i*3600, "R6 1_"+str(i)),
		S_S4_A.timetable(1740+i*3600, "S4 3_"+str(i)),
		S_L8_A.timetable(2340+i*3600, "L8 3_"+str(i)),
		S_S8_A.timetable(2880+i*3600, "S8 1_"+str(i)),
		S_L8_A.timetable(3300+i*3600, "L8 5_"+str(i)),
		S_R6B_D.timetable(i*3600, "R6 2_"+str(i)),
		S_L8_D.timetable(240+i*3600, "L8 8_"+str(i)),
		S_L8_D.timetable(1320+i*3600, "L8 6_"+str(i)),
		S_S8_D.timetable(1680+i*3600, "S8 4_"+str(i)),
		S_S4_D.timetable(2280+i*3600, "S4 2_"+str(i)),
		S_R5B_D.timetable(2285+i*3600, "R5 2_"+str(i)),
		S_L8_D.timetable(2520+i*3600, "L8 6_"+str(i)),
		S_S4_D.timetable(3300+i*3600, "S4 4_"+str(i))
	]
	i += 1
	data += tmp;

fig, ax = plt.subplots()
for d in data:
	ax.plot(d.tms, d.sts)
plt.ylabel('Posició (estacions)')
plt.xlabel('Temps (segons)')
ax.grid()
ax.xaxis.set_major_locator(plticker.MultipleLocator(base=600))
ax.xaxis.set_minor_locator(plticker.MultipleLocator(base=60))
plt.show()

print(createCSV(data)) # Add parameter False to createCSV to replace seconds by HH:MM:SS format
