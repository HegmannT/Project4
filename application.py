#-------------------------------------------------------------------------------
# Name:        ENGO 551 Lab 4
# Student:      Tanya Hegmann
# Created:     25-02-2021
# Goal:        Have an aesthetic map layer building off of lab 2's Leaflet code
#-------------------------------------------------------------------------------

#Additional Imports below
import os
import csv #added on for csv read in
import json #built in json package to work with data
import requests #import requests #as provided in lab to acess requests for json


from flask import Flask, session, render_template, request, jsonify #Note added in request & render_template as they do in the lectures
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
#postgres://hittsqstabxgpv:edfab3a728220ef17e540ebb509e91c46a8fb41af43fb845ecb30ff16b7be7ce@ec2-52-7-168-69.compute-1.amazonaws.com:5432/dfafkrpfvhk650
db = scoped_session(sessionmaker(bind=engine))

#------------------------------------------------------------------------------
@app.route("/")
def index():


    #Get Hospital and Clinic Data from Database to pass in
    hospitaltosearch = "Hospital" #keyword to search partial matches
    clinictosearch = "PHS Clinic" #keywork to search partial matches
    hospitalsearchresults = db.execute("SELECT typeof, name, address, comm, longitude, latitude, location FROM communityservices1 WHERE typeof LIKE (:hospitaltosearch) OR typeof LIKE (:clinictosearch) ",{"hospitaltosearch":("%"+hospitaltosearch+"%"),"clinictosearch":("%"+clinictosearch+"%")}).fetchall()
    numhospitals = len(hospitalsearchresults)

    #Get School Data from Database to pass in
    schoolsearchresults = db.execute("SELECT * FROM schoollocations1").fetchall() #fetch all since want all the points
    numschools = len(schoolsearchresults)

    return render_template("home.html", hospitalsearchresults = hospitalsearchresults, schoolsearchresults = schoolsearchresults, numhospitals = numhospitals, numschools = numschools) #pass in database results as a variables












###------------------------------------------------------------------------------
### Already uploaded the tables as needed through the following code, so commenting out so that the / route pages can no longer be acessed since they are not needed
##
##@app.route("/import_lab4_school_locations") #long name don't want users to acidently stumble upon but is required for
##def importexcel1():
##    #import books from books.csv into a database
##
##    #check if already been imported by checking if entry in there (don't want to double import every time run page)
##
##    #name to check (first entry from excel)
##    name1 = "Mount Royal University - City Centre Campus"
##
##    checkuser = db.execute("SELECT * FROM schoollocations1 WHERE (name = '{name}')".format(name = name1)).fetchone()
##
##
##    if checkuser is None: #if not already uploaded
##        #Upload
##        opencsv = open("School_Locations.csv")
##        bookreader = csv.reader(opencsv)
##
##        #import values
##        for name, board, typeof, nameab, addressab, city, province, grades, postsecond, datasource, provincialcodenum, ecs, elem, juniorh, seniorh, processdt, postalcod, structureid, longitude, latitude, location in bookreader:
##            db.execute("INSERT INTO schoollocations1 (name, board, typeof, nameab, addressab, city, province, grades, postsecond, datasource, provincialcodenum, ecs, elem, juniorh, seniorh, processdt, postalcod, structureid, longitude, latitude, location) VALUES (:name, :board, :typeof, :nameab, :addressab, :city, :province, :grades, :postsecond, :datasource, :provincialcodenum, :ecs, :elem, :juniorh, :seniorh, :processdt, :postalcod, :structureid, :longitude, :latitude, :location)",{"name":name, "board":board, "typeof":typeof, "nameab":nameab, "addressab":addressab, "city":city, "province":province, "grades":grades, "postsecond":postsecond, "datasource":datasource, "provincialcodenum":provincialcodenum, "ecs":ecs, "elem":elem, "juniorh":juniorh, "seniorh":seniorh, "processdt":processdt, "postalcod":postalcod, "structureid":structureid, "longitude":longitude, "latitude":latitude, "location":location})
##        db.commit()#commit changes
##
##        textvar = "School_Locations.csv Has Been Uploaded"
##        opencsv.close() #Close the open csv
##        return render_template("proofofupload.html", textvar = textvar) #quick page for compleation of upload and screenshot proof of import sucsess
##
##
##    #else already uploaded
##    textvar = "School_Locations.csv Has Already Been Uploaded"
##    return render_template("proofofupload.html", textvar = textvar) #quick page for compleation of upload and screenshot proof of import sucsess
##
##
##
##
##@app.route("/import_lab4_community_services") #long name don't want users to acidently stumble upon but is required for
##def importexcel2():
##    #import books from books.csv into a database
##
##    #check if already been imported by checking if entry in there (don't want to double import every time run page)
##
##    #name to check (first entry from excel)
##    typeof1 = "Library"
##
##    checkuser = db.execute("SELECT * FROM communityservices1 WHERE (typeof = '{typeof}')".format(typeof = typeof1)).fetchone()
##
##
##    if checkuser is None: #if not already uploaded
##        #Upload
##        opencsv = open("Community_Services.csv")
##        bookreader = csv.reader(opencsv)
##
##        #import values
##        for typeof, name, address, comm, longitude, latitude, location in bookreader:
##            db.execute("INSERT INTO communityservices1 (typeof, name, address, comm, longitude, latitude, location) VALUES (:typeof, :name, :address, :comm, :longitude, :latitude, :location)",{"typeof":typeof, "name":name, "address":address, "comm":comm, "longitude":longitude, "latitude":latitude, "location":location})
##        db.commit()#commit changes
##
##
##        textvar = "community_services.csv Has Been Uploaded"
##        opencsv.close() #Close the open csv
##        return render_template("proofofupload.html", textvar = textvar) #quick page for compleation of upload and screenshot proof of import sucsess
##
##
##    #else already uploaded
##    textvar = "community_services.csv Has Already Been Uploaded"
##    return render_template("proofofupload.html", textvar = textvar) #quick page for compleation of upload and screenshot proof of import sucsess

