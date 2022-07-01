    
    # Order of Operations for this part of the code: (1) Sharpen the RGBWB image (called new_image + a time 
    # string) (2) Split that image into three images (3) Take the red one, find the edges on it, and save it (4) 
    # Take that image and remove all non-red pixels, and rewrite it over a blank image and save it (5) Take THAT 
    # image and de-noise--remove all pixels where 3 out of 4 of the surrounding pixels are not red, and save it 
    # ----------- future additions: ------------ (6) Determine squares (7) Enumerate squares (8) Count squares
                                   
def test(): img =Image.open('new_image.jpg').convert("RGB") size = img.size
    # Sharpen the image
    enhancer = ImageEnhance.Sharpness(img) factor = 2 img_s_1 = enhancer.enhance(factor) 
    img_s_1.save('sharpened-image_' + fname + '.jpg')
    
    img2 = Image.open('sharpened-image_' + fname + '.jpg') data = img2.load()
    
    overwrite = Image.open('blank_image.jpg') for x in range(img2.width): for y in range(img2.height): if 
            data[x, y] == (255, 255, 255):
                overwrite.putpixel((x, y), (0, 0, 0))
    
    overwrite.save('black_and_white_' + fname + '.jpg')
    
    
    
      
    
def color_id_2():
            
    # Taking the image and saving it as three seperate images, one for each color NOTE: the colors are a 
    # somewhat messed up, but what matters is the edges that begin to show up in the image
    img2 = Image.open('sharpened-image.jpg').convert("RGB") DATA = img2.getdata() r = [(d[0], 0, 0) for d in 
    DATA] g = [(0, d[1], 0) for d in DATA] b = [(0, 0, d[2]) for d in DATA] img.putdata(r) 
    img.save('only_red.jpg') img.putdata(g) img.save('only_green.jpg') img.putdata(b) img.save('only_blue.jpg')
    # Find the edges by applying the filter ImageFilter.FIND_EDGES, and then sharpening the image. The purpose 
    # of this is to make a black image with the outlines of the plastic pieces on them
    image = Image.open("only_red.jpg") ImageWithEdges = image.filter(ImageFilter.FIND_EDGES) data = 
    ImageWithEdges.load() ImageWithEdges.save('ImageWithEdges_' + fname + '.jpg')
    
    # Open the blank image again
    empty = Image.open('blank_image.jpg')
    
    # Take the image with edges and make it clearer for x in range(img.width):
     #   for y in range(img.height):
      #      new_color = red_filter(data[x, y][0], data[x, y][1], data[x, y][2])
       #     if new_color == (255, 0, 0):
        #        empty.putpixel((x,y), new_color)
    string = 'empty_' + fname + '.jpg' empty.save(string)
    
    # Take the Image with edges and get rid of extra pixels
    final_image = Image.open('ImageWithEdges_' + fname + '.jpg')
    
    X = Image.open(string) data = X.load() for x in range(1, img.width-1): for y in range(1, img.height-1):
            
            # the following "if" statements are kinda messy, if anyone has ideas on how to make them either more 
            # simple/elegant or faster, let me know Its intended purpose is to see if 3 out of 4 (or all 4) of 
            # the surrounding pixels are not red, and if so, turn that pixel black as well.
            
            # FOR TESTING: if the above loop is un-commented, change the (0, 0, 0)'s to (255, 0, 0), and the 
            # '==' to '!='
            if data[x-1, y] == (0, 0, 0) and data[x+1, y] == (0, 0, 0) and data[x, y-1] == (0, 0, 0): 
                final_image.putpixel((x, y), (0, 0, 0))
            elif data[x+1, y] == (0, 0, 0) and data[x, y-1] == (0, 0, 0) and data[x, y+1] == (0, 0, 0): 
                final_image.putpixel((x, y), (0, 0, 0))
            elif data[x-1, y] == (0, 0, 0) and data[x+1, y] == (0, 0, 0) and data[x, y+1] == (0, 0, 0): 
                final_image.putpixel((x, y), (0, 0, 0))
            elif data[x-1, y] == (0, 0, 0) and data[x, y-1] == (0, 0, 0) and data[x, y+1] == (0, 0, 0): 
                final_image.putpixel((x, y), (0, 0, 0))
     
    final_image.save('final_image_' + fname + '.jpg')
