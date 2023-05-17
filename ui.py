import bpy
import bmesh
import numpy as np
import os
import sys
import json
from random import random, uniform, randint, randrange, choice
from mathutils import Vector, Matrix

from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import Panel, PropertyGroup, Operator, AddonPreferences
from .properties import dm_lang_data

class DM_PT_First_Panel(Panel):
    bl_idname = "ADDON_MISC_PT_N_PANEL"
    bl_label = dm_lang_data["bl_Label01"]
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
        col.prop(settings, 'locx')
        col = row.column(align=True)
        col.prop(settings, 'locy')
        col = row.column(align=True)
        col.prop(settings, 'locz')
        
        row = layout.row()        
        col = row.column(align=True)
        col.operator("object.translatecol", text=dm_lang_data["objecttranslatecol"])


        row = layout.row()
        col = row.column(align=True)
        col.prop(settings, 'dmthickness')

        row = layout.row()        
        col = row.column(align=True)
        col.operator("object.applyalltransforms", text=dm_lang_data["objectapplyalltransforms"])

        row = layout.row()        
        col = row.column(align=True)
        col.operator("object.startdm", text=dm_lang_data["object.startdm"])

class DM_PT_Second_Panel(Panel):
    bl_idname = "ADDON_MISC_PT_DM_PANEL"
    bl_label = dm_lang_data["bl_Label02"]
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DispMapping"
    def draw(self, context):
        settings = context.scene.dm_misc_settings
        layout = self.layout
        box = layout.box()
        box.label(text=dm_lang_data["p2lbl"], icon='PRESET')

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

def update_lang_type(self, context):
    myaddondirectory = os.path.dirname(os.path.abspath(__file__))
    global dm_lang_data
    if self['lang_type'] == 0:
        myjsonfile = os.path.join(myaddondirectory, "lang", "en.json")
        
    elif self['lang_type'] == 1:
        myjsonfile = os.path.join(myaddondirectory, "lang", "cn.json")
    with open(myjsonfile, 'r') as f:
        dm_lang_data = json.load(f)

    return None
class DM_User_Preferences(AddonPreferences):
    bl_idname = __package__


    grayscale_dir : StringProperty(
        name="Grayscale Bmp Folder", 
        default="", 
        #default=r"E:\documents\Blender\插件\实物模型\灰度图", 
        subtype='DIR_PATH')

    lang_type : EnumProperty(
        items=(
            ('1', "English", ""),
            ('2', "简体中文", ""),),
        name="Language",
        description="Choose default lanaguage",    
        update = update_lang_type   
        )

    def draw(self, context):
        miscsettings = context.scene.dm_misc_settings
        layout = self.layout

        row = layout.row()
        row.prop(self, "grayscale_dir")
        
        row = layout.row()
        row.prop(self, "lang_type")     