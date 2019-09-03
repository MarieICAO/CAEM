In this folder, you have three kinds of documents :
- A database with only the number of Runways by Airport (called "Runways" in ".txt" or '.xlsx").
- "Rwys.json" is the layout of Runways for some Airports. "Rwys_Additional.json" is its expansion, which only includes the Airports missing in "Rwys.json" with more than one Runway, because the layout isn't meaningful for the Airports with a single Runway.
- "Runways.py" is the programm which merges the two databases (in importing the module "Database").
- "Runways.json" is the final databse of Runways with differents informations about the number & the layout of Runways by Airports.
