import bpy

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

class OT_unwrap_white(bpy.types.Operator):
    """Unwrap in the whitest area of the BW Gradient"""
    bl_idname = "mesh.unwrap_white"
    bl_label = "Unwrap White"

    def execute(self, context):
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



class OT_unwrap_from_front_view(bpy.types.Operator):
    """Unraps from View"""
    bl_idname = "mesh.unwrap_from_front_view"
    bl_label = "Unwrap from Front View"

    def execute(self, context):

        objects = bpy.context.selected_objects
        bpy.context.area.type = 'VIEW_3D'
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



class VIEW3D_PT_RoboTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Robo Tools"
    bl_label = "Tools"

    def draw(self, context):
        
        
        self.layout.operator('mesh.unwrap_white')
        self.layout.operator('mesh.unwrap_from_front_view')
        self.layout.row()
        self.layout.prop(context.scene, "mytool_color")
        self.layout.row()
        self.layout.operator('object.set_brush_color')
        self.layout.operator('object.rec_outside')


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
        currentSpace = bpy.context.area.type                
        clr = context.scene.mytool_color
        bpy.data.brushes["Draw"].color = (clr[0], clr[1], clr[2])
        bpy.context.space_data.shading.color_type = 'VERTEX'
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        bpy.context.object.data.use_paint_mask_vertex = True
        bpy.ops.paint.vertex_color_set()
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}  

class OT_rec_outside(bpy.types.Operator):
    """Selects all meshes and rec. faces outside. Press again to exit show face orientation mode"""
    bl_idname = "object.rec_outside"
    bl_label = "Recalculate Outside"

    def execute(self, context):
        objects = bpy.context.scene.objects
        if bpy.context.space_data.overlay.show_face_orientation == True:
            bpy.context.space_data.overlay.show_face_orientation = False
        
        else:

            for obj in objects:
                obj.select_set(obj.type == "MESH")

            bpy.context.space_data.overlay.show_face_orientation = True
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="FACE")
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
        
        return{'FINISHED'}





def register():
    bpy.utils.register_class(OT_unwrap_white)
    bpy.utils.register_class(VIEW3D_PT_RoboTools)
    bpy.utils.register_class(OT_unwrap_from_front_view)
    bpy.utils.register_class(OT_set_brush_color)
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(OT_rec_outside)
       
        # Register the property per Scene, Object or whatever
    bpy.types.Scene.mytool_color = bpy.props.FloatVectorProperty(
                 name = "Color Picker",
                 subtype = "COLOR",
                 size = 4,
                 min = 0.0,
                 max = 1.0,
                 default = (1.0,1.0,1.0,1.0))


def unregister():
    bpy.utils.unregister_class(OT_unwrap_white)
    bpy.utils.unregister_class(VIEW3D_PT_RoboTools)
    bpy.utils.unregister_class(OT_unwrap_from_front_view)
    bpy.utils.unregister_class(OT_set_brush_color)
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.unregister_class(OT_rec_outside)

    

