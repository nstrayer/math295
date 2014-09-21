d3.json("polioPercent.json", function(data){

var years = Object.keys(data) 

//Set up the size of the graph
var height  = 400,
	//width   = 1000,
	width   = 800,
	padding = 0;

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

var yScale = d3.scale.linear()
				.domain([0, maxPercentage])
				//.range([0, height]) 
				.range([height,0])

var xScale = d3.scale.ordinal()
				.domain(d3.range(data[31].length + 1))
				.rangeRoundBands([35,width - padding],0.2);

var svg = d3.select("#visualization")
			.append("svg")
			.attr("height", height + padding)
			.attr("width", width + padding)

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
	//.attr("y", functon(d){return height - yScale(d["polioPercent"])})
	//.attr("y", function(d){return yScale(d["polioPercent"])})
	.attr("y", function(d){return yScale( d["polioPercent"] ) }  )
	.attr("height", function(d){return height - yScale(d["polioPercent"])})
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
	//.attr("y", function(d){return (height - 3) - yScale(d["polioPercent"])})
	.attr("y", function(d){return ( yScale( d["polioPercent"] ) -3 )})
	.text(function(d){return d["state"]})
	.attr("text-anchor", "middle")
	.attr("font-family", "optima")
	.attr("font-size", 9)


var startYear = [31]
svg.selectAll("text")
	.data(startYear, function(d){return d})
	.enter()
	.append("text")
	.attr("id", "bigYear")
	.attr("x", width *(5/8) )
	.attr("y", height - 250)
	.text(function(d){return "19" + d})
	.attr("font-family", "optima")
	.attr("font-size", 130)
	.attr("opacity", .5)


function changeYear(year){
	d3.selectAll("rect")
		.data(data[year], function(d) {return d["state"]} )
		.transition()
		//.attr("y", function(d){return height - yScale(d["polioPercent"])})
		.attr("y", function(d){return yScale(d["polioPercent"])})
		.attr("height", function(d){return height - yScale(d["polioPercent"])})
		.attr("fill", function(d) { return fillColor(d["polioPercent"])})

	d3.selectAll(".stateNames")
		.data(data[year], function(d) {return d["state"]})
		.transition()
		//.attr("y", function(d){return (height - 3) - yScale(d["polioPercent"])})
		.attr("y", function(d){return ( yScale( d["polioPercent"] ) -3 )})

	d3.select("#currentYear")
		.text("Currently showing: 19" + year)

	d3.select("#bigYear")
		.text("19" + year)
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
		//.ease("exp")
		.duration(300)
		//.attr("y", function(d){return height - yScale(d["polioPercent"])})
		.attr("y", function(d){return yScale(d["polioPercent"])})
		.attr("height", function(d){return height - yScale(d["polioPercent"])})
		.attr("fill", function(d) { return fillColor(d["polioPercent"])})
		.each("end", function(d,i){ 
			if (theYear < 69) {
				history(theYear + 1)
				console.log("changing it")
			}} )

	d3.selectAll(".stateNames")
		.data(data[theYear], function(d) {return d["state"]})
		.transition()
		//.ease("exp")
		.duration(300)
		//.attr("y", function(d){return (height - 3) - yScale(d["polioPercent"])})
		.attr("y", function(d){return ( yScale( d["polioPercent"] ) -3 )})

	d3.select("#currentYear")
		.text("Currently showing: 19" + theYear)

	d3.select("#bigYear")
		.text("19" + theYear)

	$("#slider").slider('value', theYear);
}

d3.select("#startButton")
	.on("click", function(){history(31)})

var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left")
    //.ticks(3)
    .tickSize(-10);


svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);

d3.select(".y")
	.selectAll("text")
	.attr("x", 35)
	.attr("font-family", "optima")
	.attr("font-size", 8.5)
	.attr("y", function(d){
		return (d3.select(this).attr("y") - 3)
	})

})

