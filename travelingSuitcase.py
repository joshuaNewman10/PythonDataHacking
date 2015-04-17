#Get modules/libraries
import webbrowser
import urllib
from xml.etree.ElementTree import parse
import math
import time
import datetime


def trackBuses():    
  #Open static map page in Chrome
  def openMap(lat, lon):
    baseStr = 'https://maps.googleapis.com/maps/api/staticmap?center='
    locStr = '' + str(lat) + ',' + str(lon)
    zoomStr = '&zoom=15'
    sizeStr = '&size=800x800'
    markers = '&markers=color:blue|' + locStr
    queryStr = baseStr + locStr + zoomStr + sizeStr + markers
    webbrowser.open(queryStr)

  def writeOutput(busInfo, dist):    
    time = datetime.datetime.now()

    with open("busResults.txt", "a") as myfile:
        myfile.write(busInfo['route'] + ' traveling: ' + busInfo['direction'] + ' at time: ' + str(time) + ' distance: ' + str(dist) + ' miles')
        myfile.write('\n')




  #Calculate distance between office and bus coords
  def unitSphereDistance(lat1, long1, lat2, long2):
      # Convert latitude and longitude to 
      # spherical coordinates in radians.
      degToRadians = math.pi/180.0
           
      # phi = 90 - latitude
      phi1 = (90.0 - lat1)*degToRadians
      phi2 = (90.0 - lat2)*degToRadians
           
      # theta = longitude
      theta1 = long1*degToRadians
      theta2 = long2*degToRadians
           
      # Compute spherical distance from spherical coordinates.
           
      # For two locations in spherical coordinates 
      # (1, theta, phi) and (1, theta, phi)
      # cosine( arc length ) = 
      #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
      # distance = rho * arc length
       
      cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
             math.cos(phi1)*math.cos(phi2))
      arc = math.acos( cos )
      earthRadiusInMiles = 3963.1676 
   
      # Remember to multiply arc by the radius of the earth 
      # in your favorite set of units to get length.
      return arc * earthRadiusInMiles

  #Startup Data
  officeCoords = {'latitude': '41.98062', 'longitude': '-87.668458'}

  # Get XML of all buses in Chicago
  u = urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
  data = u.read()
  print(data)
  f = open('rt22.xml', 'wb')
  f.write(data)
  f.close()

  
  #Turn xml into a document tree
  doc = parse('rt22.xml')
  busNodes = doc.findall('bus')
  busList = {}

  #Get information for buses on route
  i = 0
  for bus in busNodes:
    i = bus.findtext('id')
    busList[i] = {'direction': bus.findtext('d'), 'latitude': bus.findtext('lat'), 'longitude': bus.findtext('lon'), 'route': bus.findtext('rt')}
    dist = unitSphereDistance(float(officeCoords['latitude']), float(officeCoords['longitude']), float(busList[i]['latitude']), float(busList[i]['longitude']))
    print(dist)
    if dist < 1:
      writeOutput(busList[i], dist)
      openMap(busList[i]['latitude'], busList[i]['longitude'])



def executeSomething():
    #code here
    trackBuses()
    time.sleep(60)

while True:
    executeSomething()
