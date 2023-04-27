import bpy
import bmesh
import numpy as np
import os
import sys
from random import random, uniform, randint, randrange, choice
from math import radians, atan2, pi
from mathutils import Vector, Matrix
import bgl
import blf
import functools
def getmyangleTZ(v1, v2):
    angle1 = atan2(v1[1],v1[0])
    angle1 = int(angle1 * 180/pi)
    angle2 = atan2(v2[1],v2[0])
    angle2 = round(angle2 * 180/pi,5)
    included_angle = (angle1-angle2)
    if included_angle>=0:
        included_angle = (angle1-angle2)
    elif included_angle<0:
        included_angle =360+ (angle1-angle2)
    
    return included_angle
def get_obj_face_matrix(obj, face, pos=None, normaldirco=-1, idxgap=0, myidir=-1):
    
    verts10gap = face.verts[1].co - face.verts[0].co
    verts21gap = face.verts[2].co - face.verts[1].co
    if abs(verts10gap[2]) == 0 and abs(verts21gap[2]) == 0:
        if abs(verts10gap[0]) > 0:
            vidx = 2 - idxgap
        elif abs(verts10gap[0]) == 0:
            vidx = 1 + idxgap
        
    else:
        #不是水平面了
        if abs(verts10gap[2]) > 0:
            vidx = 2 - idxgap
        elif abs(verts10gap[2]) == 0:
            vidx = 1 + idxgap
        
    
    x_axis = ((obj.matrix_world @ face.verts[vidx].co - obj.matrix_world @ face.verts[vidx - 1].co) * myidir).normalized()
    z_axis = face.normal * normaldirco
    y_axis = z_axis.cross(x_axis)

    if not pos:
        pos = obj.matrix_world @ face.calc_center_bounds()

    mat = Matrix()
    mat[0][0] = x_axis.x
    mat[1][0] = x_axis.y
    mat[2][0] = x_axis.z
    mat[3][0] = 0
    mat[0][1] = y_axis.x
    mat[1][1] = y_axis.y
    mat[2][1] = y_axis.z
    mat[3][1] = 0
    mat[0][2] = z_axis.x
    mat[1][2] = z_axis.y
    mat[2][2] = z_axis.z
    mat[3][2] = 0
    mat[0][3] = pos.x
    mat[1][3] = pos.y
    mat[2][3] = pos.z
    mat[3][3] = 1
    return mat
    
def get_face_width_and_height(face, mysizeoff=1, isreversed=False):
    if not face.is_valid or len(face.verts[:]) < 4:
        return -1, -1
    width = (face.verts[0].co - face.verts[1].co).length
    height = (face.verts[2].co - face.verts[1].co).length
    if isreversed == True:
        return height * mysizeoff, width * mysizeoff
    return width * mysizeoff, height * mysizeoff

def list_random_file(path, idx=-1):
    myfiles = os.listdir(path)
    filelist=[]
    for file in myfiles:
        myfilename = os.path.join(path, file)
        if os.path.isfile(myfilename):
          filelist.append(myfilename)
    filelistlen = len(filelist)
    if idx == -1:
        randomfile = choice(filelist)
    elif idx >= 0 and idx < filelistlen:
        randomfile = filelist[idx]
    else:
        randomfile = filelist[0]
          
    return randomfile
def list_random_dir(path, res, idx=-1):
    mypath = os.path.join(path, res)
    dirlist = []
    for i in os.listdir(mypath):
        temp_dir = os.path.join(mypath, i)
        if os.path.isdir(temp_dir):
          dirlist.append(temp_dir)
    #print(dirlist,path, res,mypath)
    dirlistlen = len(dirlist)
    if idx==-1:
        randomdir = choice(dirlist)
    elif idx >= 0 and idx < dirlistlen:
        randomdir = dirlist[idx]
    else:
        randomdir = dirlist[0]
    return randomdir

def list_dm_random_dir(mypath, idx=-1):
    dirlist = []
    for i in os.listdir(mypath):
        temp_dir = os.path.join(mypath, i)
        if os.path.isdir(temp_dir):
          dirlist.append(i)
    dirlistlen = len(dirlist)
    if idx==-1:
        randomdir = choice(dirlist)
    elif idx >= 0 and idx < dirlistlen:
        randomdir = dirlist[idx]
    else:
        randomdir = dirlist[0]
    return randomdir
def get_dm_root_dir(mygrayscaledir):
    if os.path.isdir(mygrayscaledir):
        mydirsplitlist = mygrayscaledir.split('\\')
        dirlist = []
        for mysplitdir in mydirsplitlist:

            dirlist.append(mysplitdir)
            if mysplitdir == "灰度图":
                break
        separator = "//"
        result = separator.join(dirlist)
        dm_root_dir = os.path.join(result)
        return dm_root_dir
    return ""

