from PIL import Image, ImageDraw, ImageFont
import json

class Tire:
    def __init__(self, rim_diameter_inch = 17, rim_width_inch = 7.5, tire_width_mm = 205, tire_height_relative = 45, rim_diameter_additional = 0, rim_width_additional = 1):
        self.rim_diameter_inch = rim_diameter_inch
        self.rim_width_inch = rim_width_inch
        self.tire_width_mm = tire_width_mm
        self.tire_height_relative = tire_height_relative
        self.rim_diameter_additional = rim_diameter_additional
        self.rim_width_additional = rim_width_additional

def compareTires(tires):
    if not all(isinstance(tire, Tire) for tire in tires):
        raise TypeError('All elements in the list must be Tire objects')
    
    # Set the base tire to the first tire in the list
    base_tire = tires[0]

    # Base tire properties
    base_tire_diameter_mm = round((base_tire.rim_diameter_inch * 25.4) + ((base_tire.tire_width_mm * (base_tire.tire_height_relative / 100)) * 2), 2)
    base_tire_circumference_mm = round(base_tire_diameter_mm * 3.14159265359, 2)
    tire_speedometer_difference_percent = 0
    base_tire_reading_50kmh = 50
    base_tire_reading_100kmh = 100
    base_tire_ride_height_difference = 0

    # Add the base tire to the comparison list
    base_tire_dict = {
        'tire': str(base_tire.rim_diameter_inch) + "x" + str(base_tire.rim_width_inch) + ", " + str(base_tire.tire_width_mm) + "/" + str(base_tire.tire_height_relative) + "R" + (str(base_tire.rim_diameter_inch)),
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
        tire_diameter_mm = round((tire.rim_diameter_inch * 25.4) + ((tire.tire_width_mm * (tire.tire_height_relative / 100)) * 2), 2)
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
            'tire': str(tire.rim_diameter_inch) + "x" + str(tire.rim_width_inch) + ", " + str(tire.tire_width_mm) + "/" + str(tire.tire_height_relative) + "R" + (str(tire.rim_diameter_inch)),
            'diameter_mm': tire_diameter_mm,
            'circumference_mm': tire_circumference_mm,
            'speedometer_difference_percent': tire_speedometer_difference_percent,
            'reading_50kmh': tire_reading_50kmh,
            'reading_100kmh': tire_reading_100kmh,
            'ride_height_difference_mm': tire_ride_height_difference
        }

        comparison.append(tire_dict)

    # Save the tire comparisons to a JSON file
    with open('comparison.json', 'w') as output_file:
        json.dump(comparison, output_file, indent=4)

    return

def generateTireImage(tire):
    if not isinstance(tire, Tire):
        raise TypeError('Expected a Tire object')
    
    # Image settings
    image_width = 500
    image_height = 500
    image_dpi = 16
    outline_width = 2
    outline_rim_color = 'white'
    outline_tire_color = 'red'
    font_color = 'red'

    # Convert rim size in inches to pixels
    rim_diameter = (tire.rim_diameter_inch) * image_dpi
    rim_diameter_lip = (tire.rim_diameter_additional * image_dpi)
    rim_width = (tire.rim_width_inch + tire.rim_width_additional) * image_dpi

    # Convert tire size in inches to pixels
    tire_width_inch = tire.tire_width_mm / 25.4
    tire_width_t = tire_width_inch * image_dpi # top tire width is th
    tire_width_b = rim_width # bottom tire width is the same as rim width due to seating

    # Calculate difference between top and bottom tire width, to get a relative height using sidewall length
    tire_area = tire_width_t * (tire_width_t * (tire.tire_height_relative / 100))
    average_width = (tire_width_t + tire_width_b) / 2
    tire_height = tire_area / average_width

    print("Rim diameter: ", rim_diameter)
    print("Rim width: ", rim_width)
    print("Tire width: ", tire_width_t, tire_width_b)
    print("Tire height: ", tire_height)

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
    font = ImageFont.truetype("arial.ttf", image_dpi)
    text_position = (10, 10)
    image_text = str(tire.rim_diameter_inch) + "x" + str(tire.rim_width_inch) + ", " + str(tire.tire_width_mm) + "/" + str(tire.tire_height_relative) + "R" + (str(tire.rim_diameter_inch))
    draw.text(text_position, image_text, fill=font_color, font=font)

    # Save the image
    filename_text = str(tire.rim_diameter_inch) + "x" + str(tire.rim_width_inch) + "_" + str(tire.tire_width_mm) + "_" + str(tire.tire_height_relative) + "R" + str(tire.rim_diameter_inch)
    img.save(filename_text  + '.png')
    img.save('latest.png')
    print ("Image saved as: ", filename_text + '.png and latest.png')

tire_baseline = Tire(17, 7.5, 205, 45, 1.5, 1)
tire_compare = Tire(17, 7.5, 180, 60, 1.5, 1)
tire_compare_2 = Tire(17, 7.5, 180, 40, 1.5, 1)
compareTires([tire_baseline, tire_compare, tire_compare_2])
#generateTireImage(tire)