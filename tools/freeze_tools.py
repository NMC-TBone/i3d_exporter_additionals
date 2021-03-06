"""freezeTools.py Includes tools to freeze translation, rotation and scale"""

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

import bpy


class I3DEA_OT_freeze_trans(bpy.types.Operator):
    bl_idname = "i3dea.freeze_trans"
    bl_label = "Freeze Translation"
    bl_description = "Freezes translation of selected object(s)."
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
        self.report({'INFO'}, "Freezed Location")
        return {'FINISHED'}


class I3DEA_OT_freeze_rot(bpy.types.Operator):
    bl_idname = "i3dea.freeze_rot"
    bl_label = "Freeze Rotation"
    bl_description = "Freezes rotation of selected object(s)."
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        self.report({'INFO'}, "Freezed Rotation")
        return {'FINISHED'}


class I3DEA_OT_freeze_scale(bpy.types.Operator):
    bl_idname = "i3dea.freeze_scale"
    bl_label = "Freeze Scale"
    bl_description = "Freezes scale of selected object(s)."
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        self.report({'INFO'}, "Freezed Scale")
        return {'FINISHED'}


class I3DEA_OT_freeze_all(bpy.types.Operator):
    bl_idname = "i3dea.freeze_all"
    bl_label = "Freeze All"
    bl_description = "Freezes translation, rotation and scale of selected object(s)."
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        self.report({'INFO'}, "Freezed Translation, Rotation and Scale")
        return {'FINISHED'}