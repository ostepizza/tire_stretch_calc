from PIL import Image, ImageDraw

# rims
rim_diameter_inch = 17
rim_width_inch = 10

# tires
tire_width_mm = 205
tire_height_relative = 45
tire_diameter_inch = 17

# image 
image_width = 500
image_height = 500
image_dpi = 16


# prepare the rims:
rim_diameter_pixel = rim_diameter_inch * image_dpi
rim_width_pixel = rim_width_inch * image_dpi

# prepare the tires:
tire_width_inch = tire_width_mm * 0.0393701
tire_width_pixel = tire_width_inch * image_dpi
tire_height_pixel = tire_width_pixel * (tire_height_relative / 100)
tire_diameter_pixel = tire_diameter_inch * image_dpi

print("Rim diameter in pixels: ", rim_diameter_pixel)
print("Rim width in pixels: ", rim_width_pixel)
print("Tire width in pixels: ", tire_width_pixel)
print("Tire height in pixels: ", tire_height_pixel)
print("Tire diameter in pixels: ", tire_diameter_pixel)


# coordinates of the rim
rsx = image_width / 2 - rim_width_pixel / 2
rsy = image_width / 2 - rim_diameter_pixel / 2
rex = rsx + rim_width_pixel
rey = rsy + rim_diameter_pixel

# coordinates for tire, top
tsxt = rsx + rim_width_pixel / 2 - tire_width_pixel / 2
tsyt = rsy - tire_height_pixel
text = tsxt + tire_width_pixel
teyt = tsyt + tire_height_pixel

# coordinates for tire, bottom
tsxb = rsx + rim_width_pixel / 2 - tire_width_pixel / 2
tsyb = rsy + rim_diameter_pixel
texb = tsxb + tire_width_pixel
teyb = tsyb + tire_height_pixel


# Create a new image with white background
img = Image.new('RGB', (500, 500), 'black')

# Create a draw object
draw = ImageDraw.Draw(img)

# Define the points for the square
rim_coordinates = [(rsx, rsy), (rex, rsy), (rex, rey), (rsx, rey)]
tire_coordinates_top = [(tsxt, tsyt), (text, tsyt), (text, teyt), (tsxt, teyt)]
tire_coordinates_bottom = [(tsxb, tsyb), (texb, tsyb), (texb, teyb), (tsxb, teyb)]

# Draw the square
draw.polygon(rim_coordinates, outline='white')
draw.polygon(tire_coordinates_top, outline='red')
draw.polygon(tire_coordinates_bottom, outline='blue')

# Save the image
img.save('square.png')