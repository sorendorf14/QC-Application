# Output File Column Readme

## Standard Output Files 

### aaaYYYYMMq10.txt, aaaYYYYMMq1h.txt, aaaYYYYMMq3h.txt

First two rows are a header. q10 is 10-minute data, q1h is hourly data (taken at the top of the hour, with +/- 10 minutes (one observation)), q3h is three hourly data (taken at the top of every third hour (e.g., 00, 03), with +/- 40 minutes (4 observations) if the data are missing at the), 
1. year
2. julian day
3. month
4. day of the month
5. time (HHMM)
6. temperature (C)
7. pressure (hPa)
8. wind speed (m/s)
9. wind direction (degrees)
10. relative humidity (%)
11. delta T (C)

### aaaYYYYMMraw.txt
First seven rows are a header. Rows 2-7 detailed the data that have been previously QC'ed that has 2 columns and 7 (or 23 for tall tower) rows. The tall tower section details all the raw file information for tall tower. 
Header Explanation:
* 1st row: Abbreviated name, station ID, latitude, longitude, elevation, year, month, days of the month, number of observations, is RH included?, is delta T included?
* Rows 2-7: Column 1 - Manual QC Removal (not marked by the rules), Column 2 - Manual QC Removal from Rules for temperature (row 2), pressure (3), wind speed (4), wind direction (5), relative humidity (6), delta T (7).

Main data:
1. Date (YYYY-MM-DD)
2. Time (HH:MM:SS)
3. Year
4. Julian Day
5. Month
6. Day of the Month
7. Time (HHMM)
8. Quality Controlled Temperature (C)
9. Manually Removed Temperature
10. Manually removed temperature that was marked with the rules
11. Quality Controlled Pressure (hPa)
12. Manually Removed Pressure
13. Manually removed pressure that was marked with the rules
14. Quality Controlled Wind Speed (m/s)
15. Manually Removed Wind Speed
16. Manually removed wind speed that was marked with the rules
17. Quality Controlled Wind Direction (degrees)
18. Manually Removed Wind Direction
19. Manually removed wind direction that was marked with the rules
20. Quality Controlled Relative Humidity
21. Manually Removed Relative Humidity
22. Manually removed relative humidity that was marked with the rules
23. Quality Controlled Delta Temperature (C)
24. Manually Removed deltaT
25. Manually removed deltaT that was marked with the rules

### change log

### qc log

## Tall Tower Specific Output Files

All the files listed above will be output when saving tall tower data. The standard data files will include all of variables at one level - 4 meters. There are three extra files that are output when saving the tall tower data that include all variables at all levels.

### aaaYYYYMMq10_all.txt, aaaYYYYMMq1h_all.txt, and aaaYYYYMMq3h_all.txt
First two rows are a header. q10 is 10-minute data, q1h is hourly data (taken at the top of the hour, with +/- 10 minutes (one observation)), q3h is three hourly data (taken at the top of every third hour (e.g., 00, 03), with +/- 40 minutes (4 observations) if the data are missing at the top of the third hour)

1. year
2. julian day
3. month
4. day of the month
5. time (HHMM)
6. 1m temperature (C)
7. 2m temperature (C)
8. 4m temperature (C)
9. 7m temperature (C)
10. 15m temperature (C)
11. 30m temperature (C)
12. pressure (hPa)
13. 1m wind speed (m/s)
14. 2m wind speed (m/s)
15. 4m wind speed (m/s)
16. 7m wind speed (m/s)
17. 15m wind speed (m/s)
18. 30m wind speed (m/s)
19. 1m wind direction (degrees)
20. 2m wind direction (degrees)
21. 4m wind direction (degrees)
22. 7m wind direction (degrees)
23. 15m wind direction (degrees)
24. 30m wind direction (degrees)
25. 4m relative humidity (%)
26. 7m relative humidity (%)
27. 15m relative humidity (%)
28. 30m relative humidity (%)

### aaaYYYYMMraw.txt
First 24 rows are a header. Rows 2-24 detailed the data that have been previously QC'ed that has 2 columns 23 rows.

