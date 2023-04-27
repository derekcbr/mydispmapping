import bpy


def create_glass_mat():
    mat = bpy.data.materials.new('glasswindow')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    mat.node_tree.nodes.remove(bsdf)
    my_material_output = mat.node_tree.nodes['Material Output']
    my_material_output.location = (920.0, 290.0)
    my_transparent_0 = mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
    my_transparent_0.location = (271.0, 112.0)
    my_add_shader = mat.node_tree.nodes.new('ShaderNodeAddShader')
    my_add_shader.location = (545.0, 32.0)
    my_mix_1 = mat.node_tree.nodes.new('ShaderNodeMixShader')
    my_mix_1.location = (690.0, 290.0)
    my_mix_1.inputs['Fac'].default_value = 0.1
    my_glossy_0 = mat.node_tree.nodes.new('ShaderNodeBsdfGlossy')
    my_glossy_0.location = (271.0, 4.0)
    my_glossy_0.inputs['Roughness'].default_value = 0.0
    my_glass_bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfGlass')
    my_glass_bsdf.location = (304.0, 304.0)
    my_glass_bsdf.inputs['Roughness'].default_value = 0.0
    my_glass_bsdf.inputs['IOR'].default_value = 1.45
    my_math = mat.node_tree.nodes.new('ShaderNodeMath')
    my_math.location = (473.0, 483.0)
    my_math.inputs['Value'].default_value = 0.5
    my_math.inputs['Value'].default_value = 0.5
    my_math.inputs['Value'].default_value = 0.0
    my_light_0 = mat.node_tree.nodes.new('ShaderNodeLightPath')
    my_light_0.location = (23.0, 645.0)
    mat.node_tree.links.new(my_mix_1.outputs['Shader'], my_material_output.inputs['Surface'])
    mat.node_tree.links.new(my_glass_bsdf.outputs['BSDF'], my_mix_1.inputs[1])
    mat.node_tree.links.new(my_transparent_0.outputs['BSDF'], my_add_shader.inputs[0])
    mat.node_tree.links.new(my_add_shader.outputs['Shader'], my_mix_1.inputs[2])
    mat.node_tree.links.new(my_math.outputs['Value'], my_mix_1.inputs['Fac'])
    mat.node_tree.links.new(my_light_0.outputs['Is Diffuse Ray'], my_math.inputs[0])
    mat.node_tree.links.new(my_light_0.outputs['Transparent Depth'], my_math.inputs[1])
    mat.node_tree.links.new(my_glossy_0.outputs['BSDF'], my_add_shader.inputs[1])
    return mat
