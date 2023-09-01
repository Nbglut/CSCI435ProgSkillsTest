###################################################
#  This program is designed to process metadata   #
#  given by an xml in order to highlight where    #
#  leaf level GUI-components are in an Android    #
#  application screenshot.                        #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
#   CSCI 435 Programming Assignment 1             #
#   Nicolette Glut                                #
###################################################




#imports
from PIL import Image
from pathlib import Path
import xml.etree.ElementTree as ET
import sys

#-------------------------------------------------------
# Helper function to traverse the XML tree recursively
#--------------------------------------------------------

def traverseXML(root, bounds):
    num=0
    #if the node has no children, store bounds in a list called bounds
    for child in root:
        num=+1
        if child == None:
            bounds.append(root)
        else:
            traverseXML(child, bounds)
    if num==0:
        return bounds.append(root)

def findFile(fileName):
    root= Path(".")
    files=root.glob("**/*") #search current dir and all subdir
    for item in files:
        curritem=item.parts
        if curritem[-1] == fileName:
            return item
    print("The file " + fileName + " cannot be found")
    exit()



#---------------
#  MAIN
#---------------
def main():
    #get the name of the app and set imagename and xmlName
    imageName=sys.argv[1] +".png"
    xmlName= sys.argv[1] + ".xml"
    #find the paths
    imagePath=findFile(imageName)
    xmlName=findFile(xmlName)
    #read xml
    xmltree = ET.parse(xmlName)
    root=xmltree.getroot()
    bounds=[]
    #traverse the xml and get the bounds of the leaf nodes
    for child in root:
        traverseXML(child, bounds)
    #get image
    im=Image.open(imagePath)
    #for every set of bounds in the list of bounds
    for item in bounds:
        currbounds=item.attrib.get("bounds")
        currboundslisttemp= currbounds.split("[")
        currboundslist= [];
        tempboundslist= []
        #turn bounds into lists 
        for item2 in currboundslisttemp:
            if(item2 !=""):
                currboundslist.append(item2[:-1].split(","))
        #outline each leafnode
        for x in range(int(currboundslist[0][0]), int(currboundslist[1][0])):
            for y in range (int(currboundslist[0][1]) -5, int(currboundslist[0][1]) +5):
                im.putpixel( (x,y), (225,156,53))
            for y in range (int(currboundslist[1][1]) -5, int(currboundslist[1][1]) +5):
                if y >= im.height:
                    y=im.height-1
                im.putpixel( (x,y), (225,156,53))
        for y in range(int(currboundslist[0][1]), int(currboundslist[1][1])):
            for x in range (int(currboundslist[0][0]) -5, int(currboundslist[0][0]) +5):
                im.putpixel( (x,y), (225,156,53))
            for x in range (int(currboundslist[1][0]) -5, int(currboundslist[1][0]) +5):
                #if the endBound is the width of the image, offset it by one pixel
                if x >= im.width:
                    x = im.width-1
                im.putpixel( (x,y), (225,156,53))
    #save the image
    im.save(imageName[0:-4] + "_annotated.png");


if __name__=="__main__":
    main()



        

