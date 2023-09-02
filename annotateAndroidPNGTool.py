###################################################
#  This program is designed to process metadata   #
#  given by an xml in order to highlight where    #
#  leaf level GUI-components are in an Android    #
#  application screenshot.                        #
#                                                 #
#                                                 #
#   It does this by using the PIL library as well #
#   as the standard library modules pathlib and   #    
#   xml.etree.ElementTree (ET). I created two     #
#   helper functions, one recursive function to   #                                             
#   traverse the XML tree that was parsed by      #
#   functions in the ET library and one to find   #                                           
#   a file given a file name. This was to make    #
#   the code more readable and easier to manage.  #
#   The program finds the needed files indicated  #
#   by command line arguments, and parses the XML,#
#   in order to get a usuable list of pixel bounds#
#   of leaf node GUI components. Then, it uses PIL#
#   to load the png and draw an about 4-9 pixel   #
#   thick outline of the component. I made it 4-8 #
#   pixels thick in order for the outline to be   #
#   very obvious and visible. Then, the image is  #
#   saved with the same name as the original with #                                       
#   "_appended" before the .png. There is also    #
#   some error catching, such as if a file does   #
#   not exist and if the user does not have a     #
#   command argument in order to take into account#
#   user error and tell the user where their error#
#   is.                                           #
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
#-------------------------------------------------------
# Helper function to find the file given a fileName
#--------------------------------------------------------
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
     #check to see there is input
    if len(sys.argv) <2:
        print("ERROR : Program must have at least one command line argument")
        exit()
    #get the name of the app and set imagename and xmlName
    baseName=sys.argv[1] 
    #if there is more than one input to the command line then the second input is the screen #
    if len(sys.argv) >2 :
        baseName=baseName + "-" + sys.argv[2]
    imageName= baseName +".png"
    xmlName= baseName + ".xml"
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
            for y in range (int(currboundslist[0][1])-2, int(currboundslist[0][1])+2 ):
                if y<0:
                    y=0
                im.putpixel( (x,y), (225,156,53))
            for y in range (int(currboundslist[1][1])-2, int(currboundslist[1][1]) +2):
                if y >= im.height:
                    y=im.height-1
                im.putpixel( (x,y), (225,156,53))
        for y in range(int(currboundslist[0][1]), int(currboundslist[1][1])):
            for x in range (int(currboundslist[0][0]) -4, int(currboundslist[0][0]) +4):
                if x<0:
                    x=0
                im.putpixel( (x,y), (225,156,53))
            for x in range (int(currboundslist[1][0]) -4, int(currboundslist[1][0]) +4):
                #if the endBound is the width of the image, offset it by one pixel
                if x >= im.width:
                    x = im.width-1
                im.putpixel( (x,y), (225,156,53))
    #save the image
    im.save(imageName[0:-4] + "_annotated.png");


if __name__=="__main__":
    main()



        

