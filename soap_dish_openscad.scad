union(){
  import("border.stl");
  intersection(){
      scale([0.25,0.25,1])
        linear_extrude(height = 5)
          import(file = "file.svg", center = true);
      import("intersect_base.stl");
}}
