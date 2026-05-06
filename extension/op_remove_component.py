import bpy


class RemoveComponentIndexMixin:
    component_index: bpy.props.IntProperty(
        name="Component Index",
        description="Index in skein_two to remove; -1 removes the active list selection",
        default=-1,
        min=-1,
    )


def remove_component_at_index(obj, removed_index):
    collection = obj.skein_two
    if removed_index < 0 or removed_index >= len(collection):
        return
    active_before = obj.active_component_index
    collection.remove(removed_index)
    remaining_count = len(collection)
    if remaining_count == 0 or removed_index == active_before:
        obj.active_component_index = 0
    elif active_before > removed_index:
        obj.active_component_index = active_before - 1


class RemoveComponentOnObject(bpy.types.Operator, RemoveComponentIndexMixin):
    """Remove a component on the selected object"""
    bl_idname = "object.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Object)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return hasattr(context, "object") and context.object is not None

    def execute(self, context):
        remove_component_at_index(context.object, self.component_index)
        return {'FINISHED'}

class RemoveComponentOnMesh(bpy.types.Operator, RemoveComponentIndexMixin):
    """Remove a component on the selected mesh"""
    bl_idname = "mesh.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Mesh)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return hasattr(context, "mesh") and context.mesh is not None

    def execute(self, context):
        remove_component_at_index(context.mesh, self.component_index)
        return {'FINISHED'}

class RemoveComponentOnMaterial(bpy.types.Operator, RemoveComponentIndexMixin):
    """Remove a component on the selected material"""
    bl_idname = "material.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Material)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return hasattr(context, "material") and context.material is not None

    def execute(self, context):
        remove_component_at_index(context.material, self.component_index)
        return {'FINISHED'}

class RemoveComponentOnScene(bpy.types.Operator, RemoveComponentIndexMixin):
    """Remove a component on the selected scene"""
    bl_idname = "scene.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Scene)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return hasattr(context, "scene") and context.scene is not None

    def execute(self, context):
        remove_component_at_index(context.scene, self.component_index)
        return {'FINISHED'}

class RemoveComponentOnLight(bpy.types.Operator, RemoveComponentIndexMixin):
    """Remove a component on the selected light"""
    bl_idname = "light.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Light)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return hasattr(context, "light") and context.light is not None

    def execute(self, context):
        remove_component_at_index(context.light, self.component_index)
        return {'FINISHED'}

class RemoveComponentOnCollection(bpy.types.Operator, RemoveComponentIndexMixin):
    """Remove a component on the selected collection"""
    bl_idname = "collection.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Collection)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return hasattr(context, "collection") and context.collection is not None

    def execute(self, context):
        remove_component_at_index(context.collection, self.component_index)
        return {'FINISHED'}

class RemoveComponentOnBone(bpy.types.Operator, RemoveComponentIndexMixin):
    """Remove a component on the selected bone"""
    bl_idname = "bone.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Bone)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return hasattr(context, "bone") and context.bone is not None

    def execute(self, context):
        remove_component_at_index(context.bone, self.component_index)
        return {'FINISHED'}

classes = (
    RemoveComponentOnObject,
    RemoveComponentOnMesh,
    RemoveComponentOnMaterial,
    RemoveComponentOnScene,
    RemoveComponentOnLight,
    RemoveComponentOnCollection,
    RemoveComponentOnBone,
)

register, unregister = bpy.utils.register_classes_factory(classes)