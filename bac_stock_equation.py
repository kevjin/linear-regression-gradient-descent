import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import openpyxl
wb = openpyxl.load_workbook('bac.xlsx')
type(wb)
wb.get_sheet_names()
sheet = wb.get_sheet_by_name('Sheet1')
print sheet
anotherSheet = wb.active
print anotherSheet

origin = 0
time = 0
timeaxis = []
priceaxis = []
equ_axis = []

theta_first = 0
theta_second = 0
theta_third = 0
ALPHA = .000000008

for i in reversed(range(1,128,1)):
	date = anotherSheet.cell(row=i, column=1).value
	close_price = anotherSheet.cell(row=i, column=3).value
	date_array = str(date).split('-')
	month_iter = int(date_array[1])
	calendar = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
	while(month_iter!=0):
		month_iter-=1
		time+=calendar.get(month_iter,0)
	time+=int(date_array[2].split()[0])
	if(origin==0):
		origin=time
	time-=origin
	timeaxis.append(time)
	priceaxis.append(close_price)
	time=0
print "It worked!1"


previous = 100000 #arbitrary value that's not 0 or .1 close to it
iter = 0
while iter<100000:
	previous = theta_second
	sum_one = 0
	sum_two = 0
	sum_three = 1
	for i in range(0,127,1):
		x = timeaxis[i] 
		sum_one += (theta_first + theta_second*x + theta_third*x*x - priceaxis[i])
		sum_two += (theta_first + theta_second*x + theta_third*x*x - priceaxis[i])*x
		sum_three +=(theta_first + theta_second*x + theta_third*x*x - priceaxis[i])*x*x
	theta_first -= ALPHA*sum_one/127
	theta_second -= ALPHA*sum_two/127
	theta_third -= ALPHA*sum_three/127
	#print "This is the index of the iteration", iter, "theta_first:", theta_first, "theta_second:", theta_second, "theta_third", theta_third
	iter+=1

for i in xrange(0,127,1):
	x = timeaxis[i]
	equ_axis.append(theta_third*x*x + theta_second*x + theta_first)
print "equation points plotted!"

plt.plot(timeaxis,priceaxis)
plt.savefig("actualdata.png")
plt.plot(timeaxis,equ_axis)
plt.savefig("equationed.png")