def genSubsurfDisplaceGrid(self, context, inner_radius=1, mysubpath='', mysubcategory='', myidx=-1, mystrength=0.03):
    
    mygridloc = (0, 0, 0)
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=15, y_subdivisions=15, size=inner_radius, calc_uvs=True, rotation=(1.57,0,0), location=mygridloc)  
    mygrid = bpy.context.object
    mygrid.name = 'My_DM_Grid'
    
    mod01 = mygrid.modifiers.new(name='Subsurf', type='SUBSURF')
    mod01.subdivision_type = 'SIMPLE'
    mod01.levels = 4
    mod01.render_levels = 4
    
    mod02 = mygrid.modifiers.new(name="Displace", type='DISPLACE')

    addon_name = __name__.split('.')[0] 
    mygrayscaledir = bpy.context.preferences.addons[addon_name].preferences.grayscale_dir
    mypath = get_dm_root_dir(mygrayscaledir)
    if mysubpath == '':
        dirlist = os.listdir(mypath)
        randomdir = choice(dirlist)
    else:
        randomdir= os.path.join(mypath, mysubpath)
    if mysubcategory == '':
        mysubpath = os.path.join(mypath, randomdir)
        subdirlist = os.listdir(mysubpath)
        randomsubdir = choice(subdirlist)
    else:
        randomsubdir = os.path.join(randomdir, mysubcategory)

    myfilepath = os.path.join(mysubpath, randomsubdir)
    myimgpath = list_random_file(myfilepath, idx=myidx)
    
    handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (self, context, myimgpath, -30), 'WINDOW', 'POST_PIXEL')
    bpy.app.timers.register(functools.partial(remove_text, handle), first_interval=1)
    img = bpy.data.images.load(filepath=myimgpath)
    mtex = bpy.data.textures.new("texturemat01", 'IMAGE')
    mtex.image = img
    
    mod02.texture = mtex
    mod02.texture_coords = 'UV'
    mod02.strength = mystrength
    mod02.mid_level = 0
    #myMat.genUniPBRMatbyFaces(mygrid, reslist=['wood'], diridxlist=[-1], randlist=[], displist=[0, 0])
    
    
    mat_name = 'marble'
    path = r'E:\documents\Blender\插件\pbr'
    mydir = list_random_dir(path, mat_name, idx=-1)
    displist=[0.02, 0.02]
    mymappingvectorlist = [[0,0,0],[1,1,1]]
    #mymat = myMat.genMaterial21(matname=mat_name,mymappingtype='POINT',isuffix=-2,itexturecoordinate=2,dirname=mydir,mappingvectorlist=mymappingvectorlist, displist=displist)
    #mygrid.data.materials.append(mymat)
    return mygrid        

def genSubsurfDisplaceGridbyFaceMatrix(self, context, obj, faceidx=0, mysubpath='动物', mysubcategory='马', myidx=-1, mystrength=0.03, myidir=-1):
    mygrid = genSubsurfDisplaceGrid(self, context, inner_radius=1, mysubpath=mysubpath, mysubcategory=mysubcategory, myidx=myidx, mystrength=mystrength)
    mygriddims = mygrid.dimensions
    mygrid.select_set(True)
    #bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    face = bm.faces[faceidx]
    for vert in face.verts:
        #print(vert.co)
        pass
    if (not face.is_valid) or (len(face.verts) != 4):
        bm.free()
        return

    face_width, face_height = get_face_width_and_height(face, isreversed=False)
    depth = 0.175 * min(face_width, face_height)
    facematrix = get_obj_face_matrix(obj, face, face.calc_center_bounds() + face.normal * (depth * 0.042 + mygriddims[2]) * 1, normaldirco=1, idxgap=0, myidir=myidir)
    mygrid.matrix_world = obj.matrix_world @ facematrix
    mygrid.scale = (face_height, face_width, 1)
    #villa:isreversed=True,, idxgap=0, myidir=1
    
    bm.free()
    return mygrid
