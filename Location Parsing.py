import csv
from math import radians, cos, sin, asin, sqrt

## Import ##
with open('history-12-31-2013 EDIT.xml', 'r') as f:
    locations = [line.strip() for line in f]

# Tag Specification
whenTagOpen = "<when>"
whenTagClosed = "</when>"
coordTagOpen = "<coordinates>"
coordTagClosed = "</coordinates>"

#Lists
DateList = []
TimeList = []
LatList = []
LonList = []


# Find Between Functions
def find_between(s,first,last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last,start)
        return s[start:end]
    except ValueError:
        return ""

def find_between_r(s,first,last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last,start)
        return s[start:end]
    except ValueError:
        return ""

## Export ##
with open('locations.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Date'] + ['Time'] + ['Latitude'] + ['Longitude'])
    # Reads String and Parses Text as Variables
    for i in range (len(locations)):
            currentLine = locations[i]
        
            #Date and Time
            if whenTagOpen in currentLine and whenTagClosed in currentLine:

                # Remove <when> & </when> tags
                currentLine = find_between(currentLine,whenTagOpen,whenTagClosed)

                #Extract Date
                Date = find_between(currentLine,"","T")

                #Extract Time and Format to Minutes
                Time = find_between_r(currentLine,"T","")
                Time = Time[0:5]
            
            elif coordTagOpen in currentLine and coordTagClosed in currentLine:

                # Remove <coordinate> & </coordinate> tags
                currentLine = find_between(currentLine,coordTagOpen,coordTagClosed)

                #Split by Space
                Coordinate = currentLine.split()
                Lon = Coordinate[0]
                Lat = Coordinate[1]

                # Add to a list
                DateList.append(Date)
                TimeList.append(Time)
                LatList.append(Lat)
                LonList.append(Lon)
    ## Filtering ##
                
    # Could maybe filter down half of the elements here (by time even?)

    # Calculates the Distance between two pairs of coordinates
    def haversine(lon1,lat1,lon2,lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km

    # Distance of each coordinate pair
    for i in range (len(LatList) - 1):
        currentDistance = (haversine(float(LonList[i]),float(LatList[i]),float(LonList[i + 1]),float(LatList[i + 1])))
        # Max Distance is 0.002 change to edit
        if currentDistance > 1:
            #print ("Acceptable")
            #print (DateList[i])
            #print (TimeList[i])
            #print (LonList[i])
            #print (LatList[i])
        
            # Add into the CSV File
            writer.writerow([DateList[i]] + [TimeList[i]] + [LatList[i]] + [LonList[i]])
