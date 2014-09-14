d3.json("polioPercent.json", function(data){

var years = Object.keys(data) 

//Set up the size of the graph
var height  = 500,
	width   = 1000,
	padding = 10;

var maxPercentage = 0, //need to seed this to find max and min percents. 
	minPercentage = 0.2;

for (var i = 0; i < years.length; i++){
	var maxPerc    = d3.max(data[years[i]], function(d){return d["polioPercent"]})
	var minPerc    = d3.min(data[years[i]], function(d){ if (d["polioPercent"] !== 0) {return d["polioPercent"]} } )
	if (maxPerc > maxPercentage) {
		maxPercentage = maxPerc
	}
	if (minPerc < minPercentage) {
		minPercentage = minPerc
	}
}

console.log("Max = " + maxPercentage + " Min = " + minPercentage)

var yScale = d3.scale.linear()
				.domain([0, maxPercentage])
				.range([0, height - padding]) //-50 for fitting text

var xScale = d3.scale.ordinal()
				.domain(d3.range(data[31].length + 1))
				.rangeRoundBands([0,width],0.2);

var svg = d3.select("#visualization")
			.append("svg")
			.attr("height", height)
			.attr("width", width)

function fillColor(value){
	if (value != 0) {
		return "steelblue"
	} else {
		return "black"} }

svg.selectAll("rect")
	.data(data[31], function(d) {return d["state"]} )
	.enter()
	.append("rect")
	.attr("x", function(d,i) {return xScale(i) })
	.attr("y", function(d){return height - yScale(d["polioPercent"])})
	.attr("height", function(d){return yScale(d["polioPercent"])})
	.attr("width", xScale.rangeBand())
	.attr("fill", function(d) { return fillColor(d["polioPercent"])})
	.on("click", function(){
		history(31)
	})
 
svg.selectAll("text")
	.data(data[31], function(d) {return d["state"]} )
	.enter()
	.append("text")
	.attr("class", "stateNames")
	.attr("x", function(d,i) {return xScale(i) + (xScale.rangeBand())/2 })
	.attr("y", function(d){return (height - 3) - yScale(d["polioPercent"])})
	.text(function(d){return d["state"]})
	.attr("text-anchor", "middle")
	.attr("font-family", "optima")
	.attr("font-size", 9)


svg.selectAll("text")
	.append("text")
	.attr("x", width - 20)
	.attr("y", height - 300)
	.text("1931")
	.attr("font-family", "optima")
	.attr("font-size", 30)


function changeYear(year){
	d3.selectAll("rect")
		.data(data[year], function(d) {return d["state"]} )
		.transition()
		.attr("y", function(d){return height - yScale(d["polioPercent"])})
		.attr("height", function(d){return yScale(d["polioPercent"])})
		.attr("fill", function(d) { return fillColor(d["polioPercent"])})

	d3.selectAll(".stateNames")
		.data(data[year], function(d) {return d["state"]})
		.transition()
		.attr("y", function(d){return (height - 3) - yScale(d["polioPercent"])})

	d3.select("#currentYear")
		.text("Currently showing: 19" + year)
}

//slider code
$(function() {
            $( "#slider" ).slider({
               value: 31,
               ticks: true,
               min: 31,
               max: 69,
               step: 1,
               animate:"slow",
               orientation: "horizontal",
               slide: function( event, ui ) { changeYear(ui.value) }
           });
         });

var theYear = 31

function history(theYear){
	d3.selectAll("rect")
		.data(data[theYear], function(d) {return d["state"]} )
		.transition()
		.ease("log")
		.duration(500)
		.attr("y", function(d){return height - yScale(d["polioPercent"])})
		.attr("height", function(d){return yScale(d["polioPercent"])})
		.attr("fill", function(d) { return fillColor(d["polioPercent"])})
		.each("end", function(d,i){ 
			if (theYear < 69) {
				history(theYear + 1)
				console.log("changing it")
			}} )

	d3.selectAll(".stateNames")
		.data(data[theYear], function(d) {return d["state"]})
		.transition()
		.ease("log")
		.duration(500)
		.attr("y", function(d){return (height - 3) - yScale(d["polioPercent"])})

	d3.select("#currentYear")
		.text("Currently showing: 19" + theYear)

	$("#slider").slider('value', theYear);
}

d3.select("#startButton")
	.on("click", function(){history(31)})

})