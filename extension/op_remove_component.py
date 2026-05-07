import bpy

from .op_insert_component import resolve_skein_component_target


class RemoveComponentIndexMixin:
    component_index: bpy.props.IntProperty(
        name="Component Index",
        description="Index in skein_two to remove; -1 removes the active list selection",
        default=-1,
        min=-1,
    )


def remove_component_at_index(component_owner, removed_index):
    collection = component_owner.skein_two
    if removed_index < 0 or removed_index >= len(collection):
        return
    active_before = component_owner.active_component_index
    collection.remove(removed_index)
    remaining_count = len(collection)
    if remaining_count == 0 or removed_index == active_before:
        component_owner.active_component_index = 0
    elif active_before > removed_index:
        component_owner.active_component_index = active_before - 1


class SkeinRemoveComponent(bpy.types.Operator, RemoveComponentIndexMixin):
    """Remove a Skein component entry from the datablock resolved from context."""
    bl_idname = "wm.skein_remove_component"
    bl_label = "Remove Skein Component Data"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return resolve_skein_component_target(context) is not None

    def execute(self, context):
        target = resolve_skein_component_target(context)
        if target is None:
            return {'CANCELLED'}
        remove_component_at_index(target, self.component_index)
        return {'FINISHED'}

classes = (SkeinRemoveComponent,)

register, unregister = bpy.utils.register_classes_factory(classes)
