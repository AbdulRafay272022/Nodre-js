import numpy as np
import matplotlib.pyplot as plt

# Specify the image path
image_path = r'C:\Users\Lenovo\Downloads\allfiles\image1.jpg'#r'C:\Users\Lenovo\Desktop\Python Code\ML\Screenshot 2024-02-17 154048.png'
image_path_1= r'C:\Users\Lenovo\Downloads\allfiles\image2.jpg'#r'C:\Users\Lenovo\Desktop\Python Code\ML\Screenshot 2024-02-19 131540.png'
image_path_2= r'C:\Users\Lenovo\Downloads\allfiles\image3.jpg'

def binarize(img, threshold):
    # create an image with True or False (that can be seen as 1 or 0) and multiply by 255
    binaryimg = (img > threshold).astype(int) * 255
    #print(binaryimg)
    return binaryimg #return binary image ,more than threshold 1 *255 else 0*255
    

def comparison(img1, img2):
    # convert to gray. What's the filter doing?
    gray1 = rgb2gray(img1)
    gray2 = rgb2gray(img2)
 

    # Calculate histograms of pixel intensities
    histogram_gray1, bins_gray1 = np.histogram(gray1.flatten(), bins=256, range=(0, 256))
    histogram_gray2, bins_gray2 = np.histogram(gray2.flatten(), bins=256, range=(0, 256))

    # Plot histograms
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(histogram_gray1, color='black')
    plt.title('Histogram of Gray1')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    plt.plot(histogram_gray2, color='black')
    plt.title('Histogram of Gray2')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()


    # select a threhsold value and binarize the image
    threshold = 0.6
    gray1_bin = binarize(gray1, threshold)
    gray2_bin = binarize(gray2, threshold)
    
    # in python you can compute a difference image.
    # so diff will contain in each pixel the difference between the two images
    diff = gray1_bin - gray2_bin
    print(np.mean(gray1_bin),np.mean(gray2_bin))
    # the np.mean gives you already sum / number of pixels
    average = np.mean(diff)

    return average

def rgb2gray(col_img):
    # converts images to gray
    weights = np.array([0.3, 0.59, 0.11])
    gray = np.sum([col_img[:, :, i].astype(np.float64) * weights[i] for i in range(3)], axis=0)
    return gray

# the "main" method
if __name__ == "__main__":
    # read the images
    img = plt.imread(image_path_1)
    img2 = plt.imread(image_path_2)
    result = comparison(img, img2)

    print("The difference between the images is {}".format(result))
