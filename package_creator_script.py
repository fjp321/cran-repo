# -*- coding: utf-8 -*-
"""
Created on Mon May 20 22:07:01 2019

@author: finley Potter
"""

#import necessary libraries
from lxml import html
import requests
import os
import sys

def downloadZip(package, location, statusfile, version, kit):
    page = requests.get("https://cran.r-project.org/bin/windows/contrib/" + version)
    if page.status_code != 200:
        statusfile.write("\nincorrect, version does not exist")
        sys.exit(0)
    if kit == "devel":
        kit = 0
    elif kit == "oldrel":
        kit = 2
    else:
        kit = 1
    page = requests.get("https://cran.r-project.org/web/packages/" + package + "/index.html") #get html file where package dependencies are
    tree = html.fromstring(page.content)
    imports = tree.xpath("//tr/td[contains(text(),'Windows')]/../td[2]/a[@href]/text()") #get all packages that are linked, non-linked packages are outdated, 404, not necessary
    try:
        zipFile = requests.get('https://cran.r-project.org/bin/windows/contrib/' + version+ '/' + imports[kit])
        with open(location + "/" + imports[1], 'wb') as f:  
            f.write(zipFile.content)
            f.close()
        statusfile.write("\nFound correct kit for "+package)
    except IndexError:
        statusfile.write("\nDid not find correct kit for "+package+", manual help may be required")
        

def downloadAll(userInput, listOfPackages, whereToPutDir, statusfile, version, kit):
    # whereToPutDir =  "C:/Users/potte/Downloads/"#input("Where should the packages be saved? ")
    try:
        # Create target Directory
        os.mkdir(whereToPutDir + '/' + userInput + 'AndImports')
    except FileExistsError:
        statusfile.write("\nDirectory "+userInput+"AndImports already exists")
    except FileNotFoundError:
        statusfile.write("\nDirectory location "+whereToPutDir+" is not valid")
        sys.exit(0)
    for x in listOfPackages:
        downloadZip(x, whereToPutDir + '/' + userInput + 'AndImports', statusfile, version, kit)
    statusfile.write("\nDownload complete")
            
#function being recursively called
def getImports(package,listOfPackages,statusfile):
    inListAlready = False
    listOfPackages.append(package)
    page = requests.get("https://cran.r-project.org/web/packages/" + package + "/index.html") #get html file where package dependencies are
    tree = html.fromstring(page.content)
    imports = tree.xpath("//tr/td[contains(text(),'Imports')]/../td[2]/a[@href]/text()") #get all packages that are linked, non-linked packages are outdated, 404, not necessary
    if(len(imports) > len([])): # if no linkable packages
        for x in imports: 
            for y in listOfPackages:
                if x==y:
                    inListAlready = True
            if inListAlready == False:
                getImports(x,listOfPackages, statusfile) # run recursion
            inListAlready = False

def initialImports(userInput, location, version, kit):
    statusfile = open(location+"/status.txt","w")
    statusfile.write("Download Initialized\n\n")
    listOfPackages = []
    page = requests.get("https://cran.r-project.org/web/packages/" + userInput + "/index.html") #get html file where package dependencies are
    if page.status_code != 200:
        statusfile.write("\nError, something went wrong; Error "+page.status_code)
        sys.exit(0)
    tree = html.fromstring(page.content)
    isItInMainRepository = tree.xpath("//h1[contains(text(),'Object not found!')]")
    if(len(isItInMainRepository) != 0):
        statusfile.write("\nThis is not a package in the repository, sorry")     
        sys.exit(0)
    isItInMainRepository = tree.xpath("//p[contains(text(),'was removed from the CRAN repository')]")
    if(len(isItInMainRepository) != 0):
        statusfile.write("\nThis is not a package in the repository, sorry")
        sys.exit(0)
    getImports(userInput, listOfPackages, statusfile)
    statusfile.write("Packages to download:\n")    
    for x in listOfPackages:
        statusfile.write(x+"\n")
    downloadAll(userInput, listOfPackages, location, statusfile, version, kit)
    statusfile.close()

        
# C:/Users/potte/Downloads    
initialImports("ggplot2", "C:/Users/potte/Downloads", "3.5", "release")