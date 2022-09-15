/*var fileInput = document.getElementById("coucou"),

    readFile = function () {
	  var reader = new FileReader();
	  reader.onload = function () {
		document.getElementById('out').innerHTML = reader.result;
	  };
	  // start reading the file. When it is done, calls the onload event defined above.
	  reader.readAsBinaryString(fileInput.files[0]);
    };


fileInput.addEventListener('change', readFile);
*/
//const data = require('./mds.json');

var mydata = JSON.parse(jsdata);
var data= mydata.data;
var layout= mydata.layout;

var updatemenus=[
	{
	buttons: [
		{
			args: ['shapes', []],
			label: 'None',
			method: 'relayout'
		}
	],
	direction: 'left',
	pad: {'r': 10, 't': 10},
	showactive: true,
	type: 'buttons',
	x: 0.1,
	xanchor: 'left',
	y: 1.2,
	yanchor: 'top'
	}
]
console.log(updatemenus)

var cluster=Array()
for (let i = 0; i < data.length; i++) {
	data[i].marker.color= Array(data[i].x.length).fill(data[i].marker.color)
	data[i].cachetext=data[i].text
	data[i].text= Array(data[i].x.length).fill(null)
	cluster.push({type:"rectangle",
							xref: 'x', yref: 'y',
							x0: Math.min(...data[i].x), y0: Math.min(...data[i].y),
							x1: Math.max(...data[i].x), y1: Math.max(...data[i].y),
							opacity:0.25,
							line:{color:data[i].marker.color[0]},
							fillcolor:data[i].marker.color[0]
	})
	console.log(data[i].marker.color)
	updatemenus[0].buttons.push({args: ['shapes', [cluster[i]]],
							label: data[i].legendgroup,
							method: 'relayout'})
}

//layout.updatemenus=updatemenus;
console.log(mydata.data[0]);
console.log(cluster)
Plotly.newPlot("myDiv", data, layout);

console.log("yo");
console.log(data[0]);
console.log("gae");



console.log(data[0])


myDiv.on("plotly_click", function(data){
	//alert('You clicked this Plotly chart!');
	var pn='',
	tn='',
	colors=[];
	for(var i=0; i < data.points.length; i++){
		pn = data.points[i].pointNumber;
		tn = data.points[i].curveNumber;
		//colors = data.points[i].data.marker.color;
		text= data.points[i].data.text
		cachetext= data.points[i].data.cachetext
		console.log(data)
	};
	console.log((text[pn] === null));
	//colors[pn] = '#C54C82';
	if (text[pn] === null){
		text[pn] = cachetext[pn];
		console.log("fefzfazefa");
	} else {
		text[pn]= null;
		console.log("vcxvxc");
	}
	
	console.log(text);
	console.log(cachetext);
	var update = {"text":[text]};
	console.log(update);
	Plotly.restyle('myDiv', update, [tn]);
	Plotly.restyle('myDiv', update, [tn]);
	//console.log(data)
});

myDiv.on('plotly_doubleclick', function(data){
	var pn='',
	tn='',
	colors=[];
	console.log(myDiv.data);
	for(var i=0; i < myDiv.data.length; i++){
		//myDiv.data.[i]
		var update = {'marker':{size:16}};
		Plotly.restyle('myDiv', update,[tn]);
	}
});
//console.log(myDiv)
//console.log(myDiv);

/*

var myPlot = document.getElementById('myDiv'),
    x = [1, 2, 3, 4, 5, 6],
    y = [1, 2, 3, 2, 3, 4],
    colors = ['#00000','#00000','#00000',
		  '#00000','#00000','#00000'],
    data = [{x:x, y:y, type:'scatter',
		 mode:'markers', marker:{size:16, color:colors}}],
    layout = {
	  hovermode:'closest',
	  title:'Click on a Point to Change Color<br>Double Click (anywhere) to Change it Back'
     };

console.log("gfeaz")
console.log(data)

Plotly.newPlot('myDiv', data, layout);

myPlot.on('plotly_click', function(data){
  var pn='',
	tn='',
	colors=[];
  for(var i=0; i < data.points.length; i++){
    pn = data.points[i].pointNumber;
    tn = data.points[i].curveNumber;
    colors = data.points[i].data.marker.color;
  };
  colors[pn] = '#C54C82';

  var update = {'marker':{color: colors, size:16}};
  Plotly.restyle('myDiv', update, [tn]);
  console.log(data)
 
});

console.log("ta")
console.log(myDiv)
*/

/*
var myPlot = document.getElementById('myDiv'),
    x = [1, 2, 3, 4, 6],
    y = [10, 20, 30, 20, 30],
    data = [{x:x, y:y, type:'scatter',
		 mode:'markers', marker:{size:20}
		}],
    layout = {hovermode:'closest',
		  title:'Click on Points'
     };

Plotly.newPlot('myDiv', data, layout);

myPlot.on('plotly_click', function(){
    alert('You clicked this Plotly chart!');
});
*/
