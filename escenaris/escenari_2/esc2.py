## RUN GENERATOR.PY BEFORE THIS POINT
data = []
count = 4
i = 0
while i < count:
	tmp = [
		S_S4_A.timetable(120+i*3600, "S4 1_"+str(i)),
		S_L8_A.timetable(480+i*3600, "L8 1_"+str(i)),
		S_S8_A.timetable(825+i*3600, "S8 1_"+str(i), _extras = {"QC": 270}),
		S_L8_A.timetable(1140+i*3600, "L8 3_"+str(i)),
		S_R6_A.timetable(1775+i*3600, "R6 1_"+str(i)),
		S_S4_A.timetable(1920+i*3600, "S4 3_"+str(i)),
		S_L8_A.timetable(2280+i*3600, "L8 5_"+str(i)),
		S_S8_A.timetable(2625+i*3600, "S8 3_"+str(i), _extras = {"QC": 270}),
		S_L8_A.timetable(2940+i*3600, "L8 7_"+str(i)),
		S_R5_A.timetable(3575+i*3600, "R5 1_"+str(i)),
		S_R6_D.timetable(i*3600, "R6 2_"+str(i)),
		S_S8_D.timetable(45+i*3600, "S8 2_"+str(i), _extras = {"QC": 300}),
		S_L8_D.timetable(120+i*3600, "L8 2_"+str(i)),
		S_L8_D.timetable(720+i*3600, "L8 4_"+str(i)),
		S_S4_D.timetable(960+i*3600, "S4 2_"+str(i)),
		S_L8_D.timetable(1620+i*3600, "L8 6_"+str(i)),
		S_R5_D.timetable(1685+i*3600, "R5 2_"+str(i)),
		S_S8_D.timetable(2195+i*3600, "S8 4_"+str(i), _extras = {"QC": 300}),
		S_S4_D.timetable(2400+i*3600, "S4 4_"+str(i)),
		S_L8_D.timetable(2520+i*3600, "L8 8_"+str(i))
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
