import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import os

# Specify the image path
image_path_1 = r'C:\Users\Lenovo\Downloads\allfiles\image1.jpg'
image_path_2 = r'C:\Users\Lenovo\Downloads\allfiles\image2.jpg'
image_path_3= r'C:\Users\Lenovo\Downloads\allfiles\image3.jpg'
image_path_4= r'C:\Users\Lenovo\Downloads\allfiles\image4.jpeg'
image_path_5= r'C:\Users\Lenovo\Downloads\allfiles2\image5.jpeg'
image_path_6= r'C:\Users\Lenovo\Downloads\allfiles\image6.jpg'
image_path_7= r'C:\Users\Lenovo\Downloads\allfiles\image7.jpeg'
def comparison(img1, img2):
    # Resize images to a smaller size
    img1_resized = cv2.resize(img1, (0, 0), fx=0.2, fy=0.2)  # Resize to 50% of the original size
    img2_resized = cv2.resize(img2, (0, 0), fx=0.2, fy=0.2)
    # convert to gray
    gray1 = cv2.cvtColor(img1_resized, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_RGB2GRAY)

    # Apply Otsu's thresholding
    _, img_binary_otsu_1 = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, img_binary_otsu_2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Display the binarized images
    #cv2.imshow('Otsu Binarization 1', img_binary_otsu_1)
    #cv2.imshow('Otsu Binarization 2', img_binary_otsu_2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Calculate the difference
    diff = img_binary_otsu_1 - img_binary_otsu_2
    average = np.mean(diff)

    return average
start_time = time.time()
# Load the images
img1 = cv2.imread(image_path_5)
folder_path=r'C:\Users\Lenovo\Downloads\allfiles'
files_in_folder = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
#print(files_in_folder)
for image_path in files_in_folder:
    img2 = cv2.imread(image_path)
    # Perform comparison
    result = comparison(img1, img2)

    print("The difference between the images {} is {}".format(image_path,result))

# Your code snippet here

end_time = time.time()
execution_time = end_time - start_time

print(f"The execution_time is {execution_time}")


