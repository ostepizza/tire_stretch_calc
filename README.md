# Tire Stretch Calculator

Python calculator for visualizing tire size and stretching, as well as comparing multiple tire and rim configurations.

## Features
- Generate front and side visualizations of tire and rim configurations.
- Generate JSON-comparison of multiple rim and tire configurations
- Configuration-file for file-saving and image-settings

## Prerequisites

1. Requires Python Imaging Library (PIL) (`pip install pillow`)

## Example Usage
### Input explanation
Using example 7.5 inch wide 17" rim, on 205/45R17 tires:
- `rim_diameter_inch`: Diameter of the rim in inches (17).
- `rim_width_inch`: Width of the rim in inches (7.5).
- `tire_width_mm`: Width of the tire in millimeters (205).
- `tire_height_relative`: Relative height of the tire (45).
- As tire size (R17) is the same as the rim diameter, it is not used
- `rim_diameter_additional`: Extra inches to account for outside diameter. Using 1.5", estimates a 0.75" lip protruding past rim barrel.
- `rim_width_additional`: Extra inches to account for outside width. Using 1", estimates a 0.5" lip on each side of the rim.

### Example usage in practice
1. Edit script and create tire-objects using rim diameter, rim width, tire width, relative tire sidewall, as well as rim additional diameter and width (as rim specifications are inside measurements):
   
`tire_baseline = Tire(17, 7.5, 205, 45, 1.5, 1)`

For comparison, more configurations can be added:

`tire_compare = Tire(17, 7.5, 205, 50, 1.5, 1)`

`tire_compare_2 = Tire(17, 7.5, 205, 55, 1.5, 1)`

3. For generating images, use functions:

`generateTireImageFront(tire_baseline)`

`generateTireImageSide(tire_baseline)`

5. For generating comparison JSON, use function:
   
`compareTires([tire_baseline, tire_compare, tire_compare_2])`

## Configuring
On first run, a config.json is generated:

`save_images`: true/false - Whether images are saved locally, default is true

`save_comparison`: true/false - Whether comparison file is saved locally, default is true

`generate_image_on_compare`: true/false - Whether images should be generated for every configuration compared, default is false

`output_folder`: string - Name of output folder, default is "output"

`image_width`: number - Width of generated images in pixels, default is 500

`image_height`: number - Height of generated images in pixels, default is 500

`image_dpi`: number - How many pixels 1 inch equals to, default is 16

`outline_width`: number - Relative outline thickness on generated images, default is 2

`outline_rim_color`: string - Color of outlines of the rim in generated images, default is "white"

`outline_tire_color`: string - Color of outlines of the tire in generated images, default is "red"

`font_color`: string - Color of text displaying rim and tire info on generated images, default is "red"

`font`: string - Filename of font used to display rim and tire info, default is "arial.ttf"

