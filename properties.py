import bpy
import os
import json
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import Panel, PropertyGroup, Operator
import functools
from .utils import myutils
global dm_lang_data
dm_lang_data = {}
language = 'en'

def my_dm_img_files_callback(self, context):
    items = []
    my_dmimgs_path = self.dmimgsdir
    if not os.path.isdir(my_dmimgs_path):
        return [("0", "None", "")]
    myunsortedfiles = os.listdir(my_dmimgs_path)
    mydmimgfiles = sorted(myunsortedfiles, key=lambda x: os.path.getmtime(os.path.join(my_dmimgs_path, x)), reverse=False)
    i = 0
    for file in mydmimgfiles:
        myfilename = os.path.join(my_dmimgs_path, file)
        if os.path.isfile(myfilename) and myfilename.lower()[-4:] in ['.bmp', '.png', '.jpg']:
            if i > 30:
                break
            #filename = file.split('.bmp')[0]
            filename = file[:-4]
            cnfilename = bytes(filename, encoding='UTF-8')
            items.append((str(i), str(i), ""))
            i += 1
    if len(items) == 0:
        return [("0", "None", "")]
    return items
    
def update_dm_img_files(self, context):
    items = []
    my_dmimgs_path = self.dmimgsdir
    myunsortedfiles = os.listdir(my_dmimgs_path)
    mydmimgfiles = sorted(myunsortedfiles, key=lambda x: os.path.getmtime(os.path.join(my_dmimgs_path, x)), reverse=False)
    i = 0
    for file in mydmimgfiles:
        myfilename = os.path.join(my_dmimgs_path, file)
        if os.path.isfile(myfilename) and myfilename.lower()[-4:] in ['.bmp', '.png', '.jpg']:
            if i > 30:
                break
            #filename = file.split('.bmp')[0]
            filename = file[:-4]
            items.append(filename)
            i += 1
            
    imgname = os.path.join(my_dmimgs_path, items[int(self.dmimgenumfiles)])
    handle = bpy.types.SpaceView3D.draw_handler_add(myutils.draw_callback_px, (self, context, imgname, 20), 'WINDOW', 'POST_PIXEL')
    bpy.app.timers.register(functools.partial(myutils.remove_text, handle), first_interval=1)
    

def my_dm_img_dirs_callback(self, context):
    #this only applies to enum property

    addon_name = __name__.split('.')[0] 
    mygrayscaledir = context.preferences.addons[addon_name].preferences.grayscale_dir
    items = []
    
    mydmimgdirs = os.listdir(mygrayscaledir)
    i = 0
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

myaddondirectory = os.path.dirname(os.path.abspath(__file__))

if language == 'en':
    myjsonfile = os.path.join(myaddondirectory, "lang", "en.json")
    
elif language == 'cn':
    myjsonfile = os.path.join(myaddondirectory, "lang", "cn.json")
with open(myjsonfile, 'r') as f:
    dm_lang_data = json.load(f)

class DMMISCSettings(PropertyGroup):
    # FOR MISC SETTINGS
    
    collectionName : StringProperty(
        name = dm_lang_data["collectionName"],
        default = ""
    )
    boolName : BoolProperty(
        name = "Boolean",
        default = True
    )
    locx : FloatProperty(
        name = "X:",
        description = "translate x",
        min = -10000,
        max = 10000,
        default = 0.0,
        )
    locy : FloatProperty(
        name = "Y:",
        description = "translate y",
        min = -10000,
        max = 10000,
        default = 0.0,
        )
    locz : FloatProperty(
        name = "Z:",
        description = "translate z",
        min = -10000,
        max = 10000,
        default = 0.0,
        )
    
    dmthickness : FloatProperty(
        name = dm_lang_data["dmthickness"],
        description = "Thickness",
        min = 0,
        max = 1000,
        default = 0.03,
        )



    isbyrandomdir : BoolProperty(
        name = dm_lang_data["isbyrandomfile"],
        default = True
    )

    isbyrandomfile : BoolProperty(
        name = dm_lang_data["isbyrandomfile"],
        default = True
    )

    isclockwise : BoolProperty(
        name = dm_lang_data["isclockwise"],
        default = False
    )


    dmimgsdir: bpy.props.StringProperty(
        name = dm_lang_data["dmimgsdir"],
        subtype = 'DIR_PATH',
        description = "Displacement mapping images Directory",
        default = '',
        get = get_dm_imgs_dir,
        set = set_dm_imgs_dir
        
    )

    dmimgenumfiles: EnumProperty(
        items=my_dm_img_files_callback,
        name=dm_lang_data["dmimgenumfiles"],
        description="Displacement mapping images",
        update=update_dm_img_files,
        )

    