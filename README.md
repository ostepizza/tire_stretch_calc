# tire_stretch_calc

This Python script generates a visualization of a tire and rim configuration based on input variables.

## Prerequisites

1. Requires Python Imaging Library (PIL) (`pip install pillow`)

## Example usage

Modify the following input variables as desired:

### Rim and Tire Variables
Using example 7.5 inch wide 17" rim, on 205/45R17 tires:
- `rim_diameter_inch`: Diameter of the rim in inches (17).
- `rim_width_inch`: Width of the rim in inches (7.5).
- `tire_width_mm`: Width of the tire in millimeters (205).
- `tire_height_relative`: Relative height of the tire (45).
- As tire size (R17) is the same as the rim diameter, it is not used

### Image Variables

- `image_width`: Image width in pixels.
- `image_height`: Image height in pixels.
- `image_dpi`: DPI of the image (how many pixels per inch).
- `outline_width`: Width of the outlines drawn.
- `outline_rim_color`: Color of the rim outline.
- `outline_tire_color`: Color of the tire outline.
- `font_color`: Color of the text.

### Additional Variables
- `rim_diameter_additional`: Extra inches to account for diameter. Default is 0,
and should not need to be modified, as visualization shows inner diameter but outside width.
- `rim_width_additional`: Extra inches to account for width. Default is 1, estimating a 0.5" lip on each side of the rim


Run the script, and the generated image will be saved as `result.png` in the same directory.
