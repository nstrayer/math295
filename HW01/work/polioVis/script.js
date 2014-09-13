d3.json("polioPercent.json", function(data){

var years = Object.keys(data) 

//console.log(data[years[2]])
var maxPercentage = 0

for (var i = 0; i < years.length; i++){
	var maxPerc = d3.max(data[years[i]], function(d){return d["polioPercent"]})
	if (maxPerc > maxPercentage) {
		maxPercentage = maxPerc
	}
}

console.log(maxPercentage)

// percents = []
// for (var i = 1; i < data.length; i++){ 					//loop through list of dictionaries
// 	for (var j = 0; j < states.length; j++) { 		    //inside the dictionaries loop through the states
// 		var state = states[j]
// 		percents.push(data[i][state])
// 	}
// }

// maxPercent = d3.max(percents, function(d){return d})
// minPercent = d3.min(percents, function(d){ if (d !== 0) {return d} } )
// console.log("Max: " + maxPercent + " Min: " + minPercent)

//percents.forEach(function(element){console.log(element) }) //example of forEach syntax, valubale to have. 
})