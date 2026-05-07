import bpy

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
            delete_operator = operator_row.operator(
                "wm.skein_remove_component",
                icon='TRASH',
                text="",
                emboss=False,
            )
            delete_operator.component_index = index
