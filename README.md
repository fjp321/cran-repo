# CRAN_package_creator
Creates directory of CRAN packages that are required for the package the user inputs, and saves all necessary files in this directory, as well as a txt file which prints any errors that the script ran into. 
Run the initialImports(userInput, location, version, kit) method to create the directory. 
The userInput argument is a string representation of the package that the user is looking for imports for. For example, if I am looking for imports for ggplot2, I would enter the first argument as "ggplot2".
The location argument is a string representation of where to create a directory where all the necessary imports are saved. For example, if I would like to save the import files to the c drive, I would enter this argument as "C:"
The version argument is a string representation of which version of R the user wants to use. For example, if I want R-version 3.5, I would enter "3.5" for this argument.
The kit argument is a string representation of which kit the user would like to get. There are 3 options; "devel", "release", or "oldrel".
