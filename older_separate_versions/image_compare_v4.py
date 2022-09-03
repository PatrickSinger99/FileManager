"""Image Compare v4"""
import numpy as np
import cv2 as cv
import os
import time

# Variables
compute_size = (400, 400)
canny_thresholds = (80, 180)
compare_size = 15  # (Under 15 accuracy starts to deteriorate)
skip_col = True  # Skip match if both images have "Col" in the name

# Image Formats
valid_images = [".jpg", ".webp", ".png"]


# Resize the Image and convert to grayscale
def reformat(image, size=compute_size):
    try:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    except cv.error:
        pass
    return cv.resize(image, size, interpolation=cv.INTER_AREA)


# Edge Detection with Canny
def canny(image):
    return cv.Canny(image, canny_thresholds[0], canny_thresholds[1])


# Edge Comparison with improved accuracy
def edge_compare_v2(image_1, image_2):
    prep_1 = image_1
    prep_2 = image_2

    hit = 0
    miss_1 = 0
    miss_2 = 0

    for i in range(compare_size):
        for j in range(compare_size):
            if prep_1[i, j] == 255:
                if prep_2[i, j] == 255:
                    hit += 1
                else:
                    miss_1 += 1
            elif prep_2[i, j] == 255:
                miss_2 += 1

    base_1_score = hit / (hit+miss_1)
    base_2_score = hit / (hit+miss_2)

    return (base_1_score + base_2_score) / 2


# Enter Directory
print("Welcome to Image-Compare v4 !")
print("-----------------------------")
print("Compare size: " + str(compare_size))
print("Skip \"Col\" images: " + str(skip_col))
print("-----------------------------\n")
while True:
    try:
        directory = input("Input directory of images: ")
        print("\nLoading images...")
        start = time.perf_counter()

        # Get Images
        images = []
        for img in os.listdir(directory):
            ext = os.path.splitext(img)[1]
            if ext.lower() in valid_images:
                try:
                    if cv.imread(directory + "\\" + img).shape[2] == 3:
                        images.append([img, canny(reformat(cv.imread(directory + "\\" + img),
                                                           (compare_size, compare_size)))])
                    else:
                        print("(i) Image \"" + img + "\" has incompatible number of channels (Will be skipped)")
                except:
                    print("(!) Could not read image \"" + img + "\" (Will be skipped)")

        if len(images) > 0:
            print("\n" + str(len(images)) + " image(s) loaded from directory. Beginning comparison now\n")
            break
        else:
            print("\n(!) No images found in this directory")

    except FileNotFoundError or OSError:
        print("\n(!) Directory could not be found\n")

# Calculate combinations
combs = 0
for i in range(len(images)):
    for j in range(i+1, len(images)):
        combs += 1

# Compare every Image
iteration = 0
comparisons = []   # [[img 1 name, img 2 name],[img 1 data, img 2 data], similarity score]
for i in range(len(images)):
    for j in range(i+1, len(images)):
        img_1 = images[i]
        img_2 = images[j]
        iteration += 1

        info_text = "Comparing \"" + os.path.splitext(img_1[0])[0] + "\" and \"" + os.path.splitext(img_2[0])[0] + "\""

        if len(info_text) >= 46:
            info_text = info_text[0:46] + "..."
        print(info_text + (" "*(50-len(info_text))) + "[" + str(iteration) + "/" + str(combs) + "] ", end="")

        similarity = edge_compare_v2(img_1[1], img_2[1])

        if similarity >= .6:
            print("- finished. " + str(int(round(similarity, 2)*100)) + "% Similar!")

            if skip_col is True and "Col" in img_1[0] and "Col" in img_2[0]:
                pass
            else:
                comparisons.append([[img_1[0], img_2[0]], [img_1[1], img_2[1]], similarity])

        else:
            print("- finished.")


# Debug Timer
stop = time.perf_counter()
print("\nComputing time: " + str(round(stop-start, 1)) + " sek")

print("\nComparison finished. Displaying matches now.\n")

# Print matches
num_of_matches = 0
for comparison in comparisons:
    num_of_matches += 1
    print("Edge-Similarity of", str(int(round(comparison[2], 2)*100)) +
          "% between", comparison[0][0], "and", comparison[0][1])


# Display matches
if num_of_matches > 0:
    choice = input("\nDo you want to compare " + str(num_of_matches) + " match(es) in detail? [y,n]: ")
    if choice.lower() == "y":
        review_num = 0
        print("")

        for comparison in comparisons:
            no_img_1, no_img_2 = False, False
            review_num += 1
            print("Reviewing Match", review_num, "of", num_of_matches)

            input_img_1 = cv.imread(directory + "\\" + comparison[0][0])
            if input_img_1 is None:
                input_img_1 = np.zeros((400, 400, 3), np.uint8)
                input_img_1 = cv.putText(input_img_1, "Image could not be found", (90, 195),
                                         cv.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
                no_img_1 = True

            input_img_2 = cv.imread(directory + "\\" + comparison[0][1])
            if input_img_2 is None:
                input_img_2 = np.zeros((400, 400, 3), np.uint8)
                input_img_2 = cv.putText(input_img_2, "Image could not be found", (90, 195),
                                         cv.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
                no_img_2 = True

            # Image 1 Text
            img_1 = cv.putText(cv.resize(input_img_1, compute_size, interpolation=cv.INTER_AREA),
                               comparison[0][0], (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, 0, 7)
            img_1 = cv.putText(img_1, comparison[0][0], (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if not no_img_1:
                size = str(input_img_1.shape[0]) + "x" + str(input_img_1.shape[1])
                img_1 = cv.putText(img_1, size, (10, 80), cv.FONT_HERSHEY_SIMPLEX, .5, 0, 5)
                img_1 = cv.putText(img_1, size, (10, 80), cv.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)

            # Image 2 Text
            img_2 = cv.putText(cv.resize(input_img_2, compute_size, interpolation=cv.INTER_AREA),
                               comparison[0][1], (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, 0, 7)
            img_2 = cv.putText(img_2, comparison[0][1], (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if not no_img_2:
                size = str(input_img_2.shape[0]) + "x" + str(input_img_2.shape[1])
                img_2 = cv.putText(img_2, size, (10, 80), cv.FONT_HERSHEY_SIMPLEX, .5, 0, 5)
                img_2 = cv.putText(img_2, size, (10, 80), cv.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)

            # Combined Image Text
            concat_img = np.concatenate((img_1, img_2), axis=1)
            concat_img = cv.putText(concat_img, "Edge-Similarity: " + str(int(round(comparison[2], 2)*100)) + "%",
                                    (220, 390), cv.FONT_HERSHEY_SIMPLEX, 1, 0, 7)
            concat_img = cv.putText(concat_img, "Edge-Similarity: " + str(int(round(comparison[2], 2)*100)) + "%",
                                    (220, 390), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv.imshow("Edge-Similarity match review", concat_img)
            cv.waitKey(0)

        closing_img = np.zeros((400, 800, 3), np.uint8)
        closing_img = cv.putText(closing_img, "All images compared. Window can be closed.",
                                 (220, 195), cv.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
        cv.imshow("Edge-Similarity match review", closing_img)
        cv.waitKey(0)

else:
    print("\nNo matches found.")

print("\nClosing Program...")
