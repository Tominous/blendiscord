'''
Discord Rich Presence for Blender 0.2
By @AlexApps#9295
Tip of the day - consult Blender's built-in templates if confused.
'''
bl_info = {
    "name": "Discord Rich Presence",
    "description": "Brings Discord Rich Presence support to Blender",
    "author": "@AlexApps#9295",
    "version": (0, 3),
    "blender": (2, 80, 0),
    "location": "Preferences > Addons",
    "warning": "Beta - Still in development!",
    "wiki_url": "https://github.com/AlexApps99/blender-rich-presence/README.md",
    "tracker_url": "https://github.com/AlexApps99/blender-rich-presence/issues",
    "support": "COMMUNITY",
    "category": "System"
}
# Imports
from time import time
from os import getpid
from threading import Timer # Find another way to thread
from pypresence import Presence # Discord Rich Presence - todo error handle when discord is closed
import bpy # Blender imports
from bpy.types import AddonPreferences, Operator
from bpy.props import BoolProperty, IntProperty, EnumProperty, StringProperty

# UI Options
artassets = [("blender_logo", "Blender Logo", "A flat logo for Blender"),
             ("bricks", "Lego", "A pile of Lego Bricks"),
             ("flamingtext", "Lit Text", "It says 'Lit Boi'"),
             ("ring", "Ring", "A blue ring"),
             ("rubiks", "Rubik's Cube", "A Rubik's Cube"),
             ("triforce", "Triforce", "The Triforce"),
             ("vaporwave", "Vaporwave", "Aesthetic Suzanne")]
texts = [("filename", "Filename", "e.g untitled.blend"),
         ("version", "Blender Version", "e.g Blender 2.80.0"),
         ("renderer", "Renderer", "e.g Cycles"),
         ("space", "Current Space", "e.g Movie Clip Editor"),
         ("mode", "3D View Mode", "e.g Editing Mesh"),
         ("objects", "Objects", "e.g 10/102 Objects selected"),
         ("custom", "Custom String", "e.g Happy Blending!")]
# Blender status to formatted text
modes = {'EDIT_MESH': 'Editing Mesh',
         'EDIT_CURVE': 'Editing Curve',
         'EDIT_SURFACE': 'Editing Surface',
         'EDIT_TEXT': 'Editing Text',
         'EDIT_ARMATURE': 'Editing Armature',
         'EDIT_METABALL': 'Editing Metaball',
         'EDIT_LATTICE': 'Editing Lattice',
         'POSE': 'Posing',
         'SCULPT': 'Sculpting',
         'PAINT_WEIGHT': 'Weight Painting',
         'PAINT_VERTEX': 'Vertex Painting',
         'PAINT_TEXTURE': 'Texture Painting',
         'PARTICLE': 'Editing Particles',
         'OBJECT': 'Viewing Objects',
         'PAINT_GPENCIL': 'Painting Grease Pencil',
         'EDIT_GPENCIL': 'Editing Grease Pencil',
         'SCULPT_GPENCIL': 'Sculpting Grease Pencil',
         'WEIGHT_GPENCIL': 'Weighting Grease Pencil'}
renderers = {'BLENDER_EEVEE': 'Eevee',
             'BLENDER_WORKBENCH': 'Workbench',
             'CYCLES': 'Cycles'}
spaces = {'EMPTY': 'None',
          'VIEW_3D': '3D Viewport',
          'IMAGE_EDITOR': 'Image/UV Editor',
          'NODE_EDITOR': 'Node Editor',
          'SEQUENCE_EDITOR': 'Video Sequencer',
          'CLIP_EDITOR': 'Movie Clip Editor',
          'DOPESHEET_EDITOR': 'Dope Sheet',
          'GRAPH_EDITOR': 'Graph Editor',
          'NLA_EDITOR': 'Nonlinear Animation',
          'TEXT_EDITOR': 'Text Editor',
          'CONSOLE': 'Python Console',
          'INFO': 'Info',
          'TOPBAR': 'Top Bar',
          'STATUSBAR': 'Status Bar',
          'OUTLINER': 'Outliner',
          'PROPERTIES': 'Properties',
          'FILE_BROWSER': 'File Browser',
          'PREFERENCES': 'Preferences'}

