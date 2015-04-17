#Get modules/libraries
import csv 
import operator
import re

# Import Chicago potholes file
potholesFile = open('potholes.csv')

#Set up data storage
potholesLookup = {}
potholesByBlock = {}

#Use to make street address be stored the same
def appendChar(baseStr, char, times):
  i = 0
  while i < times:
    i+=1
    baseStr += char
  return baseStr

#Populate table with pothole data
for row in csv.DictReader(potholesFile):
  address = row['STREET ADDRESS']
  addressParts = address.split(' ')
  num = addressParts[0]
  if len(num) > 0:
    addressParts[0] = appendChar(num[0], 'X', len(num)-1)
  address = ' '.join(addressParts)
  try: 
    numPotHoles = int(row['NUMBER OF POTHOLES FILLED ON BLOCK'])
  except ValueError:
    numPotHoles = 0
  latitude = row['LATITUDE']
  longitude = row['LONGITUDE']

  if address in potholesLookup :
    potholesLookup[address]['potholeCount'] +=numPotHoles
  else:
    potholesLookup[address] = {'potholeCount': numPotHoles, 'lat': latitude, 'long': longitude}

#Sort by the poholeCount property of the second item in the resulting sorted tuple
def getPotholeCount(item):
  return item[1]['potholeCount']

#SortData by number of pot holes
sortedPotholeData = sorted(potholesLookup.items(), key=getPotholeCount)


#Order data by continuous streets and store their counts
tenBlockStreets = {'ashland': {'count': 0}}

for entry in sortedPotholeData:
  isAnX = re.search(r'X', entry[0][0:6])
  if not isAnX:
    continue
  else:
    street = entry[0].split('X ')[1]
    if street not in tenBlockStreets:
      tenBlockStreets[street] = {'count': 0}
    blockNum = entry[0].split(' ')[0]
    if blockNum not in tenBlockStreets[street]:
      tenBlockStreets[street][blockNum] = (entry[0])
      tenBlockStreets[street]['count'] += entry[1]['potholeCount']


def getCount(route):
  return route[1]['count']

sortedTenBlockStreets = sorted(tenBlockStreets.items(), key=getCount)
tenBestRoutes = []


for route in sortedTenBlockStreets:
  if len(route[1])-1 >=10:
    tenBestRoutes.append((route[0], route[1]['count']))

print(tenBestRoutes[-10:])