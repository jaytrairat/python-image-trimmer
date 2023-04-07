import os
import argparse
import yaml
from PIL import Image


def crop_image(image_path, crop_template):
    # Open the image file
    image = Image.open(image_path)

    # Crop the image
    cropped_image = image.crop(
        (
            crop_template["x"],
            crop_template["y"],
            crop_template["x"] + crop_template["width"],
            crop_template["y"] + crop_template["height"],
        )
    )

    return cropped_image


def crop_images(input_folder, output_folder, template_name):
    # Load the crop template from YAML file
    with open("crop_templates.yaml", "r") as f:
        templates = yaml.safe_load(f)

    # Check if the template exists
    if template_name not in templates:
        print(f"Error: template '{template_name}' not found, only supports: scb, kbank")
        return

    # Make the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all files in the input folder
    files = os.listdir(input_folder)

    # Check if any files are images
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    image_files = [
        f for f in files if os.path.splitext(f)[1].lower() in image_extensions
    ]

    if not image_files:
        print(f"Warning: no image files found in {input_folder}.")
        return

    # Loop over all image files in the input folder
    for filename in image_files:
        # Open the image file and crop it
        image_path = os.path.join(input_folder, filename)
        cropped_image = crop_image(image_path, templates[template_name])

        # Save the cropped image to the output folder
        output_path = os.path.join(output_folder, f"""{template_name}_{filename}""")
        cropped_image.save(output_path)


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Crop images.")
    parser.add_argument(
        "--input_folder", "-i", help="Input folder containing images to crop."
    )
    parser.add_argument(
        "--output_folder", "-o", help="Output folder to save cropped images."
    )
    parser.add_argument(
        "--template", "-t", required=True, help="Name of the crop template to use."
    )
    args = parser.parse_args()

    # Crop the images
    crop_images(args.input_folder, args.output_folder, args.template)
