import bpy
import gpu
import bgl
from gpu_extras.batch import batch_for_shader
import addon_utils
import os

class VIEW3D_PT_RoboTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Robo Tools"
    bl_label = "Robo Tools"

    def draw(self, context):
        
#        image_user = bpy.types.ImageTexture.image_user
        my_icon = bpy.data.images.load("C:/Users/sssto/OneDrive/Desktop/test.png")
        layout = self.layout
#        layout.template_icon(icon_value=1, scale=6)
        layout.template_image(my_icon, 'object.VIEW3D_PT_RoboTools',image_user, compact=False, multiview=False)    
        
        

#        self.layout.operator('mesh.unwrap_white')
#        x1 = 0
#        x2 = 200
#        y1 = 0
#        y2 = 200
#   
#        shader = gpu.shader.from_builtin('2D_IMAGE')
#        batch = batch_for_shader(
#        shader, 'TRI_FAN',
#        {
#            "pos": ((x1, y1), (x2, y1), (x2, y2), (x1, y2)),
#            "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
#        },
#        )
#    
##        image = bpy.data.images['logo']
#        image = bpy.data.images.load("C:/Users/sssto/OneDrive/Desktop/test.png")

#        if image.gl_load():
#            return # an exception happened
#    
#        bgl.glActiveTexture(bgl.GL_TEXTURE0)
#        bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)
#        shader.bind()
#        shader.uniform_int("image", 0)
#        batch.draw(shader)
#    
#        image.gl_free()
#    
#        handler = bpy.types.SpaceProperties.draw_handler_add(draw,(),'WINDOW','POST_PIXEL')









classes = (VIEW3D_PT_RoboTools)


#def register():
#    from bpy.utils import register_class



#def unregister():
#    from bpy.utils import unregister_class




def register():
    from bpy.utils import register_class
    bpy.utils.register_class(VIEW3D_PT_RoboTools)



def unregister():
    from bpy.utils import unregister_class
    bpy.utils.register_class(VIEW3D_PT_RoboTools)





if __name__ == "__main__":
    register()