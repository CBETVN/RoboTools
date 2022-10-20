import bpy


objects = bpy.context.selected_objects
mat = bpy.data.materials.new(name="VerticalBW")


for obj in objects:
    obj.select_set(obj.type == "MESH")
    obj.data.materials.clear()



for o in objects:
    if o.type == 'MESH':
        if len(o.material_slots) < 1: #if no materials on the object
            o.data.materials.append(mat) 
            #this will create a slot and add the material
        else:
            o.material_slots[o.active_material_index].material = mat 
            #if there are slots, assign the material to the active one


# import bpy
# ob = bpy.context.active_object

# # Get material
# mat = bpy.data.materials.get("Material")
# if mat is None:
#     # create material
#     mat = bpy.data.materials.new(name="Material")

# # Assign it to object
# if ob.data.materials:
#     # assign to 1st material slot
#     ob.data.materials[0] = mat
# else:
#     # no slots
#     ob.data.materials.append(mat)





# mat = "VerticalBW"


# if bpy.data.materials.find(mat) >= 0:
#     print("Found one!")
# else:
#     print("None")




#This shit  WORKS!


        

# mat = "VerticalBW"        
        
# for i in bpy.data.materials:
#     if str(mat) != i.name:
#         bpy.data.materials.remove(i) 