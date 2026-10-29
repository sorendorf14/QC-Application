# Standard File Column Explainer of Input Files

Listing all the column names and other information for standard AWS files that do not have column names within the files

## .r files

The filenames of the data are set up as follows:  the first four digits are the ARGOS ID # of the unit, the next two are the month, followed by two more digits indicating the year.  All files have a .r extension.  So, a filename like 089000589.r would be data for site 8900 during May of 1989. If the file begins with a zero, i.e. 08900MMYY.r, the ID# is actually only 4 digits, in this case, the ID# would really be 8900.

The first two lines of the .r files are the header. The data are organized in ten minute intervals.  The data are also uncorrected; i.e., they still have bad data points. 

The columns are: 
1. julian day
2. ten minute interval marker - The ten minute interval marker is a number between 1 and 144 representing time; 1 is 00:00, 2 is 00:10, 3 is 00:20, 7 is 01:00, and 144 is 23:50.
3. temperature (degrees Celsius)
4. pressure (millibars)
5. wind speed (meters per second)
6. wind direction (meteorological degrees)  
7. humidity (percent)
8. vertical temperature difference (delta T; degrees Celsius)

All times listed are GMT and missing data are indicated as 444.0.  Wind directions listed are the direction the wind is blowing from, from 0 to 360 clockwise (thus 90 degrees is east, 180 is south and 270 is west).

## .10 files

The files have most of the same data as the .r files; however, there is panel temperature and voltage. These files are read in along with the .10 files to get panel temperature and voltage. The data are organized in ten minute intervals.  The data are also uncorrected; i.e., they still have bad data points. There are no headers in these files. 

The columns are: 
1. ID
2. julian day
3. time (hhmmss)
4. temperature (degrees Celsius)
5. panel temperature (degrees Celsius)
6. pressure (millibars)
7. wind direction (meteorological degrees) 
8. wind speed (meters per second)
10. humidity (percent)
11. voltage
12. col12
13. col13
14. col14
15. col15
