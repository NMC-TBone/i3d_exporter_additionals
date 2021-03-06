# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# track_tools.py includes different tools for uv

import bpy
import math


class I3DEA_OT_add_empty(bpy.types.Operator):
    bl_label = "Create empties"
    bl_idname = "i3dea.add_empty"
    bl_description = "Create empties between selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_list = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        for _ in range(context.scene.i3dea.add_empty_int):
            for loop_obj in selected_list:
                bpy.ops.object.empty_add(radius=0)
                empty = bpy.context.active_object
                empty.name = loop_obj.name + ".001"
                if loop_obj.parent is not None:
                    empty.parent = loop_obj.parent

        bpy.ops.object.select_all(action='DESELECT')
        for loop_obj in selected_list:
            bpy.data.objects[loop_obj.name].select_set(True)
            self.report({'INFO'}, "Empties added")
            return {'FINISHED'}


def getCurveLength(length):
    length = bpy.context.active_object.data.splines[0].calc_length(resolution=1024)
    return length


class I3DEA_OT_curve_length(bpy.types.Operator):
    bl_idname = "i3dea.curve_length"
    bl_label = "Get Curve Length"
    bl_description = "Measure length of the selected curve"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, length):
        if bpy.context.view_layer.objects.active is None:
            self.report({'ERROR'}, "No active object in scene")
            return {'CANCELLED'}
        if not bpy.context.active_object.type == "CURVE":
            self.report({'ERROR'}, "The active object [" + bpy.context.active_object.name + "] is not a curve")
            return {'CANCELLED'}
        else:
            curve_length = getCurveLength(length)
            bpy.context.scene.i3dea.curve_length_disp = curve_length
        return {'FINISHED'}


class I3DEA_OT_calculate_amount(bpy.types.Operator):
    bl_idname = "i3dea.calculate_amount"
    bl_label = "Calculate Amount"
    bl_description = "Calculates how many track pieces that fit from given track piece length and curve length"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, length):
        if bpy.context.view_layer.objects.active is None:
            self.report({'ERROR'}, "No active object in scene")
            return {'CANCELLED'}
        # if not bpy.context.active_object.type == "CURVE":
        #     self.report({'ERROR'}, "The active object [" + bpy.context.active_object.name + "] is not a curve")
        #     return {'CANCELLED'}
        if len(bpy.context.selected_objects) == 2:
            obj1 = bpy.context.selected_objects[0].location
            obj2 = bpy.context.selected_objects[1].location
            # print(math.dist(obj1, obj2))
            bpy.context.scene.i3dea.piece_distance = math.dist(obj1, obj2)
            # curve_length = getCurveLength(length)
        if bpy.context.active_object.type == 'CURVE':
            curve_length = getCurveLength(length)
            float_val = curve_length/bpy.context.scene.i3dea.piece_distance
            # print(float_val)
            rounded_val = round(float_val)
            string = str(float_val and rounded_val)
            bpy.context.scene.i3dea.track_piece_amount = string

        return {'FINISHED'}


class I3DEA_OT_track_on_curve(bpy.types.Operator):
    bl_idname = "i3dea.track_on_curve"
    bl_label = "Add track along curve"
    bl_description = "Makes a full setup to see how the track will look along the curve"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        types = ['MESH', 'CURVE']
        selected_list = [obj for obj in bpy.context.selected_objects if obj.type in types]
        piece_list = [mesh for mesh in selected_list if mesh.type == 'MESH']
        curve_list = [curve for curve in selected_list if curve.type == 'CURVE']

        if len(bpy.context.selected_objects) == 2:
            for piece, curve in zip(piece_list, curve_list):

                hierarchy_name = 'track_visualization'
                space = bpy.context.scene.i3dea.piece_distance
                if bpy.context.scene.i3dea.track_piece_amount:
                    piece_num = int(bpy.context.scene.i3dea.track_piece_amount)
                else:
                    piece_num = 30
                    self.report({'INFO'}, "No amount set in track piece amount, using default instead")

                bpy.ops.mesh.primitive_plane_add()
                plane = bpy.context.object
                plane.name = hierarchy_name
                plane.dimensions[1] = space
                bpy.ops.object.transform_apply(scale=True)
                plane.instance_type = 'FACES'
                plane.show_instancer_for_viewport = False
                plane.modifiers.new("Array", 'ARRAY')
                plane.modifiers["Array"].use_relative_offset = False
                plane.modifiers["Array"].use_constant_offset = True
                plane.modifiers["Array"].constant_offset_displace[0] = 0
                plane.modifiers["Array"].constant_offset_displace[1] = space
                plane.modifiers["Array"].count = piece_num
                plane.modifiers.new("Curve", 'CURVE')
                plane.modifiers["Curve"].object = curve
                plane.modifiers["Curve"].deform_axis = 'NEG_Y'

                piece.parent = plane

        return {'FINISHED'}


