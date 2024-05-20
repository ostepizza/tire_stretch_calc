from PIL import Image, ImageDraw, ImageFont
import os
import json

# Load settings from config.json, or create it if it doesn't exist
def load_settings():
    if not os.path.exists('config.json'):
        config = {
            "save_images": True,
            "save_comparison": True,
            "output_folder": "output",
            "image_width": 500,
            "image_height": 500,
            "image_dpi": 16,
            "outline_width": 2,
            "outline_rim_color": "white",
            "outline_tire_color": "red",
            "font_color": "red",
            "font": "arial.ttf"
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
    else:
        with open('config.json', 'r') as f:
            config = json.load(f)
    return config

config = load_settings()

# Create output file folder if it doesn't exist
if config['save_images'] is True or config['save_comparison'] is True:
    subfolder = config['output_folder']
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

# Tire class to store tire properties
class Tire:
    def __init__(self, rim_diameter_inch = 17, rim_width_inch = 7.5, tire_width_mm = 205, tire_height_relative = 45, rim_diameter_additional = 0, rim_width_additional = 1):
        self.rim_diameter_inch = rim_diameter_inch
        self.rim_diameter_mm = self.rim_diameter_inch * 25.4
        self.rim_width_inch = rim_width_inch
        self.rim_width_mm = self.rim_width_inch * 25.4
        self.rim_diameter_additional_inch = rim_diameter_additional
        self.rim_diameter_additional_mm = self.rim_diameter_additional_inch * 25.4
        self.rim_width_additional_inch = rim_width_additional
        self.rim_width_additional_mm = self.rim_width_additional_inch * 25.4

        self.tire_width_t_mm = tire_width_mm
        self.tire_width_t_inch = self.tire_width_t_mm / 25.4
        self.tire_width_b_inch = self.rim_width_inch + self.rim_width_additional_inch
        self.tire_width_b_mm = self.tire_width_b_inch * 25.4
        self.tire_height_relative = tire_height_relative

        # Calculate difference between top and bottom tire width, to get a relative height using sidewall length
        self.__tire_area = self.tire_width_t_inch * (self.tire_width_t_inch * (self.tire_height_relative / 100))
        self.__average_width = (self.tire_width_t_inch + self.tire_width_b_inch) / 2
        self.tire_height_adj_inch = self.__tire_area / self.__average_width
        self.tire_height_adj_mm = self.tire_height_adj_inch * 25.4

# Compare a list of tires to a base tire (base tire is the first tire in the list)
def compareTires(tires):
    if not all(isinstance(tire, Tire) for tire in tires):
        raise TypeError('All elements in the list must be Tire objects')
    
    # Set the base tire to the first tire in the list
    base_tire = tires[0]

    # Base tire properties
    base_tire_diameter_mm = round(base_tire.rim_diameter_mm + (base_tire.tire_height_adj_mm * 2), 2) 
    base_tire_circumference_mm = round(base_tire_diameter_mm * 3.14159265359, 2)
    tire_speedometer_difference_percent = 0
    base_tire_reading_50kmh = 50
    base_tire_reading_100kmh = 100
    base_tire_ride_height_difference = 0

    # Add the base tire to the comparison list
    base_tire_dict = {
        'tire': str(base_tire.rim_diameter_inch) + "x" + str(base_tire.rim_width_inch) + ", " + str(base_tire.tire_width_t_mm) + "/" + str(base_tire.tire_height_relative) + "R" + (str(base_tire.rim_diameter_inch)),
        'diameter_mm': base_tire_diameter_mm,
        'circumference_mm': base_tire_circumference_mm,
        'speedometer_difference_percent': tire_speedometer_difference_percent,
        'reading_50kmh': base_tire_reading_50kmh,
        'reading_100kmh': base_tire_reading_100kmh,
        'ride_height_difference_mm': base_tire_ride_height_difference
    }

    comparison = [base_tire_dict]

    for tire in tires[1:]:
        # Calculate the properties for the tire
        tire_diameter_mm = round(tire.rim_diameter_mm + (tire.tire_height_adj_mm * 2), 2)
        tire_circumference_mm = round(tire_diameter_mm * 3.14159265359, 2)

        # Calculate the difference in speedometer reading
        tire_speedometer_difference_percent = ((tire_circumference_mm - base_tire_circumference_mm) / base_tire_circumference_mm) * 100
        tire_speedometer_difference_percent = round(tire_speedometer_difference_percent, 2)
        tire_speedometer_difference_percent = -(tire_speedometer_difference_percent)
        
        # Calculate the speedometer reading at 50km/h and 100km/h
        tire_reading_50kmh = base_tire_reading_50kmh * (1 + (tire_speedometer_difference_percent / 100))
        tire_reading_50kmh = round(tire_reading_50kmh, 2)

        tire_reading_100kmh = base_tire_reading_100kmh * (1 + (tire_speedometer_difference_percent / 100))
        tire_reading_100kmh = round(tire_reading_100kmh, 2)

        # Calculate the difference in ride height
        tire_ride_height_difference = (tire_diameter_mm - base_tire_diameter_mm) / 2

        # Add the tire to the comparison list
        tire_dict = {
            'tire': str(tire.rim_diameter_inch) + "x" + str(tire.rim_width_inch) + ", " + str(tire.tire_width_t_mm) + "/" + str(tire.tire_height_relative) + "R" + (str(tire.rim_diameter_inch)),
            'diameter_mm': tire_diameter_mm,
            'circumference_mm': tire_circumference_mm,
            'speedometer_difference_percent': tire_speedometer_difference_percent,
            'reading_50kmh': tire_reading_50kmh,
            'reading_100kmh': tire_reading_100kmh,
            'ride_height_difference_mm': tire_ride_height_difference
        }

        comparison.append(tire_dict)

    # Save the tire comparisons to a JSON file
    with open(os.path.join(subfolder, 'comparison.json'), 'w') as output_file:
        json.dump(comparison, output_file, indent=4)
        print ("Tire comparison saved as: comparison.json")

    return

# Generate an image of the tire from the side
def generateTireImageSide(tire):
    if not isinstance(tire, Tire):
        raise TypeError('Expected a Tire object')
    
    # Image settings
    image_width = config['image_width']
    image_height = config['image_height']
    image_dpi = config['image_dpi']
    outline_width = config['outline_width']
    outline_rim_color = config['outline_rim_color']
    outline_tire_color = config['outline_tire_color']
    font_color = config['font_color']
    font = config['font']

    # Convert rim size in inches to pixels
    rim_diameter = (tire.rim_diameter_inch) * image_dpi
    rim_diameter_lip = (tire.rim_diameter_additional_inch * image_dpi)

    tire_height = tire.tire_height_adj_inch * image_dpi

    # Calculate the top-left and bottom-right coordinates for the circle
    rim_top_left = ((image_width - rim_diameter) / 2, (image_height - rim_diameter) / 2)
    rim_bottom_right = ((image_width + rim_diameter) / 2, (image_height + rim_diameter) / 2)
    rim_lip_top_left = ((image_width - rim_diameter - rim_diameter_lip) / 2, (image_height - rim_diameter - rim_diameter_lip) / 2)
    rim_lip_bottom_right = ((image_width + rim_diameter + rim_diameter_lip) / 2, (image_height + rim_diameter + rim_diameter_lip) / 2)
    tire_top_left = ((image_width - rim_diameter - (tire_height * 2)) / 2, (image_width - rim_diameter - (tire_height * 2)) / 2)
    tire_bottom_right = ((image_width + rim_diameter + (tire_height * 2)) / 2, (image_width + rim_diameter + (tire_height * 2)) / 2)

    # Set up image and draw object
    img = Image.new('RGB', (image_width, image_height), 'black')
    draw = ImageDraw.Draw(img)
    outline_width_relative = round((outline_width * image_dpi) / 16)

    # Draw the rim, rim lip, then tire
    draw.ellipse([rim_top_left, rim_bottom_right], outline=outline_rim_color, width=outline_width_relative)
    draw.ellipse([rim_lip_top_left, rim_lip_bottom_right], outline=outline_rim_color, width=outline_width_relative)
    draw.ellipse([tire_top_left, tire_bottom_right], outline=outline_tire_color, width=outline_width_relative)
    
    # Text to display rim and tire size
    font = ImageFont.truetype(font, image_dpi)
    text_position = (10, 10)
    image_text = str(tire.rim_diameter_inch) + "x" + str(tire.rim_width_inch) + ", " + str(tire.tire_width_t_mm) + "/" + str(tire.tire_height_relative) + "R" + (str(tire.rim_diameter_inch))
    draw.text(text_position, image_text, fill=font_color, font=font)

    # Save the image
    filename_text = 'side_' + str(tire.rim_diameter_inch) + "x" + str(tire.rim_width_inch) + "_" + str(tire.tire_width_t_mm) + "_" + str(tire.tire_height_relative) + "R" + str(tire.rim_diameter_inch)
    img.save(os.path.join(subfolder, filename_text)  + '.png')
    img.save(os.path.join(subfolder, 'side_latest.png'))
    print ("Image saved as: ", filename_text + '.png and side_latest.png')

# Generate an image of the tire from the front
def generateTireImageFront(tire):
    if not isinstance(tire, Tire):
        raise TypeError('Expected a Tire object')
    
    # Image settings
    image_width = config['image_width']
    image_height = config['image_height']
    image_dpi = config['image_dpi']
    outline_width = config['outline_width']
    outline_rim_color = config['outline_rim_color']
    outline_tire_color = config['outline_tire_color']
    font_color = config['font_color']
    font = config['font']

    # Convert rim size in inches to pixels
    rim_diameter = (tire.rim_diameter_inch) * image_dpi
    rim_diameter_lip = (tire.rim_diameter_additional_inch * image_dpi)
    rim_width = (tire.rim_width_inch + tire.rim_width_additional_inch) * image_dpi

    # Convert tire top and bottom size in inches to pixels, as well as height
    tire_width_t = tire.tire_width_t_inch * image_dpi
    tire_width_b = tire.tire_width_b_inch * image_dpi
    tire_height = tire.tire_height_adj_inch * image_dpi

    # Coordinates of the rim (since rim is square, only four are needed)
    # rsx = rim start x, rey = rim end y 
    rsx = image_width / 2 - rim_width / 2
    rsy = image_width / 2 - rim_diameter / 2
    rex = rsx + rim_width
    rey = rsy + rim_diameter

    rim_coordinates = [(rsx, rsy), (rex, rsy), (rex, rey), (rsx, rey)]

    # Coordinates of the rim lip
    # rlxls = rim lip x left start, rlyre = rim lip y right end 
    # Left side
    rlxls = rsx
    rlyls = rsy - (rim_diameter_lip / 2)
    rlxle = rsx
    rlyle = rey + (rim_diameter_lip / 2)

    # Right side
    rlxrs = rex
    rlyrs = rsy - (rim_diameter_lip / 2)
    rlxre = rex
    rlyre = rey + (rim_diameter_lip / 2)

    rim_lip_coordinates_left = [(rlxls, rlyls), (rlxle, rlyle)]
    rim_lip_coordinates_right = [(rlxrs, rlyrs), (rlxre, rlyre)]

    # Coordinates of the "top" tyre (this can probably be cut down, but is somewhat easier to read)
    # tsxb = tire start x bottom, teyt = tire end y top
    tsxb = rsx
    tsyb = rsy
    texb = tsxb + tire_width_b
    teyb = rsy

    tsxt = rsx - (tire_width_t - rim_width) / 2
    tsyt = rsy - tire_height
    text = tsxt + tire_width_t
    teyt = tsyt

    tire_coordinates_top = [(tsxt, tsyt), (text, teyt), (texb, teyb), (tsxb, tsyb)]

    # Coordinates of the "bottom" tyre
    tsxb2 = rsx
    tsyb2 = rey
    texb2 = tsxb2 + tire_width_b
    teyb2 = rey

    tsxt2 = rsx - (tire_width_t - rim_width) / 2
    tsyt2 = rey + tire_height
    text2 = tsxt2 + tire_width_t
    teyt2 = tsyt2

    tire_coordinates_bottom = [(tsxt2, tsyt2), (text2, teyt2), (texb2, teyb2), (tsxb2, tsyb2)]

    # Set up image and draw object
    img = Image.new('RGB', (image_width, image_height), 'black')
    draw = ImageDraw.Draw(img)
    outline_width_relative = round((outline_width * image_dpi) / 16)

    # Draw the rim, tire, then rim lip
    draw.polygon(rim_coordinates, outline=outline_rim_color, width=outline_width_relative)
    draw.polygon(tire_coordinates_top, outline=outline_tire_color, width=outline_width_relative)
    draw.polygon(tire_coordinates_bottom, outline=outline_tire_color, width=outline_width_relative)
    draw.line(rim_lip_coordinates_left, fill=outline_rim_color, width=outline_width_relative)
    draw.line(rim_lip_coordinates_right, fill=outline_rim_color, width=outline_width_relative)

    # Text to display rim and tire size
    font = ImageFont.truetype(font, image_dpi)
    text_position = (10, 10)
    image_text = str(tire.rim_diameter_inch) + "x" + str(tire.rim_width_inch) + ", " + str(tire.tire_width_t_mm) + "/" + str(tire.tire_height_relative) + "R" + (str(tire.rim_diameter_inch))
    draw.text(text_position, image_text, fill=font_color, font=font)

    # Save the image
    filename_text = 'front_' + str(tire.rim_diameter_inch) + "x" + str(tire.rim_width_inch) + "_" + str(tire.tire_width_t_mm) + "_" + str(tire.tire_height_relative) + "R" + str(tire.rim_diameter_inch)
    img.save(os.path.join(subfolder, filename_text)  + '.png')
    img.save(os.path.join(subfolder, 'front_latest.png'))
    print ("Image saved as: ", filename_text + '.png and front_latest.png')

tire_baseline = Tire(17, 7.5, 205, 45, 1.5, 1)
tire_compare = Tire(17, 7.5, 205, 50, 1.5, 1)
compareTires([tire_baseline, tire_compare])
generateTireImageFront(tire_baseline)
generateTireImageSide(tire_baseline)
