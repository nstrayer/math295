//
var width   = $('#visualization').width(),
	height  = $(window).height()* .85,
	padding = 15,
	red     = "#e41a1c",
	blue    = "#377eb8",
	transitionSpeed = 1500,
	delayTime = 20;


var svg = d3.select("#visualization").append("svg")
			.attr("height", height)
			.attr("width", width)

var yScale = d3.scale.linear()
			.domain([0, 1])
			.range([height, padding])

var xScale = d3.scale.ordinal()
			.domain([0,1])
			.rangePoints([padding*2.8,width - padding],0);

var colorScale = d3.scale.linear()
				   .domain([0, 1])
				   .range([blue, red])

var yAxis = d3.svg.axis()
			.scale(yScale)
			.orient("right")

var axisLabel = svg.append("text")
					.text("-log10(P-Val)")
					.attr("transform","translate(" + ( 13 ) + "," + (height/2) +
						")rotate(-90)"
					)

function customAxis(g) {
				g.selectAll("text")
				.attr("x", 4)
				.attr("dy", -2);
				g
				.attr("transform", "translate(" + 20 + ",0)")
			}

var gy = svg.append("g")
			.attr("class", "axis")
			.call(yAxis)
			.call(customAxis)

var significanceBar = svg.append("line")
			.attr("x1", padding + 4)
			.attr("x2", width - padding)
			.attr("y1", yScale(0))
			.attr("y2", yScale(0))
			.attr("stroke-width", 2)
			.attr("stroke", "black")

var significanceText = svg.append("text")
						  .attr("x", width - padding)
						  .attr("y",0)
						  .attr("text-anchor", "end")
						  .text("")


function updateManhattan(file, updateTime){
	//taking an input of a file name, redraw the points accordingly
	d3.select("#current").text(file)

	d3.csv(file + "_Data.csv", function(data){

		delayTime = 20;

		if ( data.length > 200){ //if it is a small dataset do transitions.
			updateTime = 0
			delayTime  = 0
		}

		for (var i = 0; i < data.length; i++){
			data[i].PVal    	 = parseFloat(data[i].PVal);
			delete data[i][""] //because I am a neat freak.
		}

		console.log(-Math.log10(.05/data.length))

		var dataMax     = d3.max(data, function(d){return d.PVal}),
			bonferroni  = -Math.log10(.05/data.length),
			maxVal      = d3.max([dataMax,bonferroni+.5]),
			minVal      = d3.min(data, function(d){return d.PVal});

		yScale    .domain([0, maxVal])
		xScale    .domain(d3.range(data.length + 1))
		colorScale.domain([minVal, maxVal])

		significanceBar
			.transition()
			.duration(updateTime)
			.attr("y1", yScale(bonferroni))
			.attr("y2", yScale(bonferroni))

		significanceText
			.transition()
			.duration(updateTime)
			.attr("y", yScale(bonferroni) - 5)
			.text("Needed for significance")

		var points = svg.selectAll("circle")
					.data(data, function(d){return d.SNP;})

		points
			.exit()
			.transition()
			.duration(updateTime/2)
			.attr("cy",0)
			.remove()

		points
			.enter()
			.append("circle")
			.attr("cx", function(d,i){return xScale(i);})
			.attr("cy",0)
			.attr("r", 5)
			.on("mouseover", function(d){
				d3.select("#SNPName").text(d.SNP)
				d3.select("#PValue").text(Math.pow(10,-d.PVal).toExponential(4))
			})
			.transition()
			.duration(updateTime)
			.delay(function(d,i){return delayTime*i;})
			.attr("cy", function(d){return (yScale(d.PVal));})
			.transition()
			.attr("fill", function(d){ return colorScale(d.PVal); })


		points
			.transition()
			.duration(updateTime)
			.delay(function(d,i){return delayTime*i;})
			.attr("cx", function(d,i){return xScale(i);})
			.attr("cy", function(d){return (yScale(d.PVal));})
			.attr("fill", function(d){ return colorScale(d.PVal); })


		gy.transition()
			.duration(updateTime)
			.call(yAxis)
			.selectAll("text") // cancel transition on customized attributes
			.tween("attr.x", null)
			.tween("attr.dy", null);

		gy.call(customAxis);

	})
}

var options = [{"name": "Hardy Wienberg",   "file": "HWE" },
			   {"name": "Dominant Arm",     "file": "DRM" },
			   {"name": "Non-Dominant Arm", "file": "NDRM"},
		   	   {"name": "Blood Pressure",   "file": "SBP" }],
	S_width = width*.25,
	S_height = height*.45;

var selector = d3.select("#menu").append("svg")
				.attr("height", S_height)
				.attr("width", S_width)

var selectorScale = d3.scale.linear()
					.domain([0,options.length-1])
					.range([S_height - padding*3.5 , padding*4])

var menu = selector.selectAll("text")
					.data(options)
					.enter()
					.append("text")
					.attr("id", function(d){return d.file + "Select";})
					.attr("font-size", 18)
					.text(function(d){return d.name;})
					.attr("x", 5)
					.attr("y", function(d,i){return selectorScale(i);})
					.attr("text-anchor", "begining")
					.on("mouseover", function(d){
						d3.select(this).attr("font-weight", "bold")
					})
					.on("mouseout", function(d){
						d3.select(this).attr("font-weight", "normal")
					})
					.on("click", function(d){
						updateManhattan(d.file, transitionSpeed)
						menu.classed("menuSelected", false)
						d3.select(this).classed("menuSelected", true)
					})

d3.selectAll(".selector")
	.on("click", function(d){
		d3.selectAll(".selector").classed("selected", false)
		d3.select(this).classed("selected", true)
		var what = d3.select(this).attr("id")
		if (what == "slow"){
			transitionSpeed = 2500
		} else if (what == "med"){
			transitionSpeed = 1500
		} else {
			transitionSpeed = 500
		}
	})

updateManhattan("chr1", transitionSpeed)
d3.select("#SBPSelect").classed("menuSelected", true)

function submitFunc(){
	file = document.getElementById("filename").value;
	updateManhattan(file, transitionSpeed)
}
