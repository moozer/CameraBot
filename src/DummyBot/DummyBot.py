#!/bin/env python
#
#
# Inspirational sites:
# - http://effbot.org/imagingbook/image.htm
# - http://www.linuxquestions.org/questions/programming-9/python-can-you-add-text-to-an-image-in-python-632773/


from PIL import Image
import ImageFont
import ImageDraw
        
class DummyBot(object):
    _IMAGESIZE = (512, 512)

    _CurrentDirection = [0,0] # neutral position
    _image = Image.new("RGB", _IMAGESIZE, "white")  # t
    _AcqFunction = None
    _EnableAcquisition = True # default is to acquire.
    
    @property
    def direction(self):
        return self._CurrentDirection
 
    def SetDirection(self, Direction ):
        # Sets the direction. 
        # (it is a design decision not to make it a "setter" - it is more explicit this way)
        
        # do nothing if not changing direction.
        if Direction == self._CurrentDirection:
            return 
        
        if(     ( Direction[0] > 1 or Direction[0] < -1 )
             or ( Direction[1] > 1 or Direction[1] < -1 ) ):
            raise ValueError( "Directions must be -1 <= 0 <= 1. Direction specified %s"%Direction)
        
        self._CurrentDirection = Direction
        
        if self._EnableAcquisition:
            self._GenerateImage()
            if self._AcqFunction:
                self._AcqFunction()
        pass
    
    def _GenerateImage(self):
        #self._image = Image.new("RGB", self._IMAGESIZE, "white")

        # local vars
        #FontSize = 14
        #font = "Verdana.ttf"
        text = str(self._CurrentDirection)
                
        #font_dir = "/usr/share/fonts/truetype/msttcorefonts/"
        #font_size = FontSize
        #fnt = ImageFont.truetype(font_dir+font, font_size)
        fnt = ImageFont.load_default()
        lineWidth = 20
        bg="#ffffff"
        
        img = Image.new("RGB", self._IMAGESIZE, "white")
        imgbg = Image.new('RGBA', img.size, "#000000") # make an entirely black image
        mask = Image.new('L',img.size,"#000000")       # make a mask that masks out all
        draw = ImageDraw.Draw(img)                     # setup to draw on the main image
        drawmask = ImageDraw.Draw(mask)                # setup to draw on the mask
        drawmask.line((0, lineWidth/2, img.size[0],lineWidth/2),
                      fill="#999999", width=10)        # draw a line on the mask to allow some bg through
        img.paste(imgbg, mask=mask)                    # put the (somewhat) transparent bg on the main
        draw.text((10,0), text, font=fnt, fill=bg)      # add some text to the main
        del draw 
        
        self._image = img
    
    @property
    def image(self):
        ''' return the latest image as a PIL.image object '''
        return self._image

    def EnableAcquisition(self, callbackFunction = None):
        self._AcqFunction = callbackFunction
        self._EnableAcquisition = True

    def DisableAcquisition(self):
        self._EnableAcquisition = False
    
    
    
