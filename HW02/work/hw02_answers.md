# Homework 2
### Nick Strayer, September 18, 2014

—
## Problem 1

This was relatively straightforward. A couple of the problems that I ran into along the way: 

* ### What tool to use:
		* I originally tried using __requests__ but the format didn’t work with Tycho (at least in the time I spent with it.) It seemed like Tycho was particular about the order of the parameters in the query and requests couldn’t care less. 
		* I eventually went with good-ol-fashioned __urllib__. I did this because it was the method that was used in the example on the Tycho website. I lost the ability to fail gracefully but Tycho actually nicely fails in the output anyways so it was fine. 

* ### How to feed in the parameters: 
	* It wasn’t super clear if Tycho wanted individual states for the state query, and if it did, if it wanted them given in “loc” or “state” (seems more obvious now looking back on it.) Through trial and error this was figured out. 

* ### How to store the data:
	* Did I want to aggregate the data into individual csv’s for each state or disease or what? Eventually, I decided to simply get everything in as fine a resolution as possible because space is cheap and later processing would be easier if I choose to switch my methods. 

* ### Messed up disease names:
	* The first time that I ran the script I incorrectly queried for Chickenpox and Whooping cough. I didn’t realize that you needed to name them explicitly (i.e. with their formal name in square brackets). 
	* I changed their names and re-ran the script only looping over the messed up diseases. __Lines 43 to 48 in getData.py__. 

—
## Problem 2

The age old question of how to represent data! I am choosing to go summed by the whole country as state boundaries, in my opinion, especially for something like this are rather arbitrary. No-one*  looks back and remembers how badly a disease hit Ohio in the 1920’s, (an exception would be for something like AIDS in San Fransisco in the 1980’s, but we aren’t looking at that data.) 

I read in all of the files grabbed in problem 1, then concatenated them by disease, grouped by year, then summed to get the whole country average. __18 to 25 in problem2.py__


