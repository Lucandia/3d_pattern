import plotly
import numpy as np
from stl import mesh  # pip install numpy-stl
import plotly.graph_objects as go

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

my_mesh = mesh.Mesh.from_file('AT&T-Building.stl')
# stl file from: https://github.com/stephenyeargin/stl-files/blob/master/AT%26T%20Building.stl
vertices, I, J, K = stl2mesh3d(my_mesh)
x, y, z = vertices.T
colorscale= [[0, '#e5dee5'], [1, '#e5dee5']]
title = "Mesh3d from a STL file<br>AT&T building"
layout = go.Layout(paper_bgcolor='rgb(1,1,1)',
            title_text=title, title_x=0.5,
                   font_color='white',
            width=800,
            height=800,
            scene_camera=dict(eye=dict(x=1.25, y=-1.25, z=1)),
            scene_xaxis_visible=False,
            scene_yaxis_visible=False,
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

import chart_studio.plotly as py
py.iplot(fig, filename='ATandT-building')