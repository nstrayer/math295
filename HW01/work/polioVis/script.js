d3.json("listData.json", function(data){

var states = Object.keys(data[1]) 
percents = []
for (var i = 1; i < data.length; i++){ 					//loop through list of dictionaries
	for (var j = 0; j < states.length; j++) { 		    //inside the dictionaries loop through the states
		var state = states[j]
		percents.push(data[i][state])
	}
}

maxPercent = d3.max(percents, function(d){return d})
minPercent = d3.min(percents, function(d){ if (d !== 0) {return d} } )
console.log("Max: " + maxPercent + " Min: " + minPercent)

//percents.forEach(function(element){console.log(element) }) //example of forEach syntax, valubale to have. 
})