import cv2 as cv

# Variables
compute_size = (35, 35)
canny_thresholds = (80, 180)

# Image formats
valid_images = ["jpg", "webp", "png", "jpeg"]


# Resize the image and convert to grayscale
def reformat(image, size=compute_size):
    try:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    except cv.error:
        pass
    return cv.resize(image, size, interpolation=cv.INTER_AREA)


# Edge detection with Canny
def canny(image):
    return cv.Canny(image, canny_thresholds[0], canny_thresholds[1])


# Get canny edge detection as string from image
def get_canny_from_img(path):
    try:
        if path.split(".")[-1].lower() in valid_images:
            return_str = ""

            np_array = canny(reformat(cv.imread(path), (35, 35)))
            for row in np_array:
                for pixel in row:
                    if pixel == 255:
                        return_str += "1,"
                    else:
                        return_str += "0,"

            return_str = return_str[:-1]

            return return_str
    except:
        return "None"
