import("DIR/border.stl");
translate(v=[X_TRAN,Y_TRAN,0])
  rotate(a=[0,0,Z_DEG])
    scale([X_SCALE,Y_SCALE,1])
      linear_extrude(height = 5)
        import(file = "file.svg", center = true);
