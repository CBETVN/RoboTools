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


