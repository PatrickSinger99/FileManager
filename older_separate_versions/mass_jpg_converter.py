import os
from PIL import Image
import shutil


def separator():
    print("_"*45)


formats = [".png", ".jpeg", ".bmp", ".webp"]

# Program start
print("Mass JPG Converter v1")
separator()

while True:
    while True:
        try:
            directory = input("Folder path: ")
            folder_content = os.listdir(directory)

            print("\nDetected files:")
            if len(folder_content) <= 5:
                for file in folder_content:
                    print("- " + file)
            else:
                print("- " + folder_content[0])
                print("- " + folder_content[1])
                print("- " + folder_content[2])
                print("- " + folder_content[3])
                print("- " + folder_content[4])
                print("+ " + str(len(folder_content) - 5) + " more...")

            separator()
            start_val = input("Start conversion? (y/n): ")
            if start_val.lower() == "y":
                print("\nConverting images...")
                break

            separator()

        except OSError:
            print("(!) Directory doesnt Exist\n")

    separator()

    # Create folder for original images
    try:
        os.mkdir(directory + r"\orignal_imgs")
    except FileExistsError:
        pass

    conv_files = 0
    for file in folder_content:

        # Check if file is convertable format
        is_conv_format = False
        for form in formats:
            if file.lower().endswith(form):
                is_conv_format = True

        # Convert image to .jpg
        if is_conv_format:
            img = Image.open(directory + "\\" + file)
            filename = os.path.splitext(img.filename)[0]
            img = img.convert("RGB")

            img.save(filename + "_convert.jpg", "JPEG", quality=95)
            conv_files += 1

            # Move original image to subfolder
            shutil.move(directory + "\\" + file, directory + r"\orignal_imgs")

    print("Conversion finished. " + str(conv_files) + " files converted.")

    input("\nPress any key to convert again")
    separator()
