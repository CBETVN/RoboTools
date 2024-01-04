import bpy
import addon_utils
import os
import bpy.utils.previews
icons_dict = bpy.utils.previews.new()


script_path = bpy.context.space_data.text.filepath
icons_dir = os.path.join(os.path.dirname(script_path), "icons")
icons_dict.load("custom_icon", os.path.join(icons_dir, "test.png"), 'IMAGE')



class VIEW3D_PT_RoboTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Test Panel"
    bl_label = "Test Panel"

    def draw(self, context):
        
        layout = self.layout
        layout.template_icon(icon_value=icons_dict["custom_icon"].icon_id, scale=8)





classes = (VIEW3D_PT_RoboTools)


def register():
    from bpy.utils import register_class
    bpy.utils.register_class(VIEW3D_PT_RoboTools)



def unregister():
    from bpy.utils import unregister_class
    bpy.utils.register_class(VIEW3D_PT_RoboTools)





if __name__ == "__main__":
    register()