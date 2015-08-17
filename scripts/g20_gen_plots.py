#!/bin/python3.3
import os, re

rr = 50
it = 500
it_roll=81
r = 15
a=os.system("mkdir -p plots")
def get_item_line(line, i): # get the ith entry in a comma-seperated line 
    if line:
        li = re.findall(r'[\d.]+',line)
        return float(li[i])
    return None


def average_generator(p):
    time_average={}
    f=open('data/g20_project.csv')
    f = f.read()
    list_of_lines = f.split('\n')

    for i in range(1, it+1):
        time_average[i] = 0
        for j in range(1, rr+1):
            line = list_of_lines[(i-1)*rr + j - 1]
            k = get_item_line(line, 0)
            if k and k <= i:
                time_average[k] += get_item_line(line, p)
    return(time_average)

step_time_average=average_generator(2)
loop_time_average=average_generator(6)
collision_time_average=average_generator(3)
velocity_time_average=average_generator(4)
position_time_average=average_generator(5)
#~ #-----------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.axes
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

def plot1():
    x=list(step_time_average.values())
    x_data=list(loop_time_average.values())

    figure, ax1 = plt.subplots()
    ax2=ax1.twinx()
    p1, =ax1.plot(x_data, label="loop time average")
    p2=ax2.bar(range(1,it + 1), x, align='center', label = "step_time_average", edgecolor = 'red', width=0.5)
    p3=ax1.axhline(y=max(x_data), color='red', zorder=1, label = 'max_line')
    p4=ax1.axhline(y=min(x_data[1:10]), color='green', zorder=1, label = 'min_line')
    plt.xlabel("iteration")
    plt.subplots_adjust()
    plt.title("loop and step time_average", fontsize=14, fontweight='bold')
    plt.legend([p1, p2, p3, p4], ["loop time average", "step time average", "max loop time", "min loop time"], loc=2)
    plt.savefig('plots/g20_project_plot01.png', bbox_inches='tight')
    plt.close()
#-----------------------------------------------------------------------

# Question 2:
def plot2():
    x1=list(step_time_average.values())
    x2=list(collision_time_average.values())
    x3=list(velocity_time_average.values())
    x4=list(position_time_average.values())
    x_sum=[a+b+c+d for a, b, c, d in zip(x1, x2, x3, x4)]
    plt.plot(x1, label="step_time_average")
    plt.plot(x2, label="collision_time_average")
    plt.plot(x3, label="velocity_time_average")
    plt.plot(x4, label="position_time_average")
    plt.plot(x_sum, label="average_sum")
    plt.xlabel("iteration")
    plt.ylabel("time_average")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, borderaxespad=0.)
    plt.savefig('plots/g20_project_plot02.png', bbox_inches='tight')
    plt.close()
#-----------------------------------------------------------------------

# Question 3:

def plot3():
    y=list(step_time_average.values())
    x=range(1,it+1)
    y_mean = sum(y)/len(y)
    yerr = [(err - y_mean)**2/y_mean for err in y]
    p1, =plt.plot(x,y,  color='b')
    p2=plt.errorbar(x, y, yerr=yerr, fmt=None, ecolor = "green")
    plt.legend([p1, p2], ["step time average","error bars"])
    plt.title("Error Analysis (Deviation form Mean)", fontsize=14, fontweight='bold')
    plt.xlabel("Iteration")
    plt.ylabel("step time average")
    plt.savefig('plots/g20_project_plot03.png', bbox_inches='tight')
    plt.close()


#-----------------------------------------------------------------------
# Question 4:

#~ import pylab as P
#~ 
def plot4():
    f=open('data/g20_project.csv')
    f=f.read()
    list_of_lines = f.split('\n')
    step_time_average={}
    for i in range(1,rr+1):
        line=list_of_lines[(it_roll-1)*rr + i - 1]
        k = get_item_line(line, 1)
        if k:
            step_time_average[k] = get_item_line(line, 2)

    x_data=list(step_time_average.values())
    poop = np.array(x_data)


    y=plt.hist(x_data, bins = 50)
    plt.hist(x_data, 5000, histtype='step', cumulative = True, label= "Cumulative Plot")
    #~ cumulative=np.cumsum(y[0])
    #~ j=0
    #~ newlist=[]
    #~ dic={}
    #~ for i in cumulative:
        #~ if i not in newlist:
            #~ newlist.append(i)
            #~ dic[j]=i
        #~ j+=1
    #~ plt.plot(list(dic.values()), marker='o', color='b')
    plt.savefig('plots/g20_project_plot04.png', bbox_inches='tight')
    plt.close()
#-----------------------------------------------------------------------
#Question 5:
import random
def plot5():
    f=open('data/g20_project.csv')
    f=f.read()
    f=f.split('\n')
    #~ print(f[0:10])

    r_dic={}
    for i in range(1, it+1):
        #~ print((i-1)*rr, ' ', i*rr-1)
        num_list=random.sample(range((i-1)*rr, i*rr-1), r)
        #~ print('this', num_list)
        r_dic[i]=0
        for j in num_list:
            r_dic[i]+=get_item_line(f[j], 2)
    l =len(list(r_dic.values()))
    x=range(l)
    y=list(r_dic.values())
    y1=list(step_time_average.values())
    #~ plt.scatter(x,y,alpha=0.5, edgecolor='black',
    #~ facecolor='red', linewidth=0.15)

    m1,c1 = np.polyfit(x,y,1)
    m2,c2 = np.polyfit(x,y1,1)
    #~ fit_fn = np.poly1d(fit)
    #~ fit_fn2 = np.poly1d(fit2)

    p1=plt.plot(y, 'o',label="random sample averaging")
    p2=plt.plot(y1, 'o',label = "step time averaging")
    p3=plt.plot(m1*x + c1, label= "least square fit for random")
    p4=plt.plot(m2*x + c2, label= "least square fit")
    plt.title("Curve fitting and random sampling", fontsize=14, fontweight='bold')
    #~ plt.legend([p1, p2], ["step time average using random sampling", "step time average"])
    plt.xlabel("Iteration")
    plt.ylabel("Step time average")
    plt.legend(["step time average(random sampling)", "best fit:random sample" ,"step time average","best fit:Step time average"])
    plt.savefig('plots/g20_project_plot05.png', bbox_inches='tight')
    plt.close()


plot1()
plot2()
plot3()
plot4()
plot5()
