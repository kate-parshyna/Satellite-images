#Description
The programm takes the coordinates from the csv file, then get the images of the territory according to the coordinates and in the nearest radius (the radius can be changed). 

Then on images, program detects houses using Microsoft Cognitive Services. After that, those parts of the image on which houses were found are converted into coordinates. These coordinates are saved in a output csv file. 

#Usage
This command is required to run the program:

````
python3 main.py --csv path/to/csv/file 

````

This arguments can be used also:
````
--number - number of areas around a given coordinate, default = 1
--zoom   - mileage, default = 0.001
--tile_size
--image_size

````
#Example
````
python3 main.py --csv input/coordinates.csv --number 2

````