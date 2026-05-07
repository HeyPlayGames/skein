import json
import bpy

from .object_to_form import object_to_form
from .property_groups import hash_over_64


def resolve_insert_component_target_properties(context):
    """Resolve datablock from the active Properties editor tab (object vs mesh vs …)."""
    space = getattr(context, "space_data", None)
    if space is None or space.type != "PROPERTIES":
        return None
    tab = getattr(space, "context", None)
    if tab == "OBJECT":
        return getattr(context, "object", None)
    if tab == "DATA":
        if getattr(context, "mesh", None):
            return context.mesh
        if getattr(context, "light", None):
            return context.light
        return None
    if tab == "MATERIAL":
        return getattr(context, "material", None)
    if tab == "SCENE":
        return getattr(context, "scene", None)
    if tab == "COLLECTION":
        return getattr(context, "collection", None)
    if tab == "BONE":
        return getattr(context, "bone", None)
    return None


def resolve_skein_component_target(context):
    """Resolve which datablock owns Skein components for insert/remove/panel poll.

    Uses the Properties tab when the active space is the Properties editor so mesh
    vs object stay distinct. Otherwise falls back to a single supported datablock
    (scripting, tests, other editors); order prefers lamp/light over mesh data
    when multiple exist, and object over mesh so object.insert-style calls match
    prior behavior.
    """
    target = resolve_insert_component_target_properties(context)
    if target is not None:
        return target
    if getattr(context, "bone", None):
        return context.bone
    if getattr(context, "collection", None):
        return context.collection
    if getattr(context, "scene", None):
        return context.scene
    if getattr(context, "material", None):
        return context.material
    if getattr(context, "light", None):
        return context.light
    if getattr(context, "object", None):
        return context.object
    if getattr(context, "mesh", None):
        return context.mesh
    return None

def on_selected_component_changed(_self, context):
    selected_component = context.window_manager.selected_component
    if not selected_component:
        return

    target = resolve_insert_component_target_properties(context)
    if target is None:
        return

    global_skein = context.window_manager.skein
    if not global_skein.registry:
        return

    registry = json.loads(global_skein.registry)
    if not list(registry) or selected_component not in registry or not registry[selected_component]:
        return

    insert_component_data(context, target)


class SkeinInsertComponent(bpy.types.Operator):
    """Insert a Skein component on the datablock resolved from context."""
    bl_idname = "wm.skein_insert_component"
    bl_label = "Insert Skein Component Data"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return resolve_skein_component_target(context) is not None

    def execute(self, context):
        target = resolve_skein_component_target(context)
        if target is None:
            return {'CANCELLED'}
        insert_component_data(context, target)
        return {'FINISHED'}

def insert_component_data(context, obj):
    """
    Inserting data is super generic, the only difference is where we're inserting it.
    This is basically the same concept as Custom Properties which don't care what object they're on.
    """
    debug = False
    presets = False
    if __package__ in bpy.context.preferences.addons:
        preferences = bpy.context.preferences.addons[__package__].preferences
        debug = preferences.debug
        presets = preferences.presets

    if debug:
        print("\ninsert_component_data:")
    
    global_skein = context.window_manager.skein
    selected_component = context.window_manager.selected_component

    if global_skein.registry:
        registry = json.loads(global_skein.registry)
        if list(registry) and registry[selected_component]:
            data = registry[selected_component]
            if debug:
                print(data)

            new_component = obj.skein_two.add()
            new_component.name = data["shortPath"]
            new_component.selected_type_path = selected_component

            # Blender will not initialize PointerPropertys if we don't
            # access them, leading to missing data issues when we render
            # the UI. This is why we touch all PointerProperty fields
            # to make sure they're initialized.
            touch_all_fields(new_component, hash_over_64(new_component.selected_type_path))

            # If we inserted a new component, update the 
            # active_component_index to show the right editor
            # for the newly inserted component
            obj.active_component_index = len(obj.skein_two) - 1

            if presets:
                try:
                    if "skein-presets.json" in bpy.data.texts:
                        text = bpy.data.texts["skein-presets.json"].as_string()
                        embedded_presets = json.loads(text)
                        object_to_form(
                            new_component,
                            hash_over_64(new_component.selected_type_path),
                            embedded_presets[selected_component]["default"]
                        )
                except Exception as e:
                    print(e)
                    pass
        else:
            print("no data in registry")
    else:
        print("no global registry set")

def touch_all_fields(context, key):
    try:
        obj = getattr(context, key)
        annotations = getattr(obj, "__annotations__")
        for key, value in annotations.items():
            if "PointerProperty" == value.function.__name__:
                touch_all_fields(obj, key)
    except:
        pass

classes = (SkeinInsertComponent,)

register, unregister = bpy.utils.register_classes_factory(classes)