# Standard File Column Explainer of Input Files

Listing all the column names and other information for standard AWS files that do not have column names within the files

## .r files

The filenames of the data are set up as follows:  the first four digits are the ARGOS ID # of the unit, the next two are the month, followed by two more digits indicating the year.  All files have a .r extension.  So, a filename like 89060589.r would be data for site 8906 during May of 1989. If the file begins with a zero, i.e. 08965####.r, the ID# is actually only 4 digits, in this case, the ID# would really be 8965.

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

