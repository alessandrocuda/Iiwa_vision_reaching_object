import bpy, sys
bpy.ops.import_mesh.stl(filepath=sys.argv[-1]+".stl")
bpy.ops.wm.collada_export(filepath=sys.argv[-1]+".dae")