class I3DEA_OT_track_on_curve_delete(bpy.types.Operator):
    bl_idname = "i3dea.track_on_curve_delete"
    bl_label = "Delete track visualization"
    bl_description = "Deletes the track visualization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj_list = [obj for obj in bpy.data.objects if obj.name.startswith("track_visualization")]

        if obj_list:
            for obj in obj_list:
                # for children in obj.children_recursive:
                #     bpy.data.objects.remove(children)
                bpy.data.objects.remove(obj)
        return {'FINISHED'}


class I3DEA_OT_make_uvset(bpy.types.Operator):
    bl_label = "Generate UVset 2"
    bl_idname = "i3dea.make_uvset"
    bl_description = "Generate UVset 2 from selected objects."
    bl_options = {'REGISTER', 'UNDO'}

    def four(self, context):
        if not bpy.context.active_object:
            self.report({'ERROR'}, "No selected object!")
            return {'CANCELLED'}
        if len(bpy.context.selected_objects) > 0:
            mode = bpy.context.object.mode
            for obj in bpy.context.selected_objects:
                if not obj.type == "MESH":
                    continue
                if not mode == 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')
        selected_obj = bpy.context.selected_objects
        for obj in selected_obj:
            if obj.type == 'MESH':
                obj.data.uv_layers[0].name = 'UVset1'
            if 'UVset2' not in obj.data.uv_layers:
                obj.data.uv_layers.new(name="UVset2")

        # start location X 0.25
        # start location Y 0.25
        # scale 0.5
        original_type = bpy.context.area.ui_type
        bpy.context.area.ui_type = 'UV'
        bpy.context.space_data.cursor_location[0] = 0.25
        bpy.context.space_data.cursor_location[1] = 0.25
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.context.space_data.pivot_point = 'CENTER'
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.transform.resize(value=[0.5, 0.5, 0.5])
        bpy.ops.object.editmode_toggle()
        bpy.context.object.name = context.scene.i3dea.custom_text + ".001"
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.75
        bpy.context.space_data.cursor_location[1] = 0.25
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.75
        bpy.context.space_data.cursor_location[1] = 0.75
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.25
        bpy.context.space_data.cursor_location[1] = 0.75
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.context.area.ui_type = original_type
        self.report({'INFO'}, "UVset2 2x2 Created")

    def sixteen(self, context):
        if not bpy.context.active_object:
            self.report({'ERROR'}, "No selected object!")
            return {'CANCELLED'}
        if len(bpy.context.selected_objects) > 0:
            mode = bpy.context.object.mode
            for obj in bpy.context.selected_objects:
                if not obj.type == "MESH":
                    continue
                if not mode == 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')
        selected_obj = bpy.context.selected_objects
        for obj in selected_obj:
            if obj.type == 'MESH':
                obj.data.uv_layers[0].name = 'UVset1'
            if 'UVset2' not in obj.data.uv_layers:
                obj.data.uv_layers.new(name="UVset2")

        # start location X 0.125
        # start location Y 0.125
        # scale 0.25
        original_type = bpy.context.area.ui_type
        bpy.context.area.ui_type = 'UV'
        bpy.context.space_data.cursor_location[0] = 0.125
        bpy.context.space_data.cursor_location[1] = 0.125
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.context.space_data.pivot_point = 'CENTER'
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.transform.resize(value=[0.25, 0.25, 0.25])
        bpy.ops.object.editmode_toggle()
        bpy.context.object.name = context.scene.i3dea.custom_text + ".001"
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.375
        bpy.context.space_data.cursor_location[1] = 0.125
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.625
        bpy.context.space_data.cursor_location[1] = 0.125
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.875
        bpy.context.space_data.cursor_location[1] = 0.125
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        # start location X 0.875
        # start location Y 0.375
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.875
        bpy.context.space_data.cursor_location[1] = 0.375
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.625
        bpy.context.space_data.cursor_location[1] = 0.375
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.375
        bpy.context.space_data.cursor_location[1] = 0.375
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.125
        bpy.context.space_data.cursor_location[1] = 0.375
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        # start location X 0.125
        # start location Y 0.625
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.125
        bpy.context.space_data.cursor_location[1] = 0.625
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.375
        bpy.context.space_data.cursor_location[1] = 0.625
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.625
        bpy.context.space_data.cursor_location[1] = 0.625
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.875
        bpy.context.space_data.cursor_location[1] = 0.625
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        # start location X 0.875
        # start location Y 0.875
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.875
        bpy.context.space_data.cursor_location[1] = 0.875
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.625
        bpy.context.space_data.cursor_location[1] = 0.875
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.375
        bpy.context.space_data.cursor_location[1] = 0.875
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.125
        bpy.context.space_data.cursor_location[1] = 0.875
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.context.area.ui_type = original_type
        self.report({'INFO'}, "UVset2 4x4 Created")

    def execute(self, context):
        if context.scene.i3dea.size_dropdown == 'four':
            self.four(context)
            return {'FINISHED'}
        if context.scene.i3dea.size_dropdown == 'sixteen':
            self.sixteen(context)
            return {'FINISHED'}
        return {'FINISHED'}
