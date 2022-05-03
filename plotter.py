
from tkinter import *
import json
from scipy.interpolate import interp1d
import numpy as np
import time

start = time.time()
root = Tk()
cans=Canvas(root,height=800,width=1500,background="white")
cans.pack()

with open('ecgData.txt') as json_file:
    data = json.load(json_file)
lead1 = data["lead1"]
lead2 = data["lead2"]
lead3 = data["lead3"]
lead4 = data["lead4"]
lead5 = data["lead5"]
lead6 = data["lead6"]
lead7 = data["lead7"]
lead8 = data["lead8"]
lead9 = data["lead9"]
lead10 = data["lead10"]
lead11 = data["lead11"]
lead12 = data["lead12"]

# Raw data from json file. 1000 mesurements/secound - to much for python to handle
EcgDataLong = [lead1,lead2,lead3,lead4,lead5,lead6,lead7,lead8,lead9,lead10,lead11,lead12]
EcgDataLong= np.array(EcgDataLong)

# Matrix for the short wersion of data
EcgDataShort =  np.zeros(shape=(12,150))

# Matrix for the fit-to-screen data. This is 10s of ECG data, each secound is 150 mesurements long
EcgDataFit = np.zeros(shape=(12,1500))
print("Shape of EKG data numpy array: ",np.shape(EcgDataLong))

# interploation of data, from 1000 to 150 samples per secound
x = np.linspace(0, 2, num=1000, endpoint=True)
xnew = np.linspace(0, 2, num=150, endpoint=True)
for index, lead in enumerate(EcgDataLong):
    f = interp1d(x, lead, kind='cubic')
    EcgDataShort[index] = f(xnew)
print("Shape of EKG data numpy array after interpolation: ",np.shape(EcgDataShort))


### Repeat the data 10 times, to get 10s of data on screen (1000 samples = 1s)
for index, lead in enumerate(EcgDataShort):
    leadOrg = lead
    for a in range(0,9):
        lead = np.append(lead,leadOrg)
    EcgDataFit[index] = lead
print("Shape of EKG data numpy array after repeat operation: ",np.shape(EcgDataFit))

# Adjust the aplitude of the mesurements
g = 0.8    
# Vertical ofset for the lines   
offset = [60,120,180,240,300,360,420,480,540,600,660,720]

delay = 1  # milliseconds

# draws the lines on canvas from data inside EcgDataFit
def draw_line(i=1,count=0,data=EcgDataFit):
    if i == 1499:
        i = 0
        count +=1

    # add tag to every line for the delete_line function to delete the corect lines
    tag = "A"+str(count)+str(i)
    cans.create_line(i-1, offset[0] - (data[(0,i-1)] * g), i, offset[0] - (data[(0,i)] * g), tags = tag)
    cans.create_line(i-1, offset[1] - (data[(1,i-1)] * g), i, offset[1] - (data[(1,i)] * g), tags = tag)
    cans.create_line(i-1, offset[2] - (data[(2,i-1)] * g), i, offset[2] - (data[(2,i)] * g), tags = tag)
    cans.create_line(i-1, offset[3] - (data[(3,i-1)] * g), i, offset[3] - (data[(3,i)] * g), tags = tag)
    cans.create_line(i-1, offset[4] - (data[(4,i-1)] * g), i, offset[4] - (data[(4,i)] * g), tags = tag)
    cans.create_line(i-1, offset[5] - (data[(5,i-1)] * g), i, offset[5] - (data[(5,i)] * g), tags = tag)
    cans.create_line(i-1, offset[6] - (data[(6,i-1)] * g), i, offset[6] - (data[(6,i)] * g), tags = tag)
    cans.create_line(i-1, offset[7] - (data[(7,i-1)] * g), i, offset[7] - (data[(7,i)] * g), tags = tag)
    cans.create_line(i-1, offset[8] - (data[(8,i-1)] * g), i, offset[8] - (data[(8,i)] * g), tags = tag)
    cans.create_line(i-1, offset[9] - (data[(9,i-1)] * g), i, offset[9] - (data[(9,i)] * g), tags = tag)
    cans.create_line(i-1, offset[10] - (data[(10,i-1)] * g), i, offset[10] - (data[(10,i)] * g), tags = tag)
    cans.create_line(i-1, offset[11] - (data[(11,i-1)] * g), i, offset[11] - (data[(11,i)] * g), tags = tag)
    # run this function every milisecound
    root.after(delay, draw_line, i+1, count)
    
def delete_line(i=0,count=0,start=time.monotonic_ns()):
    # time mesurement
    if i == 1:
        start = time.monotonic_ns()
        
    if i == 1499:
        i = 0
        count+=1
        end = time.monotonic_ns()
        #print((end-start)*1e-9)

    # delete the 20 old samples from the grapf in front of the new lines. Moving strip 
    if count > 0:
        for a in range(i,i+20):
            cans.delete("A"+str(count-1)+str(a))
            #print("A"+str(count-1)+str(a))

    root.after(delay, delete_line, i+1,count,start)

# scale the data every 100ms just to se that there is indeen new data being plotted. this can be removed. 
def manipulation():
    for i, lead in enumerate(EcgDataFit):
        for j, num in enumerate(lead):
            EcgDataFit[i,j] = EcgDataFit[i,j]*0.99
    root.after(delay*100, manipulation)


draw_line()
delete_line()   
manipulation()     

root.mainloop()