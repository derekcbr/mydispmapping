import bpy
import bmesh
import numpy as np
import time
import os
import sys
from random import random, uniform, randint, randrange, choice
from mathutils import Vector, Matrix
import functools
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import Panel, PropertyGroup, Operator
from bpy_extras import view3d_utils
from ..utils import myutils, mymat
        
class Translate_OT_Col_to_New_Location(Operator):
    bl_label = "TranslateColNewLoc"
    bl_idname = "object.translatecol"
    bl_description = "TranslateColNewLoc"
    
    @classmethod
    def poll(cls, context):
        settings = bpy.context.scene.dm_misc_settings
        
        mycolname = settings.collectionName
        myselectedcol = bpy.context.view_layer.active_layer_collection
        return len(mycolname) > 0 or len(myselectedcol.name) > 0
    def execute(self, context):

        
        miscsettings = bpy.context.scene.dm_misc_settings
        myfx = miscsettings.locx
        myfy = miscsettings.locy
        myfz = miscsettings.locz
        mycolname = miscsettings.collectionName
        if len(mycolname) > 0:
            myutils.translateColinCol(colname=mycolname, myloc=(myfx, myfy, myfz))
        elif len(mycolname) == 0:
        
            myselectedcol = bpy.context.view_layer.active_layer_collection
            if len(myselectedcol.name) > 0:
                myutils.translateColinCol(colname=myselectedcol.name, myloc=(myfx, myfy, myfz))

        return {'FINISHED'}
        
class Add_OT_Non_PBR_Mat(Operator):
    bl_label = "AddNonPBRMat"
    bl_idname = "object.addnonpbrmat"
    bl_description = "AddNonPBRMat"
    
    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == "MESH"
    def execute(self, context):
        myobject = bpy.context.object
        mymat = myMat.create_glass_mat()
        myobject.data.materials.clear()
        myobject.data.materials.append(mymat)
        return {'FINISHED'}

class Add_OT_DM_to_Mesh_Object(Operator):
    bl_idname = "object.startdm"
    bl_description = "Modal Operator"
    bl_label = "start DM"
    @classmethod
    def poll(cls, context):
        addon_name = __name__.split('.')[0] 
        mygrayscaledir = context.preferences.addons[addon_name].preferences.grayscale_dir
        obj = context.object
        return obj and obj.type == "MESH" and os.path.isdir(mygrayscaledir)
    t = 0
    click = False

    def modal(self, context, event):

        addon_name = __name__.split('.')[0] 
        mygrayscaledir = context.preferences.addons[addon_name].preferences.grayscale_dir
        miscsettings = context.scene.dm_misc_settings
        isbyrandomfile = miscsettings.isbyrandomfile
        isclockwise = miscsettings.isclockwise
        mydmthickness = miscsettings.dmthickness
        mydmimgsdir = miscsettings.dmimgsdir
        #mydirsplitlist = mygrayscaledir.split('\\')
        if mydmimgsdir[-1] == "\\":
            mydirsplitlist = mydmimgsdir[:-1].split('\\')
        else:
            mydirsplitlist = mydmimgsdir.split('\\')
        if mydirsplitlist[-3] == '灰度图':
            mysubcat01 = mydirsplitlist[-2]
            mysubcat02 = mydirsplitlist[-1]
        elif mydirsplitlist[-2] == '灰度图':
            mysubcat01 = mydirsplitlist[-1]
            mysubcat02 = myutils.list_dm_random_dir(mydmimgsdir, idx=-1)
        
        elif mydirsplitlist[-1] == '灰度图':
            
            mysubcat01 = myutils.list_dm_random_dir(mydmimgsdir, idx=-1)
            mysubcat02path = os.path.join(mydmimgsdir, mysubcat01)
            mysubcat02 = myutils.list_dm_random_dir(mysubcat02path, idx=-1)
        
        else:
            return {'CANCELLED'}
        
        mydmimgfileidx = miscsettings.dmimgenumfiles
        #if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            if context.area.type == 'VIEW_3D':
                temp = time.time()
                if (temp - self.t) < 0.3:
                    
                    self.mouse_pos = event.mouse_region_x, event.mouse_region_y
                    
                    region = bpy.context.region
                    region3D = bpy.context.space_data.region_3d

                    self.view_vector = view3d_utils.region_2d_to_vector_3d(region, region3D, self.mouse_pos)
                    self.view_point = view3d_utils.region_2d_to_origin_3d(region, region3D, self.mouse_pos)
                    self.world_loc = view3d_utils.region_2d_to_location_3d(region, region3D, self.mouse_pos, self.view_vector)
                    
                    self.object = bpy.context.object
                    obj = bpy.context.object
                    if obj.type == 'MESH':
                        self.loc_on_plane = None
                        world_mat_inv = obj.matrix_world.inverted()
                        rc_origin = world_mat_inv @ self.view_point
                        rc_destination = world_mat_inv @ self.world_loc
                        rc_direction = (rc_destination - rc_origin).normalized()
                        
                        hit, loc, norm, index = obj.ray_cast( origin = rc_origin, direction = rc_direction )
                        
                        self.loc_on_plane = loc
                        if hit:
                            catmsg = mysubcat01 + "  " + mysubcat02
                            handle = bpy.types.SpaceView3D.draw_handler_add(myutils.draw_callback_px, (self, context, catmsg, 0), 'WINDOW', 'POST_PIXEL')
                            bpy.app.timers.register(functools.partial(myutils.remove_text, handle), first_interval=1)
                            self.world_loc = obj.matrix_world @ loc
                            self.facenormal = norm
                            self.faceidx = index
                            if isbyrandomfile == True:
                                dmimgidx = -1
                            else:
                                if mydmimgfileidx != '':
                                    dmimgidx = int(mydmimgfileidx)
                                else:  
                                    dmimgidx = -1
                            if isclockwise == True:
                                myidir = 1
                            else:
                                myidir = -1
                            try:
                                myutils.genSubsurfDisplaceGridbyFaceMatrix(self, context, obj, faceidx=self.faceidx, mysubpath=mysubcat01, mysubcategory=mysubcat02, myidx=dmimgidx, mystrength=mydmthickness, myidir=myidir)
                                #myutils.genSubsurfDisplaceGridbyFaceTransform(obj, faceidx=self.faceidx, mysubpath=mysubcat01, mysubcategory=mysubcat02, myidx=-1, mystrength=mydmthickness)
                            except Exception as e:
                                print("Indexerror:", e)
                self.t = temp    
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}

        
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

    def execute(self, context):
        if context.area.type != 'VIEW_3D':
            print("Must use in a 3d region")
            return {'CANCELLED'}
        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        
