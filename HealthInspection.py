#Get modules/libraries
import csv
import re
import sys
import pylab
from pylab import *
#Tabluate reports by facilityType
def facilityType():   
  #import Chicago health inspection data
  healthData = open('food.csv')

  #Set up data storage
  facilityTypeIndex = {}
  riskLevelIndex = {};

  # Organize Data by Type
  for row in csv.DictReader(healthData):
    if row['Facility Type'] not in facilityTypeIndex:
      facilityTypeIndex[row['Facility Type']] = []
    facilityTypeIndex[row['Facility Type']].append(row)
  
  # Log all resteraunts
  print(len(facilityTypeIndex['Restaurant']))

  #Sort resteraunts by number of issues
  sortedFacilities = sorted(facilityTypeIndex, key=len)

  #print out ten facility types with most complaints
  print(sortedFacilities[0:10])

#Tabulate reports by their risk level
def riskLevel():
  healthData = open('food.csv')

  #Organize Data by Risk Level
  for row in csv.DictReader(healthData):
    if row['Risk'] not in riskLevelIndex:
      riskLevelIndex[row['Risk']] = []
    riskLevelIndex[row['Risk']].append(row)

  #open dataset for reading

#Tabulate reports for subway by their risk level
def subway():
  healthData = open('food.csv')
  #make subway array holder
  subway = {}

  #Get all subway data
  for row in csv.DictReader(healthData):
    if row['DBA Name'] == 'SUBWAY SANDWHICH' or row['AKA Name'] == 'SUBWAY':
      if row['Risk'] not in subway:
        subway[row['Risk']] = []
      subway[row['Risk']].append(row)

  for risk in subway:
    print(risk, len(risk))

  pylab.pie([23, 47, 62])
  xlabel('hi mom!')
  pylab.show()


def parseNotes(line):
  interestingFeatures = ['rodent', 'droppings']


#Calls various above functions
def main():
  if len(sys.argv) !=2:
    print 'usagage: HealthInspetion.py {--subway | --risk | --facilityType}'

  option = sys.argv[1]

  if option == '--subway':
    subway()
  elif option == '--risk':
    riskType()
  elif option == '--facilityType':
    facilityType()

if __name__ == '__main__':
  main()
