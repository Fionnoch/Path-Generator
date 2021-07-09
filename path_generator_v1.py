# User inputs
material_thickness = 8 #mm
num_of_flanges = 5
front_pannel_length = 300 #mm
side_pannel_length = 250 #mm
num_of_pannels = 4
kerf = 1 #mm the width of the material lost from the cutting tool
pannel_height = 300 #mm

#calculated inputs
height_of_flange = pannel_height / num_of_flanges
bottom_up = True

#output vector
path_points = []

for i in range(num_of_pannels) :
    x_value = i * side_pannel_length
    for j in range(num_of_flanges):
        if bottom_up == True :
            y_value = height_of_flange * j
            if j == 0: #1st value is straight up     
                path_points.append([x_value, y_value])  
            elif j % 2: #returns true if there is a remainder. ie any odd number 
                path_points.append([x_value, y_value])
                path_points.append([x_value + material_thickness, y_value]) 
            else: #any even numbers 
                path_points.append([x_value + material_thickness, y_value])
                path_points.append([x_value, y_value]) 
        else:
            y_value = pannel_height - height_of_flange * j #start from the top
            if j == 0: #1st value is straight up     
                path_points.append([x_value, y_value])  
            elif j % 2: #returns true if there is a remainder. ie any odd number 
                path_points.append([x_value, y_value])
                path_points.append([x_value + material_thickness, y_value]) 
            else: #any even numbers 
                path_points.append([x_value + material_thickness, y_value])
                path_points.append([x_value, y_value]) 
                
    bottom_up = not(bottom_up)

          
print(path_points)                      
        