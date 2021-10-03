var goButton = document.getElementById("GoButton")
var departureTime = document.getElementById("DepartureTime")
var arrivalTime = document.getElementById("ArrivalTime")
var departureDate = document.getElementById("DepartureDate")
url = "https://bkciccar.pythonanywhere.com/"
function getDelay(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    dTime = departureTime.value.replace(":","")
    aTime = arrivalTime.value.replace(":","")
    duration = parseInt(aTime) - parseInt(dTime)
    var date = new Date(departureDate.value)
    var day = String(date.getDate())
    xhr.send(JSON.stringify({
        "CRSDepTime": dTime,
        "CRSArrTime": aTime,
        "CRSElapsedTime": String(duration),
        "DayofMonth": day
    }));
    xhr.onload = function() {
        console.log(this.responseText);
        var data = JSON.parse(this.responseText);
        console.log(data);
        document.getElementById("delay").innerText = "Estimated Delay: " + Math.max(Math.round(data.value, 4),0) + " minutes"
      }
      
}