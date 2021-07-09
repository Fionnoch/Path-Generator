import numpy as np
import drawSvg as draw

# User inputs
material_thickness = 8 #mm
num_of_flanges = 4
front_pannel_length = 300 #mm
side_pannel_length = 250 #mm
num_of_pannels = 5
kerf = 1 #mm the width of the material lost from the cutting tool
pannel_height = 300 #mm

#calculated inputs
height_of_flange = pannel_height / num_of_flanges
bottom_up = True
x_value = 0

#output vector
path_points_origin = []
path_points = []
np_path_points_origin = np.zeros((1,2))
np_path_points = np.zeros((1,2))

total_num_of_data_points = (num_of_flanges*2)*(num_of_pannels)
       
np_points_test = np.empty((total_num_of_data_points, 2)) #make one long 2d array that contains the total number of points. Total number of points will be the number of points on 1 side x the number of pannels + 1 as start = 1 cut, middle = 1 cut and end = 1 cut
counter = 0
for j in range(num_of_flanges+1): #collect the values for 1 side and store as a vector 
    if bottom_up == True :
        y_value = height_of_flange * j
        if j == 0: #1st value is straight up     
            path_points_origin.append([x_value, y_value]) 
            np_points_test[counter] = (x_value, y_value)
            counter=counter+1
        elif j % 2: #returns true if there is a remainder. ie any odd number 
            path_points_origin.append([x_value, y_value])
            np_points_test[counter] = (x_value, y_value)
            counter = counter + 1
            if (y_value < pannel_height):
                path_points_origin.append([x_value + material_thickness, y_value]) 
                np_points_test[counter] = (x_value + material_thickness, y_value)
                counter = counter + 1
      
        else: #any even numbers 
            path_points_origin.append([x_value + material_thickness, y_value])
            np_points_test[counter] = (x_value + material_thickness, y_value)
            counter = counter + 1
            if (y_value < pannel_height):
                path_points_origin.append([x_value, y_value]) 
                np_points_test[counter] = (x_value, y_value)
                counter = counter + 1
       

side_pannel_jump = np.empty(num_of_flanges*2)
side_pannel_jump[0::4] = side_pannel_length + material_thickness + kerf*0.5
side_pannel_jump[1::4] = side_pannel_length + material_thickness + kerf*0.5
side_pannel_jump[2::4] = side_pannel_length + kerf*0.5
side_pannel_jump[3::4] = side_pannel_length + kerf*0.5

front_pannel_jump = np.empty(num_of_flanges*2)
front_pannel_jump[0::4] = front_pannel_length + kerf*0.5
front_pannel_jump[1::4] = front_pannel_length + kerf*0.5
front_pannel_jump[2::4] = front_pannel_length + material_thickness + kerf*0.5
front_pannel_jump[3::4] = front_pannel_length + material_thickness + kerf*0.5

first = True
front_pannel = True
for i in range(2,num_of_pannels+1):
    if first:
        np_points_test[(i-1)*counter:i*counter, 0] = np_points_test[(i-2)*counter:(i-1)*counter, 0] + front_pannel_jump
        first = not(first)
    else:
        if front_pannel:
            np_points_test[(i-1)*counter:i*counter, 0] = np_points_test[(i-2)*counter:(i-1)*counter, 0] + (front_pannel_jump + kerf*0.5)
        else:
            np_points_test[(i-1)*counter:i*counter, 0] = np_points_test[(i-2)*counter:(i-1)*counter, 0] + (side_pannel_jump + kerf*0.5)
    
    np_points_test[(i-1)*counter:i*counter, 1] = np.flip(np_points_test[(i-2)*counter:(i-1)*counter, 1])
    front_pannel = not(front_pannel)
    #print ( np_points_test[(i-1)*counter:i*counter, 0] )
    #print ( np_points_test[(i-1)*counter:i*counter, 1] )

print(np_points_test)

d = draw.Drawing(max(np_points_test[:,0]), max(np_points_test[:,1]), origin=(0,0), displayInline=False)

d.append(draw.Lines(np_points_test,
                    close=False,
            fill='#eeee00',
            stroke='black'))

#p = draw.Path(stroke_width=kerf, stroke='black', fill='black', fill_opacity=1)



#p.M(np_points_test[0,0], np_points_test[0,1])  # Start path at point (-10, 20)
d.append(p)

d.setPixelScale(2)  # Set number of pixels per geometry unit
#d.setRenderSize(400,200)  # Alternative to setPixelScale
d.saveSvg('example.svg')
d.savePng('example.png')

d.rasterize()  # Display as PNG
d  # Display as SVG
