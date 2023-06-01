# Soap Dish 3D Pattern
A simple interface to generate soap dishes for 3D printing
Visit the original [Printables page](https://www.printables.com/it/model/489136-geometric-soap-dish-holder-normal-with-plate-or-or)!

## Try the web app:

[soap_dish_3d_pattern](https://lmonari5-soap-dish-3d-pattern.streamlit.app/) powered by streamlit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://lmonari5-soap-dish-3d-pattern.streamlit.app/)

## Convert png to svg

To convert a png to a svg I suggest using 'vectorize bitmap' on Inkscape. On Linux, you can install the packages imagemagick and potrace, and use the terminal commands:
```
convert YOUR_FILE.png YOUR_FILE.pnm
potrace -s -o YOUR_FILE.svg YOUR_FILE.pnm
rm YOUR_FILE.pnm
```
### Generate your soap dish from the svg:
You can use OpenScad to generate the soap dish. The code is stored in the file 'soap_dish_openscad.scad' and it is pretty simple:
```
union(){ // merge the pattern and the border
  import("YOUR_PATH/border.stl");
    intersection(){ // select the pattern area of the soap dish and make a slope
      translate(v=[X_TRAN,Y_TRAN,0]) // translate the svg image
        rotate(a=[0,0,Z_DEG]) // rotate the svg image
          scale([X_SCALE,Y_SCALE,1]) // scale the X and Y axis of the svg
            linear_extrude(height = 5) // extrude the svg
              import(file = "YOUR_PATH/YOUR_FILE.svg", center = true);
    import("YOUR_PATH/intersect_base.stl");
}}
```
Remember to change:
- X_TRAN, Y_TRAN with the displacement to move the image
- Z_DEG with the angle to rotate the image
- X_SCALE, Y_SCALE with the scale of the x-axis and y-axis 
- the file paths for 'intersect_base.stl' and 'border.stl' (you can find the files in the Github repository)
- the file path for your svg file.

 
## Donate

I enjoy working on this project in my free time, especially at night. If you want to support me with a coffee, just [click here!](https://www.paypal.com/donate/?hosted_button_id=V4LJ3Z3B3KXRY)

## License

Code is licensed under the GNU General Public License v3.0 ([GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html))

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%20v3-lightgrey.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
