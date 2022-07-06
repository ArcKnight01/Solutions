# IMPORTS
import cv2
import numpy as np

from PIL import Image
import PIL
import os
import glob

#Script for determining the percentage of each color using PIL and using
#RGB representation. When running in the command line, type the image file. Type
#True if you want to see the image after the filters are applied

def get_mask(image, lower_bound, upper_bound):
    """
    Get a mask of where the image corresponds to each color
    param:
        image = array of rbg values for the image
        lower_bound = lower end of range for color 
        upper_bound = upper end of range for color 
    
    return:
        masked_image = image combined with the mask
    """
    threshold = cv2.inRange(image, lower_bound, upper_bound) # returns boolean array of pixels in threshold
    # cv2.bitwise_and(first array, second array, destination array, mask operation to perform)
    mask = cv2.bitwise_and(image, image, mask=threshold)
    masked_image = cv2.bitwise_and(image, mask)
    return threshold, mask, masked_image


def part_1(image):
    """
    Get a mask of where the image corresponds to each color
    param:
        image = array of rbg values for the image
    
    return:
        color_range = ranges used for each color (RGB)
        perc_*COLOR* = percentage of pixels in image that correspond to this color
    """

    color_range = {}
    #Figure out what the lower and upper bounds for each color should be
    color_range["blue"] = [(255, 0, 0), (255, 255, 0)]
    color_range["green"] = [(0, 255, 0), (100, 255, 100)]
    color_range["red"] = [(0, 0, 200), (75, 75, 255)]
    
    #Counter for amount of pixels of each color
    color_amount = {"red":0, "green":0, "blue":0}
        
    #PART 1: COLOR IDENTIFICATION
    #<YOUR CODE GOES HERE>
    # get masks and thresholds for each of the color ranges
    blue_th, blue_mask, blue_mask_im = get_mask(image, *color_range['blue'])
    green_th, green_mask, green_mask_im = get_mask(image, *color_range['green'])
    red_th, red_mask, red_mask_im = get_mask(image, *color_range['red'])
    
    # count the pixels in each of the thresholds
    color_amount["red"] = (np.sum(red_th))/255
    #print(color_amount["red"])
    color_amount["green"] = (np.sum(green_th))/255
    #print(color_amount["green"])
    color_amount["blue"] = (np.sum(blue_th))/255
    #print(color_amount["blue"])
    
    # calculate percentage of each color in the image
    total_pixels = image.shape[0] * image.shape[1]
    #total_pixels = color_amount["red"] + color_amount["green"] + color_amount["blue"]
    print(total_pixels)
    perc_red = color_amount["red"] / total_pixels
    perc_green = color_amount["green"] / total_pixels
    perc_blue = color_amount["blue"] / total_pixels
    
    return (color_range, perc_blue, perc_green, perc_red)


def part_2(image, image_HSV):
    '''
    enhance the image
    param:
        image = array of rbg values for the image
        image_HSV = array of HSV values for the image
    
    return:
        enhanced_image = enhanced image array
    '''
    #PART 2 TODO: Increase saturation, contrast, brightness, etc
    #<YOUR CODE GOES HERE>
    # Change saturation - add constant to S column in HSV image
    saturation_change = 20
    s = image_HSV[:,:,1] 
    snew = cv2.add(s, saturation_change)

    # Change contrast - multiply pixel by constant (in H column) keep below 255
    contrast_change = 5
    h = image_HSV[:,:,0]
    hnew = cv2.add(h, contrast_change)

    # Change brightness - add constant value to all pixels (in H column) keep below 255
    brightness_change = 20
    v = image_HSV[:,:,2]
    vnew = cv2.add(v, brightness_change)
    
    hsvnew = cv2.merge([hnew,snew,vnew])
    enhanced_image = cv2.cvtColor(hsvnew, cv2.COLOR_HSV2BGR)
    return enhanced_image

    
    
#Main code that is being run
def color_id(image_file = 'test.jpg', show = False):
    """
    Get a mask of where the image corresponds to each color
    param:
        image_file = filename of image to process
        show = boolean indicating if the image should be shown or saved (nominally False)
    
    return:
        enhanced_image = enhanced image array
    """
    folder_path = '' #Replace with the folder path for the folder in the
                     #Flat Sat Challenge with your name so you can view images
                     #on Github if you don't have VNC/X forwarding


    #images_path = r"~/Labs2/Imaging/Images/" + image_file
    image = cv2.imread(image_file) #Converts image to numpy array in BGR format
    if image is None:
        print("Image not loaded properly")
    image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #Converts BGR image to HSV format
    
    color_range, perc_blue, perc_green, perc_red = part_1(image) # run part 1 function 
    
    print("The percentage of red is",round(100*perc_red,2),"%")
    print("The percentage of green is",round(100*perc_green,2),"%")
    print("The percentage of blue is",round(100*perc_blue,2),"%")
    

    blue_th, blue_mask, blue_mask_im = get_mask(image, *color_range['blue'])
    green_th, green_mask, green_mask_im = get_mask(image, *color_range['green'])
    red_th, red_mask, red_mask_im = get_mask(image, *color_range['red'])
    
    #If the show flag is set to true, this will set up images to visualize the color ID.
    #Note: if you're on a windows machine and haven't set up X11 forwarding, 
    #this won't work. If show is set to False, the image masks will be stored to
    #the images/ folder
    if show:
        cv2.imshow('Blue Mask', blue_mask_im)
        cv2.imshow('Green Mask', green_mask_im)
        cv2.imshow('Red Mask', red_mask_im)
        
        cv2.waitKey()
        cv2.destroyAllWindows()
    else: # save to desired folder if you can't display them
        cv2.imwrite(folder_path + '/blue_mask.jpg', blue_mask_im)
        cv2.imwrite(folder_path + '/green_mask.jpg', green_mask_im)
        cv2.imwrite(folder_path + '/red_mask.jpg', red_mask_im)
        print('Image masks saved')
    
    #Uncomment when you want to work on part 2
    enhanced_image = part_2(image, image_HSV)
    
    #Shows orginal image and enhanced image
    if show:
        cv2.imshow('Original Image', image) 
        cv2.imshow('Enhanced Image', enhanced_image) 
        
        cv2.waitKey()
        cv2.destroyAllWindows()
    else:
        cv2.imwrite(folder_path + '/enhanced_image.jpg', enhanced_image)
        print('Enhanced image saved')
    

""" This code is for command line entry. It allows you to add arguments 
    for what you want the code to run on. For instance, if I want to run 
    it on an image called "test1.jpg" with visualizations on, I would 
    type python3 color_id.py test1.jpg True
"""
if __name__ == '__main__':
    import sys
    
    color_id(*sys.argv[1:])
