import matplotlib.pyplot as plt
import sqlite3
import numpy
import csv

with open('image2pc.csv','rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    i = 0
    GPS_x = []
    GPS_y = []
    GPS_z = []

    for row in spamreader:
        # print ', '.join(row)
        i = i + 1
        # [x.strip() for x in row[0].split(',')]
        # GPS_x.append(x)
        newpoints = numpy.array([x.split(',') for x in row], dtype=numpy.float)
        print i,newpoints[0][2],newpoints[0][3],newpoints[0][4]
        GPS_x.append(newpoints[0][2])
        GPS_y.append(newpoints[0][3])
        GPS_z.append(newpoints[0][4])

#shape = (750,1000)
shape = (1000,750)
GPS_x_m = numpy.reshape( GPS_x,shape )
GPS_y_m = numpy.reshape( GPS_y,shape )
GPS_z_m = numpy.reshape( GPS_z,shape )


print GPS_x_m[100,3]
print GPS_y_m[100,3]
print GPS_z_m[100,3]

# print 'test', GPS_x_m[0,0]

numpy.savetxt('GPS_x.csv',GPS_x_m,delimiter=',')
numpy.savetxt('GPS_y.csv',GPS_y_m,delimiter=',')
numpy.savetxt('GPS_z.csv',GPS_z_m,delimiter=',')

# im = plt.imread('background.jpg')
# implot = plt.imshow(im)
# # put a blue dot at (10, 20)
# plt.scatter([10], [20])
# # put a red dot, size 40, at 2 locations:
# plt.scatter(x=[190,178.5,167,154,141,136.5,136.5], y=[391.5,394.5,397,400,403.5,406,407], c='r', s=5)
# # plt.plot([100,200,300],[200,150,200],'o')
# plt.show()


