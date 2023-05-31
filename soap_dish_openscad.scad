union(){
import("C:/Users/monar/Downloads/bordo.stl");
intersection(){
    scale([0.25,0.25,1])
    linear_extrude(height = 20)
    import(file = "C:/Users/monar/Pictures/curve_small.svg", center = true, dpi = 10);
    import("C:/Users/monar/Downloads/intersect_base.stl");
}}