class DiscordAddonPreferences(AddonPreferences):
    bl_idname = __name__

    enablerp = BoolProperty(
        name="Enable Rich Presence (unused)",
        description="Enables connection to Discord for Rich Presence",
        default=False
    )
    interval = IntProperty(
        name="Update Interval (s) (unused)",
        description="Interval between Rich Presence Updates (in seconds)",
        default=15,
        min=1,
        max=300,
        subtype="TIME"
    )
    details = EnumProperty(
        items=texts,
        name="Details",
        description="Choose which status you want",
        default="mode"
    )
    state = EnumProperty(
        items=texts,
        name="State",
        description="Choose which status you want",
        default="filename"
    )
    largeimage = EnumProperty(
        items=artassets,
        name="Large Image",
        description="Choose which large image you want",
        default="bricks"
    )
    largetext = EnumProperty(
        items=texts,
        name="Large Image Text",
        description="Choose which status you want",
        default="renderer"
    )
    smallimage = EnumProperty(
        items=artassets,
        name="Small Image",
        description="Choose which small image you want",
        default="blender_logo"
    )
    smalltext = EnumProperty(
        items=texts,
        name="Small Image Text",
        description="Choose which status you want",
        default="version"
    )
    customtext = StringProperty(
        name="Custom text",
        description="Enter some custom text",
        default="Happy Blending!",
        maxlen=32
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hover over options for more details")
        layout.prop(self, "enablerp")
        layout.prop(self, "interval")
        layout.prop(self, "details")
        layout.prop(self, "state")
        layout.prop(self, "largeimage")
        layout.prop(self, "largetext")
        layout.prop(self, "smallimage")
        layout.prop(self, "smalltext")
        layout.prop(self, "customtext")

start_time = int(time())
RPC = Presence('434079082339106827')
RPC.connect()
class updateRichPresence(Operator):
    """My Object Moving Script"""
    bl_idname = "wm.updaterp"
    bl_label = "Update Discord Rich Presence"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        prefs = bpy.context.preferences.addons[__name__].preferences
        #Timer(prefs.interval, updatePresence).start()
        if prefs.enablerp:
            outputs=["untitled.blend" if bpy.path.basename(bpy.context.blend_data.filepath) == "" else bpy.path.basename(bpy.context.blend_data.filepath),
                     'Blender {}.{}.{}'.format(bpy.app.version[0], bpy.app.version[1], bpy.app.version[2]),
                     renderers[bpy.context.engine] if bpy.context.engine in renderers else "Unknown Renderer ({})".format(bpy.context.engine),
                     spaces[bpy.context.space_data.type],
                     modes[bpy.context.mode],
                     len(bpy.context.selected_objects)+"/"+len(bpy.context.scene.objects)+" objects selected",
                     prefs.customtext]
            RPC.update(pid=getpid(),
                       details=outputs[prefs.details],
                       state=outputs[prefs.state],
                       start=start_time,
                       large_image=prefs.largeimage, large_text=outputs[prefs.largetext],
                       small_image=prefs.smallimage, small_text=outputs[prefs.smalltext])
        else:
            RPC.clear(pid=getpid())
        return {'FINISHED'}

def register():
    bpy.utils.register_class(DiscordAddonPreferences)
    bpy.utils.register_class(updateRichPresence)

def unregister():
    RPC.clear(pid=getpid())
    RPC.close()
    bpy.utils.unregister_class(updateRichPresence)
    bpy.utils.unregister_class(DiscordAddonPreferences)

if __name__ == "__main__":
    register()

