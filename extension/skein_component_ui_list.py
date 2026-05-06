import bpy

def remove_operator_id_for_data_block(data_block):
    if isinstance(data_block, bpy.types.Object):
        return "object.remove_component"
    if isinstance(data_block, bpy.types.Mesh):
        return "mesh.remove_component"
    if isinstance(data_block, bpy.types.Material):
        return "material.remove_component"
    if isinstance(data_block, bpy.types.Scene):
        return "scene.remove_component"
    if isinstance(data_block, bpy.types.Light):
        return "light.remove_component"
    if isinstance(data_block, bpy.types.Collection):
        return "collection.remove_component"
    if isinstance(data_block, bpy.types.Bone):
        return "bone.remove_component"
    return None


class SKEIN_UL_component_list(bpy.types.UIList):
    bl_idname = "SKEIN_UL_component_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if item is None:
            return

        display_text = getattr(item, "selected_type_path", "") or item.name

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row_split = layout.split(factor=0.82, align=True)
            row_split.label(text=display_text, icon='BOIDS')
            operator_row = row_split.row(align=True)
            operator_row.alignment = 'RIGHT'
            operator_identifier = remove_operator_id_for_data_block(data)
            if operator_identifier is not None:
                delete_operator = operator_row.operator(
                    operator_identifier,
                    icon='TRASH',
                    text="",
                    emboss=False,
                )
                delete_operator.component_index = index
