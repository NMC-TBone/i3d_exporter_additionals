import bpy

from .i3d_exporter_type import check_i3d_exporter_type


class I3DEA_PT_panel(bpy.types.Panel):
    """ GUI Panel for the I3D Exporter Additionals visible in the 3D Viewport """
    bl_idname = "I3DEA_PT_panel"
    bl_label = "I3D Exporter Additionals"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GIANTS I3D Exporter"

    def draw(self, context):
        layout = self.layout
        giants_i3d, stjerne_i3d, dcc, I3DRemoveAttributes = check_i3d_exporter_type()
        if giants_i3d and stjerne_i3d:
            # "Exporter selection" box
            layout.label(text="Both Giants & Stjerne I3D exporter is enabled", icon='ERROR')
            layout.label(text="Recommend to disable one of them as it can cause some issues")
            # layout.label(text="Do you want do disable one of them?")
            # layout.operator("i3dea.addon_disable_giants", text="Giants")
            # layout.operator("i3dea.addon_disable_stjerne", text="Stjerne")
        # "Mesh-Tools" box
        box = layout.box()
        row = box.row()
        # extend button for
        row.prop(context.scene.i3dea, "UI_meshTools", text="Mesh-Tools", icon='TRIA_DOWN' if context.scene.i3dea.UI_meshTools else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_meshTools:
            row = box.row()
            row.operator("i3dea.remove_doubles", text="Clean Meshes")
            row.operator("i3dea.mesh_name", text="Set Mesh Name")
            row = box.row()
            row.operator("i3dea.mirror_orientation", text="Set mirror orientation")
            row.operator("i3dea.fill_volume", text="Check Fill Volume")
            if giants_i3d:
                row = box.row()
                row.operator("i3dea.ignore", text="Add Suffix _ignore")
                row.operator("i3dea.xml_config", text="Enable export to i3dMappings")
        # "Track-Tools" Box
        box = layout.box()
        row = box.row()
        # expand button for "Track-Tools"
        row.prop(context.scene.i3dea, "UI_track_tools", text="Track-Tools", icon='TRIA_DOWN' if context.scene.i3dea.UI_track_tools else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_track_tools:
            col = box.column()
            box = col.box()
            row = box.row()
            row.prop(context.scene.i3dea, "UI_uvset", text="UVset 2", icon='TRIA_DOWN' if context.scene.i3dea.UI_uvset else 'TRIA_RIGHT', icon_only=False, emboss=False)
            if context.scene.i3dea.UI_uvset:
                row = box.row()
                row.prop(context.scene.i3dea, "custom_text_box", text="Custom Name")
                if context.scene.i3dea.custom_text_box:
                    row = box.row()
                    row.prop(context.scene.i3dea, "custom_text", text="Custom track name")
                row = box.row()
                row.prop(context.scene.i3dea, "size_dropdown", text="")
                row.operator("i3dea.make_uvset", text="Create UVset 2")
            box = col.box()
            row = box.row()
            row.prop(context.scene.i3dea, "add_empty_int", text="")
            row.operator("i3dea.add_empty", text="Add Empty", icon='EMPTY_DATA')
            box = col.box()
            row = box.row()
            row.operator("i3dea.curve_length", text="Get Curve Length", icon='MOD_LENGTH')
            row.prop(context.scene.i3dea, "curve_length_disp", text="")
            box = col.box()
            row = box.row()
            row.prop(context.scene.i3dea, "piece_distance", text="")
            row.operator("i3dea.calculate_amount", text="Calculate Amount")
            row = box.row()
            row.prop(context.scene.i3dea, "track_piece_amount", text="")
            box = col.box()
            row = box.row()
            row.operator("i3dea.track_on_curve", text="Add track along curve")
            row.operator("i3dea.track_on_curve_delete", text="Delete")
            # row.prop(context.scene.i3dea, "curve_length_disp", text="")
        # ---------------------------------------------------------------
        # "Skeleton-Tools" Box
        box = layout.box()
        row = box.row()
        # expand button for "Skeletons"
        row.prop(context.scene.i3dea, "UI_skeletons", text="Skeletons", icon='TRIA_DOWN' if context.scene.i3dea.UI_skeletons else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_skeletons:
            row = box.row()
            row.prop(context.scene.i3dea, "skeletons_dropdown", text="")
            row.operator("i3dea.skeletons", text="Create", icon='BONE_DATA')
        # ---------------------------------------------------------------
        # "Material-Tools" box
        box = layout.box()
        row = box.row()
        # extend button for "Material-Tools"
        row.prop(context.scene.i3dea, "UI_materialTools", text="Material-Tools", icon='TRIA_DOWN' if context.scene.i3dea.UI_materialTools else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_materialTools:
            row = box.row()
            row.operator("i3dea.mirror_material", text="Add Mirror Material")
            row.operator("i3dea.remove_duplicate_material", text="Remove Duplicate Materials")
            col = box.column()
            box = col.box()
            row = box.row()
            row.prop(context.scene.i3dea, "UI_create_mat", text="Create a material", icon='TRIA_DOWN' if context.scene.i3dea.UI_create_mat else 'TRIA_RIGHT', icon_only=False, emboss=False)
            if context.scene.i3dea.UI_create_mat:
                # row.label(text="Create a material")
                row = box.row()
                row.prop(context.scene.i3dea, "diffuse_box", text="Diffuse")
                if context.scene.i3dea.diffuse_box:
                    row.prop(context.scene.i3dea, "alpha_box", text="Alpha")
                row = box.row()
                row.prop(context.scene.i3dea, "material_name", text="")
                if context.scene.i3dea.diffuse_box:
                    row = box.row()
                    row.prop(context.scene.i3dea, "diffuse_texture_path", text="Diffuse")
                row = box.row()
                row.prop(context.scene.i3dea, "spec_texture_path", text="Specular")
                row = box.row()
                row.prop(context.scene.i3dea, "normal_texture_path", text="Normal")
                row = box.row()
                row.operator("i3dea.setup_material", text="Create " + bpy.context.scene.i3dea.material_name)
            if stjerne_i3d:
                box = col.box()
                row = box.row()
                row.prop(context.scene.i3dea, "UI_paths", text="Add paths to material", icon='TRIA_DOWN' if context.scene.i3dea.UI_paths else 'TRIA_RIGHT', icon_only=False, emboss=False)
                if context.scene.i3dea.UI_paths:
                    row = box.row()
                    row.prop(context.scene.i3dea, "shader_box", text="")
                    row.prop(context.scene.i3dea, "shader_path", text="Shader path")
                    row = box.row()
                    row.prop(context.scene.i3dea, "mask_map_box", text="")
                    row.prop(context.scene.i3dea, "mask_map", text="Mask texture")
                    row = box.row()
                    row.prop(context.scene.i3dea, "dirt_diffuse_box", text="")
                    row.prop(context.scene.i3dea, "dirt_diffuse", text="Dirt texture")
                    row = box.row()
                    row.operator("i3dea.i3dio_material", text="Run")
        # -----------------------------------------
        # "Assets Importer" box
        box = layout.box()
        row = box.row()
        # extend button for "Assets Importer"
        row.prop(context.scene.i3dea, "UI_assets", text="Assets Importer", icon='TRIA_DOWN' if context.scene.i3dea.UI_assets else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_assets:
            row = box.row()
            row.prop(context.scene.i3dea, "assets_dropdown", text="")
            row = box.row()
            row.operator("i3dea.assets", text="Import Asset")
        # -----------------------------------------
