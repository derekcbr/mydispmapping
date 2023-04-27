import bpy
import bmesh
import numpy as np
import os
import sys
from random import random, uniform, randint, randrange, choice
from mathutils import Vector, Matrix

from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import Panel, PropertyGroup, Operator, AddonPreferences


class DM_PT_First_Panel(Panel):
    bl_idname = "ADDON_MISC_PT_N_PANEL"
    bl_label = "置换贴图"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DispMapping"
    def draw(self, context):
        settings = context.scene.dm_misc_settings
        layout = self.layout
        
        row = layout.row()
        col = row.column(align=True)
        col.prop(settings, 'collectionName')

        row = layout.row()
        col = row.column(align=True)
        col.prop(settings, 'boolName')
        
        row = layout.row()
        col = row.column(align=True)
        col.prop(settings, 'locx')
        col = row.column(align=True)
        col.prop(settings, 'locy')
        col = row.column(align=True)
        col.prop(settings, 'locz')
        
        row = layout.row()        
        col = row.column(align=True)
        col.operator("object.translatecol", text='Translate Col')
        
        row = layout.row()        
        col = row.column(align=True)
        col.operator("object.addnonpbrmat", text='Add Glass')

        row = layout.row()
        col = row.column(align=True)
        col.prop(settings, 'dmthickness')

        

        row = layout.row()        
        col = row.column(align=True)
        col.operator("object.startdm", text='物体表面置换贴图')

class DM_PT_Second_Panel(Panel):
    bl_idname = "ADDON_MISC_PT_DM_PANEL"
    bl_label = "置换贴图目录文件设置"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DispMapping"
    def draw(self, context):
        settings = context.scene.dm_misc_settings
        layout = self.layout
        box = layout.box()
        box.label(text="选择贴图文件", icon='PRESET')

        row = box.row()
        col = row.column(align=True)
        col.prop(settings, 'isclockwise')
        col = row.column(align=True)
        col.prop(settings, 'isbyrandomfile')

        row = box.row()        
        col = row.column(align=True)
        col.prop(settings, 'dmimgsdir')
        row = box.row()        
        col = row.column(align=True)
        col.prop(settings, 'dmimgenumfiles')

        

class DM_User_Preferences(AddonPreferences):
    bl_idname = __package__


    grayscale_dir : StringProperty(
        name="Grayscale Bmp Folder", 
        #default="", 
        #default=r"E:\documents\Blender\插件\实物模型\灰度图\动物\蝙蝠类", 
        default=r"E:\documents\Blender\插件\实物模型\灰度图\动物", 
        #default=r"E:\documents\Blender\插件\实物模型\灰度图", 
        subtype='DIR_PATH')


    def draw(self, context):
        miscsettings = context.scene.dm_misc_settings
        layout = self.layout

        row = layout.row()
        row.prop(self, "grayscale_dir")
        