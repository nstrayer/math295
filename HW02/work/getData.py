# The site for documentation about Tycho api: http://www.tycho.pitt.edu/api_help.php
import urllib
import requests

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

diseases = ["measles", "Whooping+Cough+[pertussis]", "scarlet+fever", 
		    "diphtheria", "influenza", "mumps", "rubella", 
		    "Chickenpox+[varicella]"]

statistic = ["cases", "deaths"]

apiKey = open("nicksSuperSecretApiKey.txt").read().strip()

baseUrl = "http://www.tycho.pitt.edu/api/query?"
#baseUrl = "http://www.tycho.pitt.edu/api/info?" # Just in case I need to query by available


def getTychoData(stat, state, disease):
	"""
	Feed me a statistic (cases or deaths), a state and a disease and I will spit out a file 
	<StateAbrev>_<Disease>_<Statestic>_tycho.csv with all the project tycho 
	data you could ever want in it. 
	"""
	url = baseUrl + "event=" + stat + "&disease=" + disease + "&loc_type=state&state=" + \
		state + "&apikey=" + apiKey + ".csv"

	outfile = "data/%s/%s_%s_%s_tycho.csv" %(stat,state,disease,stat)
	urllib.urlretrieve(url,outfile)


for state in states:
	for disease in diseases:
		try: 
			getTychoData(statistic[1], state, disease)
		except:
			print "There was a problem with " + state + " and " + disease

# for state in states:  # I messed up the names of a couple of the diseases at first so I had 
# 	try: 				# to re-run the loop at specific points to fix it
# 		disease = diseases[2]
# 		getTychoData(statistic[1], state, disease)
# 	except:
# 		print "There was a problem with " + state + " and " + disease