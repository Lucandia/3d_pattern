import("border.stl");
rotate(a=[0,0,Z_DEG])
  scale([X_SCALE,Y_SCALE,1])
    linear_extrude(height = 5)
      import(file = "file.svg", center = true);
