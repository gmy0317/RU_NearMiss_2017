import sqlite3
import csv
import numpy
import math
from shutil import copyfile

###########################################################
### read sql data to csv
conn = sqlite3.connect('tracking.sqlite')
conn.text_factory = str ## my current (failed) attempt to resolve this
cur = conn.cursor()
data = cur.execute("SELECT * FROM bounding_boxes")


with open('traffic_output.csv', 'wb') as f:
    writer = csv.writer(f)
    # writer.writerow(['Column 1', 'Column 2'])
    writer.writerows(data)
f.close()

############################################################
## find each object's average boundary size
# name0 = 'Data_Number'
# cur.execute('''ALTER TABLE bounding_boxes ADD COLUMN ''' + name0 + ''' INTEGER''')
# name1 = 'Area'
# cur.execute('''ALTER TABLE bounding_boxes ADD COLUMN ''' + name1 + ''' INTEGER''')
# name2 = 'Type'
# cur.execute('''ALTER TABLE bounding_boxes ADD COLUMN ''' + name2 + ''' INTEGER''')
# name3 = 'Area_Avg'
# cur.execute('''ALTER TABLE bounding_boxes ADD COLUMN ''' + name3 + ''' INTEGER''')
# cur.execute('''update bounding_boxes set Area = (x_bottom_right - x_top_left) * (y_bottom_right - y_top_left) ''')
# ############################################################
# ### read csv to matrix
#
row_num = 0

