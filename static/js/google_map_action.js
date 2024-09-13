const map = new google.maps.Map(document.getElementById("map"), {
   zoom: 14,
   center: { lat: 49.23394901457209, lng: 28.411018265529787 },
});
var directionsService = new google.maps.DirectionsService();
var directionsDisplay = new google.maps.DirectionsRenderer();
directionsDisplay.setMap(map);

function routingValue() {
    var request = {
        origin: document.getElementById("from").value,
        destination: document.getElementById("to").value,
        travelMode: document.getElementById("mode").value,
        unitSystem: google.maps.UnitSystem.METRIC
    }
    directionsService.route(request, function (result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            const routeResult = document.querySelector('.route__result');
            routeResult.innerHTML = "" +
               "<div class='result__velue'>" +
                  "<h2 class='subtitle__route'>" + "Пункт відправлення: " + "</h2>"  + document.getElementById("from").value + "." + 
                  "<br />" +
                  "<h2 class='subtitle__route'>" + "Пункт призначення: " + "</h2>" + document.getElementById("to").value + "." +
                  "<br />" +
                  "<h2 class='subtitle__route'>" + "Відстань маршруту: " + "</h2>" + result.routes[0].legs[0].distance.text + "." +
                  "<br />" +
                  "<h2 class='subtitle__route'>" + "Тривалість " + "</h2>" + result.routes[0].legs[0].duration.text + "." +
               "</div>";
            const drivingValue = document.querySelector(".driving");
            drivingValue.innerHTML = "<div>" + result.routes[0].legs[0].distance.text + "</div>";
            const drivingTimeValue = document.querySelector(".driving-time");
            drivingTimeValue.innerHTML = "<div>" + result.routes[0].legs[0].duration.text + "</div>";
            fetch('/get_distance', {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify({
                    "distance": result.routes[0].legs[0].distance.text,
                })
            }).then(function (response) {
                return response.text()
            })
            directionsDisplay.setDirections(result);
        } else {
            directionsDisplay.setDirections({routes: []});
            map.setCenter(myLatLng);
            routeResult.innerHTML = "<div class='error'>Не вдалося отримати відстань</div>";
        }
    });
}

function getValueOfMode(mode, elementValue, elementTime) {
    var request = {
        origin: document.getElementById("from").value,
        destination: document.getElementById("to").value,
        travelMode: mode,
        unitSystem: google.maps.UnitSystem.METRIC
    }
    directionsService.route(request, function (result, status) {
        let elementValueTravelMode = document.querySelector(elementValue);
        let elementTimeTravelMode = document.querySelector(elementTime);
        if (status == google.maps.DirectionsStatus.OK) {
            elementValueTravelMode.innerHTML = "<div>" + result.routes[0].legs[0].distance.text + "</div>";
            elementTimeTravelMode.innerHTML = "<div>" + result.routes[0].legs[0].duration.text + "</div>";
        } else {
            elementValueTravelMode.innerHTML = "<div>" + "-" + "</div>";
            elementTimeTravelMode.innerHTML = "<div>" + "-" + "</div>";
        }
    });
}
var input1 = document.getElementById("from");
var input2 = document.getElementById("to");
const resultTable = document.querySelector(".route__table");
const fieldOfVehicle = document.querySelector("#user-vehicle")
const fieldOfChoice = document.querySelector("#choose-variant")
const layRoute = document.querySelector(".lay-a-route")
layRoute.addEventListener("click", function () {
   routingValue();
   getValueOfMode("TRANSIT", ".transit", ".transit-time");
   getValueOfMode("BICYCLING", ".bicycling", ".bicycling-time");
   getValueOfMode("WALKING", ".walking", ".walking-time");
   resultTable.classList.remove("none");
   fieldOfVehicle.classList.remove("none");
   fieldOfChoice.classList.remove("none");
})