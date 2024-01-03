import bpy
import addon_utils

bl_info = {
    "name" : "robo_tools_addon",
    "author" : "CBETVN",
    "description" : "",
    "blender" : (3, 00  , 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}



class VIEW3D_PT_RoboTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Robo Tools"
    bl_label = "Robo Tools"

    def draw(self, context):
        

        self.layout.operator('mesh.unwrap_white')
        self.layout.operator('mesh.unwrap_from_view')
        self.layout.row()
        self.layout.prop(context.scene, "mytool_color")
        self.layout.row()
        self.layout.operator('object.set_brush_color')
        self.layout.operator('object.rec_outside')
        self.layout.operator('object.delete_all_materials')
        self.layout.operator('object.create_vertbw_material')
        self.layout.operator('object.origin_to_selected')
        self.layout.operator('mesh.orientation_from_normals')
        self.layout.operator('panel.panelthree')
        props = bpy.context.scene.TextField
        layout = self.layout

        col = layout.column(align=True)
        rowsub = col.row(align=True)

        rowsub.label(text="Pick a name")

        rowsub = col.row(align=True)
        col2 = layout.column()
        rowsub2 = col2.row()
        rowsub2.operator("object.select_by_query", text="Rename")
        rowsub.prop(props, "newname", text="")






class OT_unwrap_white(bpy.types.Operator):
    """Unwrap in the whitest area of the BW Gradient"""
    bl_idname = "mesh.unwrap_white"
    bl_label = "Unwrap White"

    def execute(self, context):

        #Change the shadind type to "Material Preview"
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas: # iterate through areas in current screen
                if area.type == 'VIEW_3D':
                    #bpy.ops.object.mode_set(mode='EDIT')
                    for space in area.spaces: # iterate through spaces in current VIEW_3D area
                        if space.type == 'VIEW_3D': # check if space is a 3D view
                            space.shading.type = 'MATERIAL'
                            #bpy.ops.object.mode_set(mode='EDIT')

        currentSpace = bpy.context.area.type
        bpy.ops.object.mode_set(mode='EDIT')
        # bpy.context.area.type = 'VIEW_3D'
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=True)
        bpy.context.area.type = 'IMAGE_EDITOR'
        bpy.context.area.ui_type = 'UV'
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.weld()
        bpy.ops.transform.translate(value=(0, 0.49, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.area.type = currentSpace
        # bpy.ops.object.editmode_toggle()
        return {'FINISHED'} 



class OT_unwrap_from_view(bpy.types.Operator):
    """Unraps from View"""
    bl_idname = "mesh.unwrap_from_view"
    bl_label = "Unwrap from View"

    def execute(self, context):

        #Change the shadind type to "Material Preview"
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas: # iterate through areas in current screen
                if area.type == 'VIEW_3D':
                    for space in area.spaces: # iterate through spaces in current VIEW_3D area
                        if space.type == 'VIEW_3D': # check if space is a 3D view
                            space.shading.type = 'MATERIAL'

        objects = bpy.context.selected_objects
        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.object.mode_set(mode='OBJECT')
        for self in objects:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = self
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="FACE")
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=True)
            bpy.ops.object.mode_set(mode='OBJECT')
        
        for i in objects:
            bpy.data.objects[i.name].select_set(True)
       
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}     

    
class TextField(bpy.types.PropertyGroup):

    newname: bpy.props.StringProperty(default="Part")


class RenameObjects(bpy.types.Operator):

    bl_idname = "object.select_by_query"
    bl_label = "Selection of object by query"

    def execute(self, context):
        print(bpy.context.scene.TextField.newname)
        
        objects = bpy.context.selected_objects
        
        
        for (i,o) in enumerate(objects):
            o.name = bpy.context.scene.TextField.newname+"{:03d}".format(i+1)

        return {'FINISHED'}


