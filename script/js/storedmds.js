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
console.log(mydata);
//var data = JSON.parse(jsdata);
console.log(mydata);
//console.log(jsdata);

/*
$(document).ready(function(){
	$.getJSON("js/mds.json", function(data){
		console.log(data.yo);
		console.log(data.ya);
	}).fail(function(){
		console.log("An Error has occured.");
	});
});
*/

/*
fetch("http://js/mds.json")
	.then((response) => {
		return response.json();
	})
	.then((myJson) => {
		console.log(myJson);
	});
*/
function calcRectArea(width, height) {
  return width * height;
}

console.log(calcRectArea(5, 6));
console.log(calcRectArea(5, 6));

function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                alert(allText);
            }
        }
    }
    rawFile.send(null);
}


console.log(typeof jsdata)
//var yo = readTextFile(jsdata);
//console.log(readTextFile(jsdata))


