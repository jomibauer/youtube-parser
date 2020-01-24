youtube_parser readme
============================

to install all required python libraries, copy and paste this into your control panel:

pip3 install requests bs4 openpyxl

============================
—ADDING CHANNELS TO BE SCRAPED—

add the channel IDs (not channel names!) to the .txt file called channel_ids.  this text file should be located in the same 
folder as the python script. Each unique ID should be separated from the next with a new line.

============================
—EXCEL TEMPLATE—

the program creates an excel file based on the dimensions set in the template_maker script.  This script should also be located
in the same folder as our youtube_parser script.

If you want to change the dimensions of columns, change the numbers in the script.  The size of excel cells is based off an 
arbitrary unit of measurement called a ‘unit’ that varies in size depending on whether its measuring width or height.  trial 
and error is probably the best way to adjust the sizes of the columns and rows.

============================
-WHERE DOES THE OUTPUT GO?—

the excel file will be named after the date the day the file was run(e.g. Jan 17th, 2020).  Running the program multiple times 
per day will overwrite the older file from the same day.

The files will be saved into a directory named after the current month and year (e.g. Jan 2020) which will be saved in the 
current working directory.