class SimpleOperator(bpy.types.Operator):
    """Gets the color from the Color Picker"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        clr = context.scene.mytool_color
        print (clr[0], clr[1], clr[2], clr[3])
        return {'FINISHED'}



class OT_set_brush_color(bpy.types.Operator):
    """Set Vert color for selected vertices"""
    bl_idname = "object.set_brush_color"
    bl_label = "Set Vertex Color"

    def execute(self, context):

        #Change the shadind type to "SOLID"
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas: # iterate through areas in current screen
                if area.type == 'VIEW_3D':
                    for space in area.spaces: # iterate through spaces in current VIEW_3D area
                        if space.type == 'VIEW_3D': # check if space is a 3D view
                            space.shading.type = 'SOLID'



        currentSpace = bpy.context.area.type                
        clr = context.scene.mytool_color
        bpy.data.brushes["Draw"].color = (clr[0], clr[1], clr[2])
        bpy.context.space_data.shading.color_type = 'VERTEX'
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Draw")
        bpy.context.object.data.use_paint_mask_vertex = True
        bpy.ops.paint.vertex_color_set()
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}  

class OT_rec_outside(bpy.types.Operator):
    """Selects all meshes and rec. faces outside. Press again to exit show face orientation mode"""
    bl_idname = "object.rec_outside"
    bl_label = "Recalculate Outside"

    def execute(self, context):
        #Iterates over all objects in the scene
        objects = bpy.context.scene.objects
        #Gets Selected Objects if there are any
        so = bpy.context.selected_objects
        #Toggles off Face Orientation mode
        if bpy.context.space_data.overlay.show_face_orientation == True:
            bpy.context.space_data.overlay.show_face_orientation = False
        
        else:

            for obj in objects:
                obj.select_set(obj.type == "MESH")

            for o in so:
                if o.type != "MESH":
                    o.select_set(False)       

            bpy.context.space_data.overlay.show_face_orientation = True
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="FACE")
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
        
        return{'FINISHED'}

class OT_delete_all_materials(bpy.types.Operator):
    """Delete all Materials from selected objects"""
    bl_idname = "object.delete_all_materials"
    bl_label = "Delete all Materials"

    def execute(self, context):
        objects = bpy.context.selected_objects
        for obj in objects:
            if obj.type == "MESH":
                obj.data.materials.clear()

        return{'FINISHED'}




class OT_origin_to_selected(bpy.types.Operator):
    """Set origin to selected"""
    bl_idname = "object.origin_to_selected"
    bl_label = "Origin to Selected"

    def execute(self, context):
        #Some stackoverflow Ju Ju Magic
        cursorloc = [bpy.context.scene.cursor.location[0], bpy.context.scene.cursor.location[1], bpy.context.scene.cursor.location[2]]
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                override['region'] = area.regions[4]
                bpy.ops.view3d.snap_cursor_to_selected(override)
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                break



        bpy.context.scene.cursor.location = (cursorloc)

        return{'FINISHED'}









class OT_create_vertbw_material(bpy.types.Operator):
    """Create and assign VBWmaterial to selected objects"""
    bl_idname = "object.create_vertbw_material"
    bl_label = "Assign VerticalBW Mat"
    
    def execute(self, context):
        matname = "VerticalBW"
        vbw =  None       
        objects = bpy.context.selected_objects
        addon = "robo_tools_addon"
        addonpath = None

        for mod in addon_utils.modules():
            if mod.bl_info['name'] == "robo_tools_addon":
                addonpath = mod.__file__


        vbwpath = addonpath.replace('robo_tools_addon.py', '')
        texturepath = vbwpath+"VerticalBW.png"
         
        #Change the shadind type to "Material Preview"
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas: # iterate through areas in current screen
                if area.type == 'VIEW_3D':
                    for space in area.spaces: # iterate through spaces in current VIEW_3D area
                        if space.type == 'VIEW_3D': # check if space is a 3D view
                            space.shading.type = 'MATERIAL'


        #If There arent any materials create VBW material

        bpy.data.materials.new(name=matname)
        mat = bpy.data.materials["VerticalBW"]
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        
        for i in bpy.data.materials["VerticalBW"].node_tree.nodes:
            if  i.type == "TEX_IMAGE":
                bpy.data.materials["VerticalBW"].node_tree.nodes.remove(i)
        
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')

        # Search and remove loaded duplicates of "VerticalBW" texture
        for i in bpy.data.images:
    
            if matname in i.name:
                bpy.data.images.remove(i) 

        
        
        for i in bpy.data.images:
            if i.name != "VerticalBW.png":
                bpy.data.images.load(texturepath)
                break
         

        # texImage.image = bpy.data.images.load(texturepath)
        texImage.image = bpy.data.images["VerticalBW.png"]
        mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

        



        #Remove all materials except "VerticalBW"
        for i in bpy.data.materials:
            if str(matname) != i.name:
                bpy.data.materials.remove(i)

        #Clear slots of selected 'Mesh' objects then assign "VerticalBW"Material"
        for o in objects:
            if o.type == "MESH":
                o.data.materials.clear()
                o.data.materials.append(bpy.data.materials["VerticalBW"])  

        return{'FINISHED'}








class OT_orientation_from_normals(bpy.types.Operator):
    """Orients pivot along normals"""
    bl_idname = "mesh.orientation_from_normals"
    bl_label = "Orientation from Normals"

    def execute(self, context):
        cursorloc = [bpy.context.scene.cursor.location[0], bpy.context.scene.cursor.location[1], bpy.context.scene.cursor.location[2]]
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'
        bpy.ops.transform.create_orientation(use=True)
        newto = str(bpy.context.scene.transform_orientation_slots[0].type)
        bpy.ops.object.editmode_toggle()
        
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.wm.tool_set_by_id(name='builtin.move')
        bpy.context.scene.tool_settings.use_transform_data_origin = True
        bpy.ops.transform.transform(mode='ALIGN', value=(0, 0, 0, 0), orient_type= newto, orient_matrix_type= newto, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        bpy.context.scene.transform_orientation_slots[0].type = newto
        bpy.ops.transform.delete_orientation()
        bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
        bpy.context.scene.tool_settings.use_transform_data_origin = False
        bpy.context.scene.cursor.location = (cursorloc)
        return{'FINISHED'}        



classes = (
    TextField, RenameObjects, OT_unwrap_white,VIEW3D_PT_RoboTools, OT_unwrap_from_view, OT_set_brush_color, 
    SimpleOperator, OT_rec_outside, OT_delete_all_materials, OT_create_vertbw_material, 
    OT_origin_to_selected, OT_orientation_from_normals)





def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # Register TextField
    bpy.types.Scene.TextField = bpy.props.PointerProperty(type=TextField)

       
    # Register the property per Scene, Object or whatever
    bpy.types.Scene.mytool_color = bpy.props.FloatVectorProperty(
                 name = "Color Picker",
                 subtype = "COLOR",
                 size = 4,
                 min = 0.0,
                 max = 1.0,
                 default = (1.0,1.0,1.0,1.0))


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    # $ delete TextField on unregister
    del(bpy.types.Scene.TextField) 

    
    

    
    
    
    
    
    
    
    
    

    