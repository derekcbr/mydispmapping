import bpy
import os
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import Panel, PropertyGroup, Operator
import functools
from .utils import myutils
def my_dm_img_files_callback(self, context):
    items = []
    my_dmimgs_path = self.dmimgsdir
    mydmimgfiles = os.listdir(my_dmimgs_path)
    i = 1
    for file in mydmimgfiles:
        myfilename = os.path.join(my_dmimgs_path, file)
        if os.path.isfile(myfilename) and myfilename.endswith('.bmp'):
            filename = file.split('.bmp')[0]
            #cnfilename = filename.encode('utf-8')
            #cnfilename = filename.encode('utf-8').decode('utf-8')
            cnfilename = bytes(filename, encoding='UTF-8')
            #items.append((str(i), cnfilename, ""))
            #items.append((str(i), 'u' + cnfilename.decode('utf-8'), ""))
            items.append((str(i), str(i), ""))
            i += 1
    
    return items
    
def update_dm_img_files(self, context):
    items = []
    my_dmimgs_path = self.dmimgsdir
    mydmimgfiles = os.listdir(my_dmimgs_path)
    for file in mydmimgfiles:
        myfilename = os.path.join(my_dmimgs_path, file)
        if os.path.isfile(myfilename) and myfilename.endswith('.bmp'):
            filename = file.split('.bmp')[0]
            items.append(filename)
            
    imgname = items[int(self.dmimgenumfiles) + 1]
    handle = bpy.types.SpaceView3D.draw_handler_add(myutils.draw_callback_px, (self, context, imgname, 20), 'WINDOW', 'POST_PIXEL')
    bpy.app.timers.register(functools.partial(myutils.remove_text, handle), first_interval=1)
    pass

def my_dm_img_dirs_callback(self, context):
    #this only applies to enum property

    addon_name = __name__.split('.')[0] 
    mygrayscaledir = context.preferences.addons[addon_name].preferences.grayscale_dir
    items = []
    
    mydmimgdirs = os.listdir(mygrayscaledir)
    i = 1
    for mydir in mydmimgdirs:
        mydirname = os.path.join(mygrayscaledir, mydir)
        if os.path.isdir(mydirname):
            cndirname = mydir.encode('utf-8').decode('utf-8')
            items.append((str(i), cndirname, ""))
            i += 1
    return items

def my_dm_img_dirs_str_callback(context):
    #this only applies to enum property

    addon_name = __name__.split('.')[0] 
    mygrayscaledir = context.preferences.addons[addon_name].preferences.grayscale_dir
    items = []
    
    mydmimgdirs = os.listdir(mygrayscaledir)
    i = 1
    for mydir in mydmimgdirs:
        mydirname = os.path.join(mygrayscaledir, mydir)
        if os.path.isdir(mydirname):
            cndirname = mydir.encode('utf-8').decode('utf-8')
            mycndirname = os.path.join(mygrayscaledir, cndirname)
            items.append(mycndirname)
            i += 1
    return items


def update_dm_img_dirs(self, context):

   
    pass

def get_dm_imgs_dir(self):
    addon_name = __name__.split('.')[0] 
    mygrayscaledir = bpy.context.preferences.addons[addon_name].preferences.grayscale_dir
    return self.get('dm_imgs_dir', mygrayscaledir)

def set_dm_imgs_dir(self, value):
    self['dm_imgs_dir'] = value
    return None


class DMMISCSettings(PropertyGroup):
    # FOR MISC SETTINGS
    
    collectionName : StringProperty(
        name = "Col Name",
        default = ""
    )
    boolName : BoolProperty(
        name = "Boolean",
        default = True
    )
    locx : FloatProperty(
        name = "fx",
        description = "translate x",
        min = -100,
        max = 100,
        default = 0.0,
        )
    locy : FloatProperty(
        name = "fy",
        description = "translate y",
        min = -100,
        max = 100,
        default = 0.0,
        )
    locz : FloatProperty(
        name = "fz",
        description = "translate z",
        min = -100,
        max = 100,
        default = 0.0,
        )
    
    dmthickness : FloatProperty(
        name = "置换贴图厚度",
        description = "Thickness",
        min = 0,
        max = 1000,
        default = 0.03,
        )



    isbyrandomdir : BoolProperty(
        name = "随机目录",
        default = True
    )

    isbyrandomfile : BoolProperty(
        name = "随机文件",
        default = True
    )

    isclockwise : BoolProperty(
        name = "顺时针方向",
        default = False
    )


    dmimgsdir: bpy.props.StringProperty(
        name = "贴图目录",
        subtype = 'DIR_PATH',
        description = "Displacement mapping images Directory",
        default = '',
        get = get_dm_imgs_dir,
        set = set_dm_imgs_dir
        
    )

    dmimgenumfiles: EnumProperty(
        items=my_dm_img_files_callback,
        name="贴图列表",
        description="Displacement mapping images",
        update=update_dm_img_files,
        )

    