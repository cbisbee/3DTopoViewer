from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import numpy
import math


print("Welcome to the TOPO Image processor")
print("Please type the file name of the TOPO image you would like to open")

inFileName = input()

print("\nOpening ", inFileName, " ...")

img = Image.open(inFileName).convert('L')
print(inFileName , " succesfully opened!")

print("\nNow converting image to greyscale")
#img.convert('L')
img.show()


pause = input("Press enter to enhance edges")

print("\nNow enhancing edges in TOPO image")
EdgeEnhancedImg = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
EdgeEnhancedImg.show()


print("\nNow applying convultion kernel to image")
pause = input("Press enter to begin Sobel x process")
SobelEdgeX = ImageFilter.Kernel((3,3),[-1,0,1,-1,0,1,-1,0,1],1)
TOPOSobelX = EdgeEnhancedImg.filter(SobelEdgeX)
print("Saving Sobel X image")
xWidth, xHeight = TOPOSobelX.size
sobXPix = TOPOSobelX.load()
for x in range(0, xWidth):
    for y in range(0, xHeight):
        if (sobXPix[x,y] < 100):
            sobXPix[x,y] = 0
TOPOSobelX.save('SobelX.jpg','jpeg')
TOPOSobelX.show()

pause = input("Press enter to begin Sobel y process")
SobelEdgeY = ImageFilter.Kernel((3,3),[-1,-1,-1,0,0,0,1,1,1],1)
TOPOSobelY = EdgeEnhancedImg.filter(SobelEdgeY)
print("Saving Sobel Y image")
yWidth, yHeight = TOPOSobelY.size
sobYPix = TOPOSobelY.load()
for x in range(0, yWidth):
    for y in range(0, yHeight):
        if (sobYPix[x,y] < 100):
            sobYPix[x,y] = 0
TOPOSobelY.save('SobelY.jpg','jpeg')
TOPOSobelY.show()


'''What if we ran non-maximal supression and our double-hystersis thresholding on the sobelx and y images?
could we get more precise SobelX and SobelY images that we could then use to get an overall edge magnitude on?'''


pause = input("Press enter to show created image")
width, height = img.size

#Now we need to create an overall Sobel Magnitude Image
SobMag = Image.new('L',(width,height))
XPixels = TOPOSobelX.load()
YPixels = TOPOSobelY.load()
MagPixels = SobMag.load();

suppressedMag = Image.new('L',(width,height))
suppressedPixels = suppressedMag.load()

#Magnitude image
for x in range(0,width):
    for y in range(0,height):
        MagPixels[x,y] = math.floor(math.sqrt(((XPixels[x,y])*(XPixels[x,y])) + ((YPixels[x,y]) * (YPixels[x,y]))))

#Non-maximal supression
for x in range(1,width - 1):
    for y in range(1,height - 1):
        yVal = YPixels[x,y]
        xVal = XPixels[x,y]
        if xVal == 0:
            theta = 0
        else:
            theta = (math.atan(yVal / xVal))*(180/math.pi)
        if theta >= 0 and theta <= 22.5:
            #Check (0,1) and (0,-1)
            if MagPixels[x,y] > MagPixels[x+1,y] and MagPixels[x,y] > MagPixels[x-1,y]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                suppressedPixels[x,y] = 0
        elif theta > 22.5 and theta <= 45:
            #Check (-1,1) and (1,-1)
            if MagPixels[x,y] > MagPixels[x-1,y+1] and MagPixels[x,y] > MagPixels[x+1,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 45 and theta <= 67.5:
            #check (-1,1) and (1,-1)
            if MagPixels[x,y] > MagPixels[x-1,y+1] and MagPixels[x,y] > MagPixels[x+1,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 67.5 and theta <= 90:
            #check (-1,0) and (1,0)
            if MagPixels[x,y] > MagPixels[x-1,y] and MagPixels[x,y] > MagPixels[x+1,y]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 90 and theta <= 112.5:
            #check (-1,0) and (1,0)
            if MagPixels[x,y] > MagPixels[x-1,y] and MagPixels[x,y] > MagPixels[x+1,y]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 112.5 and theta <= 135:
            #check (1,1) and (-1,-1)
            if MagPixels[x,y] > MagPixels[x+1,y+1] and MagPixels[x,y] > MagPixels[x-1,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 135 and theta <= 157.5:
            #check (1,1) and (-1,-1)
            if MagPixels[x,y] > MagPixels[x+1,y+1] and MagPixels[x,y] > MagPixels[x-1,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 157.5 and theta <= 180:
            #check (0,1) and (0,-1)
            if MagPixels[x,y] > MagPixels[x,y+1] and MagPixels[x,y] > MagPixels[x,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 180 and theta <= 202.5:
            #check (0,1) and (0,-1)
            if MagPixels[x,y] > MagPixels[x,y+1] and MagPixels[x,y] > MagPixels[x,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 202.5 and theta <= 225:
            #check (1,1) and (1,-1)
            if MagPixels[x,y] > MagPixels[x+1,y+1] and MagPixels[x,y] > MagPixels[x+1,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 225 and theta <= 247.5:
            #check (1,1) and (1,-1)
            if MagPixels[x,y] > MagPixels[x+1,y+1] and MagPixels[x,y] > MagPixels[x+1,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 247.5 and theta <= 270:
            #check (-1,0) and (1,0)
            if MagPixels[x,y] > MagPixels[x-1,y] and MagPixels[x,y] > MagPixels[x+1,y]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 270 and theta <= 292.5:
            #check (-1,0) and (1,0)
            if MagPixels[x,y] > MagPixels[x-1,y] and MagPixels[x,y] > MagPixels[x+1,y]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 292.5 and theta <= 315:
            #check (1,1) and (-1,-1)
            if MagPixels[x,y] > MagPixels[x+1,y+1] and MagPixels[x,y] > MagPixels[x-1,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        elif theta > 315 and theta <= 337.5:
            #check (1,1) and (-1,-1)
            if MagPixels[x,y] > MagPixels[x+1,y+1] and MagPixels[x,y] > MagPixels[x-1,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        else:
            #check (0,1) and (0,-1)
            if MagPixels[x,y] > MagPixels[x,y+1] and MagPixels[x,y] > MagPixels[x,y-1]:
                MagPixels[x,y] = MagPixels[x,y]
            else:
                MagPixels[x,y] = 0
        #print(theta)

suppressedMag.save('SuprMag.jpg','jpeg')


SobMag.save('Mag.jpg','jpeg')

SobMag.show()


#Now we need to apply the Canny Edge Detector