def genSubsurfDisplaceGridbyFaceTransform(obj, faceidx=0, mysubpath='动物', mysubcategory='马', myidx=-1, mystrength=0.03):
    mygrid = genSubsurfDisplaceGrid(inner_radius=1, mysubpath=mysubpath, mysubcategory=mysubcategory, myidx=myidx, mystrength=mystrength)
    mygriddims = mygrid.dimensions
    mygrid.select_set(True)
    #bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    face = bm.faces[faceidx]

    if not face.is_valid:
        return
    face_width, face_height = get_face_width_and_height(face, mysizeoff=0.99)
    verts10gap = face.verts[1].co - face.verts[0].co
    verts21gap = face.verts[2].co - face.verts[1].co
    
    if abs(verts10gap[2]) > 0:
        vidx = 2
    elif abs(verts10gap[2]) == 0:
        vidx = 1
    v1 = ((face.verts[vidx].co[0] - face.verts[vidx-1].co[0]), (face.verts[vidx].co[1] - face.verts[vidx-1].co[1]))
    v2 = (-1, 0)
    myrotz = getmyangleTZ(v1, v2)
    depth = 0.175 * min(face_width, face_height)
    mylocvector = face.calc_center_bounds() + face.normal * (depth * 0.042 + mygriddims[2]) * 2
    mygrid.location = mylocvector
    mygrid.scale = (face_height, face_width, 1)
    
    mygrid.rotation_euler.z = radians(myrotz)
    mygrid.select_set(True)
    bpy.context.view_layer.objects.active = mygrid
    bpy.ops.object.convert(target='MESH')
    return mygrid


def translateColinCol(colname='Collection', myloc=(0, 0, 0)):
    for obj in bpy.data.collections[colname].objects:
        obj.location.x=obj.location.x + myloc[0]
        obj.location.y=obj.location.y + myloc[1]
        obj.location.z=obj.location.z + myloc[2]
    
    for col in bpy.data.collections[colname].children:
        for obj in col.objects:
            obj.location.x=obj.location.x + myloc[0]
            obj.location.y=obj.location.y + myloc[1]
            obj.location.z=obj.location.z + myloc[2]

def create_glass_mat():
    mat = bpy.data.materials.new('glasswindow')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    mat.node_tree.nodes.remove(bsdf)
    my_material_output = mat.node_tree.nodes['Material Output']
    my_material_output.location = (920.0, 290.0)
    my_transparent_0 = mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
    my_transparent_0.location = (271.0, 112.0)
    my_add_shader = mat.node_tree.nodes.new('ShaderNodeAddShader')
    my_add_shader.location = (545.0, 32.0)
    my_mix_1 = mat.node_tree.nodes.new('ShaderNodeMixShader')
    my_mix_1.location = (690.0, 290.0)
    my_mix_1.inputs['Fac'].default_value = 0.1
    my_glossy_0 = mat.node_tree.nodes.new('ShaderNodeBsdfGlossy')
    my_glossy_0.location = (271.0, 4.0)
    my_glossy_0.inputs['Roughness'].default_value = 0.0
    my_glass_bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfGlass')
    my_glass_bsdf.location = (304.0, 304.0)
    my_glass_bsdf.inputs['Roughness'].default_value = 0.0
    my_glass_bsdf.inputs['IOR'].default_value = 1.45
    my_math = mat.node_tree.nodes.new('ShaderNodeMath')
    my_math.location = (473.0, 483.0)
    my_math.inputs['Value'].default_value = 0.5
    my_math.inputs['Value'].default_value = 0.5
    my_math.inputs['Value'].default_value = 0.0
    my_light_0 = mat.node_tree.nodes.new('ShaderNodeLightPath')
    my_light_0.location = (23.0, 645.0)
    mat.node_tree.links.new(my_mix_1.outputs['Shader'], my_material_output.inputs['Surface'])
    mat.node_tree.links.new(my_glass_bsdf.outputs['BSDF'], my_mix_1.inputs[1])
    mat.node_tree.links.new(my_transparent_0.outputs['BSDF'], my_add_shader.inputs[0])
    mat.node_tree.links.new(my_add_shader.outputs['Shader'], my_mix_1.inputs[2])
    mat.node_tree.links.new(my_math.outputs['Value'], my_mix_1.inputs['Fac'])
    mat.node_tree.links.new(my_light_0.outputs['Is Diffuse Ray'], my_math.inputs[0])
    mat.node_tree.links.new(my_light_0.outputs['Transparent Depth'], my_math.inputs[1])
    mat.node_tree.links.new(my_glossy_0.outputs['BSDF'], my_add_shader.inputs[1])
    return mat

def draw_callback_px(self, context, msg, hgap):
    font_id = 0
    blf.size(font_id, 28, 56)
    color = (0.8, 0.6, 0.1, 1)
    blf.color(font_id, color[0], color[1], color[2], color[3])
    
    blf.position(font_id, 100, 120 + hgap, 0) 
    blf.draw(font_id, msg)  

 
def remove_text(handle):
    bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
    
