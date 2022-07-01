from picamera import PiCamera

def take_picture(orbit_number, image_path, image_index):
    """
    Takes picture with Pi camera and saves it to the desired path

    param:
        orbit_number: number of the current orbit
        imagePath: path where the image should be saved
        image_index: index of image being taken

    return
        name: full path to the image taken including the image name
    """
    with PiCamera() as camera:
        name = image_path + '{}_{}.jpg'.format(orbit_number, index)
        # TO DO: change camera settings to make better pictures for each persons lighting conditions
        camera.capture(name, quality=75)

    return name
