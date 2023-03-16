import re
import bpy

def find_diffuse_image(node_tree):
    nodes = node_tree.nodes
    """Finds the Diffuse Image node in the given node tree"""
    for node in node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            print('image test')
            for keyword in ['dif', 'diff', 'base', 'base color', 'albedo', 'color','diffuse']:
                if re.search(keyword, node.image.name, re.IGNORECASE) or keyword==node.name.lower() or keyword==node.label.lower() and not contains_negative_keywords(node.image.name):
                    return node

    # Check sub-nodetrees
    for node in node_tree.nodes:
        if node.type in ['NodeGroup', 'NodeTree','tree','subtree','GROUP', 'SHADER']:
            sub_tree = node.node_tree
            print('subtree test: ',sub_tree)
            if sub_tree is not None:
                diffuse_node = find_diffuse_image(sub_tree)
                if diffuse_node is not None:
                    print('found dif image in subtree')
                    sub_tree.nodes.active=diffuse_node
                    return node
                
    return None

def secondary_find_diffuse_image(node_tree):
    nodes = node_tree.nodes
    """Finds the Diffuse Image node in the given node tree"""
    for node in node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            print('image test')
            if  not contains_negative_keywords(node.image.name):
                return node

    # Check sub-nodetrees
    for node in node_tree.nodes:
        if node.type in ['NodeGroup', 'NodeTree','tree','subtree','GROUP', 'SHADER']:
            sub_tree = node.node_tree
            print('subtree test: ',sub_tree)
            if sub_tree is not None:
                diffuse_node = secondary_find_diffuse_image(sub_tree)
                if diffuse_node is not None:
                    print('found dif image in subtree')
                    sub_tree.nodes.active=diffuse_node
                    return node
                
    return None

def contains_negative_keywords(text):
    keywords=['_r','_n','_b','roughness','emmi','spec','glos','ambient',"AO","METAL"]
    for kw in keywords:
        if re.search(kw, text, re.IGNORECASE):
            return True 
    
    return False
    
def make_diffuse_image_active(material):
    """Sets Diffuse Image as the active node for the given material"""
    node_tree = material.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    diffuse_node = find_diffuse_image(node_tree)
    alt_diffuse_node =secondary_find_diffuse_image(node_tree)

    if diffuse_node is not None:
        nodes.active = diffuse_node

        print('Diffuse Image set as active node')
    elif alt_diffuse_node is not None:
        nodes.active=alt_diffuse_node
    else:
        print('Diffuse Image not found')


# The replace_node() function from the original code would go here
def make_all_diffuse_active():
    
    # Iterate over all materials in the scene
    for mat in bpy.data.materials:
        try: 
            make_diffuse_image_active(mat)
        except:
            pass


make_all_diffuse_active()