with open('traffic_output.csv','rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    for row in spamreader:
        row_num = row_num + 1

print('row_num',row_num)

#################################################################################################
## calculate average bounding box size and gps location of object

i = 0
j = 0
j0 = 0
object_id = []
frame = []
x1 = []
x2 = []
y1 = []
y2 = []
area = []
area_sum0 = 0
area_avg0 = 0
area_avg1 = 0
area_avg = []
object_type = []
center_10 = 0
center_20 = 0
center_1 = []  # bounding box center
center_2 = []  # bounding box lower side center
k = 0
row_num0 = 0

GPS_x = []
GPS_y = []
GPS_z = []
GPS_x = numpy.array(list(csv.reader(open("GPS_x.csv", "rb"), delimiter=","))).astype("float")
GPS_y = numpy.array(list(csv.reader(open("GPS_y.csv", "rb"), delimiter=","))).astype("float")
GPS_z = numpy.array(list(csv.reader(open("GPS_z.csv", "rb"), delimiter=","))).astype("float")

with open('traffic_output.csv','rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')


    for row in spamreader:
        # print ', '.join(row)
        i = i + 1
        row_num0 = row_num0 + 1
        # [x.strip() for x in row[0].split(',')]
        # GPS_x.append(x)
        newpoints = numpy.array([x.split(',') for x in row], dtype=numpy.float)
        object_id.append(newpoints[0][0])
        frame.append(newpoints[0][1])
        x1.append(newpoints[0][2])
        y1.append(newpoints[0][3])
        x2.append(newpoints[0][4])
        y2.append(newpoints[0][5])
        area0 = (newpoints[0][4]-newpoints[0][2])*(newpoints[0][5]-newpoints[0][3])
        center_10 = [int((newpoints[0][4]+newpoints[0][2])/2),int((newpoints[0][5]+newpoints[0][3])/2) ]  # center of the boundingbox
        center_1.append(center_10)

        center_20 = [int((newpoints[0][4]+newpoints[0][2])/2),int(newpoints[0][5]) ] # center the lower side of the bounding box
        center_2.append(center_20)
        area.append(area0)

        if j == int(newpoints[0][0]):
            area_sum0 = area_sum0 + area0
            k = k + 1
            area_avg0 = area_sum0 / k
            area_avg1 = area_avg0
            if row_num0 == row_num:
                 area_avg.append(area_avg0)
        else:
            area_avg.append(area_avg0)
            area_sum0 = area0
            j = int(newpoints[0][0])
            k = 1

        # print 'traffic_object',i,j, newpoints[0][0], newpoints[0][1], newpoints[0][2], newpoints[0][3], newpoints[0][4], newpoints[0][
        #     5], area0
        # print area_avg, len(area_avg),area_avg[2],int(area_avg[2])
#########################################################################
## define object type base on average area size, 1 for human, 2 for vehicle
i = -1
while (i < len(area_avg) - 1):
    i = i + 1
    if (int(area_avg[i]) > 1500):
        object_type0 = 2   # 2 for vehicle
        object_type.append(object_type0)
    else:
        object_type0 = 1  # 1 for human
        object_type.append(object_type0)
print('object_type',object_type)


############################################################################
## calculate GPS location base on xy in image
i = 0

# print(center_1[4],center_1[4][1])
test_xc = 0
test_xc_ = []
test_yc = 0
test_yc_ = []
test_zc = 0
test_zc_ = []
test_xb = 0
test_xb_ = []
test_yb = 0
test_yb_ = []
test_zb = 0
test_zb_ = []

print(center_1)
#print((center_2)) # 1000 by 750

print(GPS_x.shape) #750 by 1000

while( i <  row_num ):

     # test_xc = GPS_x[center_1[i][1]][ center_1[i][0]]
     # test_yc = GPS_y[center_1[i][1]][ center_1[i][0]]
     # test_zc = GPS_z[center_1[i][1]][ center_1[i][0]]

     test_xc = GPS_x[center_1[i][0]][ center_1[i][1]]
     test_yc = GPS_y[center_1[i][0]][ center_1[i][1]]
     test_zc = GPS_z[center_1[i][0]][ center_1[i][1]]

     test_xc_.append(test_xc)
     test_yc_.append(test_yc)
     test_zc_.append(test_zc)

     # test_xb = GPS_x[center_2[i][1]][center_2[i][0]]
     # test_yb = GPS_y[center_2[i][1]][center_2[i][0]]
     # test_zb = GPS_z[center_2[i][1]][center_2[i][0]]

     test_xb = GPS_x[center_2[i][0]][center_2[i][1]]
     test_yb = GPS_y[center_2[i][0]][center_2[i][1]]
     test_zb = GPS_z[center_2[i][0]][center_2[i][1]]

     test_xb_.append(test_xb)
     test_yb_.append(test_yb)
     test_zb_.append(test_zb)
     print('sql2pc',i, object_id[i], center_1[i][0], center_1[i][1], test_xc, test_yc, test_zc)  # 334 frames
     i = i + 1

output_result = [ object_id, test_xc_, test_yc_, test_zc_]
output_result = numpy.transpose(output_result)

numpy.savetxt('Output_GPS.csv',output_result,delimiter=',')
##################################################################
# #calculate movement
i = 0
Dif0  = 0  # distance movement XYZ
Dif0_ = 0 # distance movement XY
Dif   = []  # distance movement [XYZ]
Dif_  = [] # distance movement [XY]
Vel0  = 0
Vel   = []
Vel0_ = 0
Vel_  = []

Acc0  = 0
Acc   = []

Acc_alarm0 = 0
Acc_alarm = []
output_result = []
while (i < row_num - 1):
    # Dif0, Distance Difference calculated by center of the bounding box
    # Dif0 = math.sqrt((test_xc_[i + 1] - test_xc_[i])*(test_xc_[i + 1] - test_xc_[i]) + (test_yc_[i+ 1] - test_yc_[i])*(test_yc_[i+ 1] - test_yc_[i]) +(test_zc_[i+ 1] - test_zc_[i])*(test_zc_[i+ 1] - test_zc_[i]) )
    Dif0 = math.sqrt(
        (test_xc_[i + 1] - test_xc_[i]) * (test_xc_[i + 1] - test_xc_[i]) + (test_yc_[i + 1] - test_yc_[i]) * (
        test_yc_[i + 1] - test_yc_[i]))


    #Dif0_, Distance Difference calculated by lower side of the bounding box
    Dif0_ = math.sqrt(
        (test_xb_[i + 1] - test_xb_[i]) * (test_xb_[i + 1] - test_xb_[i]) + (test_yb_[i + 1] - test_yb_[i]) * (
        test_yb_[i + 1] - test_yb_[i]))


# control the calculated value, if the calculated distance movement is too large that over 10 feet, then use the previous distance movement value
    if(Dif0 > 20):
        Dif.append(Dif[i - 1])
    else:
            Dif.append(Dif0)

# control the calculated value, if the calculated distance movement is too large that over 10 feet, then use the previous distance movement value
    if(Dif0_ > 20):
        Dif_.append(Dif[i - 1])
    else:
        Dif_.append(Dif0_)


# calculate the object velocity base on current video frame speed and distance movement, here treat the fps as 12 fps
    # control the calculated velocity, if the velocity is too large, use the previous velocity
    Vel0 = float(Dif[i])*12 # unit  12 frame per second
    if(Vel0 > 80):
        Vel.append(Vel[i - 1])
    else:
        Vel.append(Vel0)

    Vel0_ = float(Dif_[i])*12 # unit 12 frame per second
    if(Vel0_ >80):
        Vel_.append(Vel_[i - 1])
    else:
        Vel_.append(Vel0_)

# calcualte the object acceleration base on the object speed
    Acc0 = (Vel[i] - Vel[i - 1])
    Acc.append(Acc0)
    if(Acc0 < -10):
        Acc_alarm0 = 'Y'
        Acc_alarm.append(Acc_alarm0)
    else:
        Acc_alarm0 = 'N'
        Acc_alarm.append(Acc_alarm0)
    # average pedestrian walking speed, 4.11- 4.95 from old to young
    print 'Dis_Vel', i,object_id[i],Dif[i],Dif_[i],Vel0,Vel0_,Acc0,Acc_alarm0
    i = i + 1
## save output result to csv


print('object_id',len(object_id))
print('Dif', len(Dif))
print('Dif_', len(Dif_))
print('Vel', len(Vel))
print('Vel_',len(Vel_))
print('Acc',len(Acc))

object_id_ = object_id[0:len(object_id) - 1]
print('object_id_modify',len(object_id_))

output_result = [object_id_,Dif, Dif_,Vel,Vel_,Acc]
output_result = numpy.transpose(output_result)

numpy.savetxt('Output_Velocity.csv',output_result,delimiter=',')
#######################################################################
# output result attributes list:
# frame number; object ID; Image Location(x0,x1,y0,y1), bounding box size(area), pointcloud center GPS(Xc,Yc,Zc), Lower cneter CPS(Xb,Yb,Zb), Diff_c, Diff_b, Velo_c, Velo_b; object_classification result
i = 0
object_seq = []
object_number =  max(object_id)
print(object_number)
velocity_avg = []
velocity_max = []
object_num = []
while (i <= object_number ):
    object_seq.append(object_id.index(i))

    if(i != 0):
        if(i == 1):
            print(0,'mean',numpy.mean(Vel[0:object_seq[1] - 1]),'max',numpy.max(Vel[0:object_seq[1] - 1]))
            velocity_avg.append(numpy.mean(Vel[0:object_seq[1] - 1]))
            velocity_max.append(numpy.max(Vel[0:object_seq[1] - 1]))
            object_num.append(0)
            print('1',object_seq[1] - 1)

        else:

            if(i == object_number ):
                print(i - 1, 'mean', numpy.mean(Vel[object_seq[i - 1]:object_seq[i] - 1]), 'max',
                      numpy.max(Vel[object_seq[i - 1]:object_seq[i] - 1]))
                print('3', object_seq[i - 1], object_seq[i] - 1)
                velocity_avg.append(numpy.mean(Vel[object_seq[i - 1]:object_seq[i] - 1]))
                velocity_max.append(numpy.max(Vel[object_seq[i - 1]:object_seq[i] - 1]))
                object_num.append(i - 1)


                print(i,'mean',numpy.mean(Vel[object_seq[i]:len(Acc)]),'max',numpy.max(Vel[object_seq[i]:len(Acc)]))
                print('2',object_seq[i], len(Acc))
                velocity_avg.append(numpy.mean(Vel[object_seq[i]:len(Acc)]))
                velocity_max.append(numpy.max(Vel[object_seq[i]:len(Acc)]))
                object_num.append(i)
            else:
                print(i - 1,'mean',numpy.mean(Vel[object_seq[i-1]:object_seq[i] - 1]),'max',numpy.max(Vel[object_seq[i-1]:object_seq[i] - 1]))
                print('3',object_seq[i-1],object_seq[i] - 1)
                velocity_avg.append(numpy.mean(Vel[object_seq[i-1]:object_seq[i] - 1]))
                velocity_max.append(numpy.max(Vel[object_seq[i-1]:object_seq[i] - 1]))
                object_num.append(i-1)
    i = i + 1
print object_seq


output_result = [object_num,velocity_avg,velocity_max]
output_result = numpy.transpose(output_result)
numpy.savetxt('Output_Avg_Velocity.csv',output_result,delimiter=',')

copyfile('traffic_output.csv','../5-result/traffic_output.csv')
copyfile('Output_Avg_Velocity.csv','../5-result/Output_Avg_Velocity.csv')
copyfile('Output_Velocity.csv','../5-result/Output_Velocity.csv')
copyfile('Output_GPS.csv','../5-result/Output_GPS.csv')

