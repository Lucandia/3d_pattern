import("DIR/border.stl");
linear_extrude(height = 5)
  translate(v=[X_TRAN,Y_TRAN,0])
    rotate(a=[0,0,Z_DEG])
      scale([X_SCALE,Y_SCALE,1])
        import(file = "file.svg", center = true);
