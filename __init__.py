bl_info = {
    "name": "DispMapping",
    "author": "Derek Wang",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "N PANEL",
    "description": "Blender API 插件开发QQ交流群:735831986，微信:wx_frame3d",
    "warning": "",
    "wiki_url": "https://www.bilibili.com/video/BV1Y54y1M7GP/",
    "category": "DispMapping",
    }

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty
from .properties import DMMISCSettings
from .operators import myoperator 
from .ui import DM_PT_First_Panel, DM_PT_Second_Panel, DM_User_Preferences
        
classes = (
    DMMISCSettings,
    DM_PT_First_Panel,
    DM_PT_Second_Panel,
    DM_User_Preferences,
    myoperator.Translate_OT_Col_to_New_Location,
    myoperator.Add_OT_Non_PBR_Mat,
    myoperator.Add_OT_DM_to_Mesh_Object,
    )        

addon_keymaps = []

def register():
    bpy.app.handlers.depsgraph_update_post.clear()
    bpy.app.handlers.save_pre.clear()
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.dm_misc_settings = PointerProperty(type=DMMISCSettings)
 
    wm = bpy.context.window_manager
    #Window manager data-block defining open windows and other user interface data
    if wm.keyconfigs.addon:
        #Key maps configured as part of this configuration
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
        #Items in the keymap, linking an operator to an input event
        kmi = km.keymap_items.new('wm.call_panel', 'Y', 'PRESS', 
            # alt=False
            )
        kmi.properties.name = "ADDON_MISC_PT_DM_PANEL"
        #kmi.properties.name = "EXAMPLE_PT_panel_1"
        addon_keymaps.append((km, kmi))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    del bpy.types.Scene.dm_misc_settings

    
        
if __name__ == '__main__':
    register()
    
