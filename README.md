# Classification des capacités Aéronautiques des États du Monde (CAEM) :

Mon travail à l’OACI consiste en une classification des états membres de l’organisation en fonction de leurs capacités aéronautiques. L’objectif est de déterminer quels états du monde ont le plus besoin du soutien technique de la section IAA (développement de logiciels, ateliers de formation, …), de manière à mieux répartir ses ressources pour qu’elles soient le plus utile possible. Cette classification se base sur un certain nombre d’indicateurs comme le nombre d’aéroports, le nombre et l’orientation des pistes d’atterrissage, le nombre de compagnies aériennes, le trafic aérien annuel, …

*En appliquant celle-ci sur les données des 15 dernières années, il est alors possible de déterminer si les capacités aéronautiques d’un état sont stables ou instables, en progression ou en régression (et même dans certains cas de suivre l’évolution politique du pays en question).*


# Classification of World States according Civil Aviation Capacities :

During my internship at the ICAO, I elaborate a classification of member states according their civil aviation capacities. The goal is to determine which world states need the most the technical support of the IAA section (software development, training workshops, …), in order to allocate the best way their resources. This categorization is based on some indicators as the number of airports, the number and the layout of runways, the number of airlines, the yearly flight traffic, …

*In extending the classification on the data of the last 15 years, one can determine if the civil aviation capacities of a member state are stable or unstable, increasing or decreasing (and even sometimes following the political changes in the country).*

You can find in this repository the needed document to understand and reproduce my classification by the ICAO member countries :
- The "Data" folder contains any needed database for this work.
- The "Results" folder contains a presentation of my work and the different analysis I produced.
- Finally, the main folder contains two program :
  - "Database.py", which contains all the function I wrote spreading into differents classes.
> If you download the programs, you must check that they are all in the same folder even if their aren't ion the GitHub. Otherwise Python might not find the module "Database" used in every programs.
  - "Complete_Classification.py", which enable to create automatically the classification between 2003 & 2018 (in the form of excel documents).