Header Explanation:
* 1st row: Abbreviated name, station ID, latitude, longitude, elevation, year, month, days of the month, number of observations, is RH included?, is delta T included?
* Rows 2-7: Column 1 - Manual QC Removal (not marked by the rules), Column 2 - Manual QC Removal from Rules for 1m temperature (row 2), 2m temperature (row 3), 4m temperature (row 4), 7m temperature (row 5), 15m temperature (row 6), 30m temperature (row 7), pressure (8), m wind speed (9), m wind speed (10), m wind speed (11), m wind speed (12), m wind speed (13), m wind speed (14), m wind direction (15), m wind direction (16), m wind direction (17), m wind direction (18), m wind direction (19), m wind direction (20), m relative humidity (21), m relative humidity (22),  m relative humidity (23), m relative humidity (24),

Main data:
1. Date (YYYY-MM-DD)
2. Time (HH:MM:SS)
3. Year
4. Julian Day
5. Month
6. Day of the Month
7. Time (HHMM)
8. Quality Controlled 1m Temperature (C)
9. Manually Removed 1m Temperature
10. Manually removed 1m temperature that was marked with the rules
11. Quality Controlled 2m Temperature (C)
12. Manually Removed 2m Temperature
13. Manually removed 2m temperature that was marked with the rules
14. Quality Controlled 4m Temperature (C)
15. Manually Removed 4m Temperature
16. Manually removed 4m temperature that was marked with the rules
17. Quality Controlled 7m Temperature (C)
18. Manually Removed 7m Temperature
19. Manually removed 7m temperature that was marked with the rules
20. Quality Controlled 15m Temperature (C)
21. Manually Removed 15m Temperature
22. Manually removed 15m temperature that was marked with the rules
23. Quality Controlled 30m Temperature (C)
24. Manually Removed 30m Temperature
25. Manually removed 30m temperature that was marked with the rules
26. Quality Controlled Pressure (hPa)
27. Manually Removed Pressure
28. Manually removed pressure that was marked with the rules
29. Quality Controlled 1m Wind Speed (m/s)
30. Manually Removed 1m Wind Speed
31. Manually removed 1m wind speed that was marked with the rules
32. Quality Controlled 2m Wind Speed (m/s)
30. Manually Removed 2m Wind Speed
31. Manually removed 2m wind speed that was marked with the rules
32. Quality Controlled 4m Wind Speed (m/s)
30. Manually Removed 4m Wind Speed
31. Manually removed 4m wind speed that was marked with the rules
32. Quality Controlled 7m Wind Speed (m/s)
30. Manually Removed 7m Wind Speed
31. Manually removed 7m wind speed that was marked with the rules
32. Quality Controlled 15m Wind Speed (m/s)
30. Manually Removed 15m Wind Speed
31. Manually removed 15m wind speed that was marked with the rules
32. Quality Controlled 30m Wind Speed (m/s)
33. Manually Removed 30m Wind Speed
34. Manually removed 30m wind speed that was marked with the rules
35. Quality Controlled 1m Wind Direction (degrees)
36. Manually Removed 1m Wind Direction
37. Manually removed 1m wind direction that was marked with the rules
38. Quality Controlled 2m Wind Direction (degrees)
39. Manually Removed 2m Wind Direction
40. Manually removed 2m wind direction that was marked with the rules
41. Quality Controlled 4m Wind Direction (degrees)
42. Manually Removed 4m Wind Direction
43. Manually removed 4m wind direction that was marked with the rules
44. Quality Controlled 7m Wind Direction (degrees)
45. Manually Removed 7m Wind Direction
46. Manually removed 7m wind direction that was marked with the rules
47. Quality Controlled 15m Wind Direction (degrees)
48. Manually Removed 15m Wind Direction
49. Manually removed 15m wind direction that was marked with the rules
50. Quality Controlled 30m Wind Direction (degrees)
51. Manually Removed 30m Wind Direction
52. Manually removed 30m wind direction that was marked with the rules
53. Quality Controlled 4m Relative Humidity
54. Manually Removed 4m Relative Humidity
55. Manually removed 4m relative humidity that was marked with the rules
56. Quality Controlled 7m Relative Humidity
57. Manually Removed 7m Relative Humidity
58. Manually removed 7m relative humidity that was marked with the rules
59. Quality Controlled 15m Relative Humidity
60. Manually Removed 15m Relative Humidity
61. Manually removed 15m relative humidity that was marked with the rules
62. Quality Controlled 30m Relative Humidity
63. Manually Removed 30m Relative Humidity
64. Manually removed 30m relative humidity that was marked with the rules
