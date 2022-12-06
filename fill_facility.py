from models import Facility, Location, Term


listoffac = ['PRIVATEPOOL',
             'SHAREDPOOL',
             'BATHTUBE',
             'KITCHEN',
             'CLEANING',
             'WIFI',
             'AC',
             'LAUNDRY',
             'DISHWASHER',
             'PETFRIENDLY',]


for element in listoffac:
    Facility.get_or_create(name=element)

listoffloc = ["CANGGU",
              "SEMINYAK",
              "ULUWATU",
              "UBUD",
              "JIMBARAN",
              "LAVINA",
              "SUKAWATI"]

listoffterm = ["DAY",
               "MONTH",
               "YEAR",]

for element in listoffac:
    Facility.get_or_create(name=element)

for element in listoffloc:
    Location.get_or_create(name=element)

for element in listoffterm:
    Term.get_or_create(name=element)
