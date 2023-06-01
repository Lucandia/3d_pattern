import subprocess
import plotly
import numpy as np
from stl import mesh  # pip install numpy-stl
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import os
import time

def stl2mesh3d(stl_mesh):
    # stl_mesh is read by nympy-stl from a stl file; it is  an array of faces/triangles (i.e. three 3d points)
    # this function extracts the unique vertices and the lists I, J, K to define a Plotly mesh3d
    p, q, r = stl_mesh.vectors.shape #(p, 3, 3)
    # the array stl_mesh.vectors.reshape(p*q, r) can contain multiple copies of the same vertex;
    # extract unique vertices from all mesh triangles
    vertices, ixr = np.unique(stl_mesh.vectors.reshape(p*q, r), return_inverse=True, axis=0)
    I = np.take(ixr, [3*k for k in range(p)])
    J = np.take(ixr, [3*k+1 for k in range(p)])
    K = np.take(ixr, [3*k+2 for k in range(p)])
    return vertices, I, J, K

def figure_mesh(filename):
  my_mesh = mesh.Mesh.from_file(filename)
  vertices, I, J, K = stl2mesh3d(my_mesh)
  x, y, z = vertices.T
  colorscale= [[0, '#e5dee5'], [1, '#e5dee5']]
  mesh3D = go.Mesh3d(
              x=x,
              y=y,
              z=z,
              i=I,
              j=J,
              k=K,
              name='soap_dish_mesh',
              showscale=False,
              colorscale=colorscale, 
              intensity=z,
              flatshading=True,)
  title = "Soap dish mesh"
  layout = go.Layout(
              paper_bgcolor='rgb(1,1,1)',
              title_text=None,# title_x=0.5, font_color='white',
              width=800,
              height=800,
              scene_camera=dict(eye=dict(x=1.25, y=-1.25, z=1)),
              scene_xaxis_visible=True,
              scene_yaxis_visible=True,
              scene_zaxis_visible=False)
  fig = go.Figure(data=[mesh3D], layout=layout)

  fig.data[0].update(lighting=dict(ambient= 0.18,
                                   diffuse= 1,
                                   fresnel=  .1,
                                   specular= 1,
                                   roughness= .1,
                                   facenormalsepsilon=0))
  fig.data[0].update(lightposition=dict(x=3000,
                                        y=3000,
                                        z=10000));
  fig.update_scenes(aspectmode='data')
  fig.write_html("file_stl.html")
  return fig

if __name__ == "__main__":
    st.title('Soap Dish 3D Pattern')
    st.write('Generate a 3D model for a custom soap dish! You can find more information about the soap dish here on [Printables](https://www.printables.com/it/model/489136-geometric-soap-dish-holder-normal-with-plate-or-or).')
    st.write('Note: Make sure are the lines of the image are connected to avoid separeted bodies in the mesh')
    # get files
    cwd = os.getcwd() + os.sep
    ## clean previous file
    #for file in os.listdir():
    #    if 'file.' in file:
    #       os.remove(file)
    #if 'preview.png' in os.listdir():
    #    os.remove('preview.png')
    filetype = st.selectbox('Choose the file type', ['svg', 'png', 'jpg', 'jpeg'])
    if filetype != 'svg':
        st.write(f'The mesh generated from a {filetype} file is not always predictable')
    
    # SCALE
    scales = [1.0, 1.0]
    col1, col2, col3 = st.columns(3)
    with col1:
        scale = st.checkbox('Rescale image size')
    if scale:
        with col2:
            scales[0] = scales[0] * st.number_input('X scale %', min_value=0.0, value=100.0) / 100
        with col3:
            scales[1] = scales[1] * st.number_input('Y scale %', min_value=0.0, value=100.0) / 100
    
    # ROTATE
    rot = 0
    col1, col2 = st.columns(2)
    with col1:
        rotate = st.checkbox('Rotate the image')
    if rotate:
        with col2:
            rot = st.number_input('Angle', value=0.0) 

    # Preview with quick render
    run_file = cwd + 'soap_dish_openscad.scad'
    preview = st.checkbox('Quick preview', help='Preview mode renders the models without performing boolean operation. It just renders your image/pattern and the border of the soap dish. It is faster than normal rendering, to understand the scaling of the image.')
    if preview:
        run_file = cwd + 'preview.scad'

    uploaded_file = st.file_uploader("Upload the file:", type=[filetype])
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open(f'{cwd}file.{filetype}', 'wb') as f:
            f.write(bytes_data)

        # convert the png to svg
        if filetype != 'svg':
            subprocess.run(f'convert {cwd}file.{filetype} {cwd}file.pnm', shell = True)
            subprocess.run(f'potrace -s -o {cwd}file.svg {cwd}file.pnm', shell = True)
                            
        # resize the scale of the svg
        # read old run file
        with open(run_file, 'r') as f:
            text = f.read()
        # change run file to a scaled one
        run_file = run_file.replace('.scad', '_run.scad')
        # replace scales in the openscad template
        text_replaced = text.replace('X_SCALE', str(scales[0]), 1).replace('Y_SCALE', str(scales[1]), 1).replace('Z_DEG', str(rot))
        with open(run_file, 'w') as f:
            f.write(text_replaced)
        st.write('The program renders with OpenScad, full rendering of a mesh takes a while. If you want to run it faster on your pc, check out the [Github page](https://github.com/lmonari5/soap_dish_3d_pattern.git).')
        if not st.button('Run'):
            st.stop()
        start = time.time()
        # run openscad
        with st.spinner('Rendering in progress...'):
            if preview:
                subprocess.run(f'xvfb-run -a openscad -o preview.png --camera=0,0,0,0,0,90,250 --projection=ortho {run_file}', shell = True)
            else:
                subprocess.run(f'openscad {run_file} -o {cwd}file.stl', shell = True)
        end = time.time()
        st.success(f'Rendered in {end-start} seconds', icon="✅")
        if preview:
            st.write('Preview image:')
            image = Image.open('preview.png')
            st.image(image, caption='Openscad preview')
            image.close()
        else:
            with open(f"{cwd}file.stl", "rb") as file:
              btn = st.download_button(
                label="Download mesh",
                data=file,
                file_name="soap_dish.stl",
                mime="model/stl"
              )
            st.write('Interactive mesh preview:')
            st.plotly_chart(figure_mesh(f'{cwd}file.stl'), use_container_width=True)

