function initMap(){
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 	18.200178, lng: -66.44513},
        zoom: 10,
        mapId: '122517338e1e4a8'
        });
    
    locations = getLocations()
    locations.forEach(cordinate_str => {
        cordinate_lst = cordinate_str.split(',')
        lat = parseFloat(cordinate_lst[0])
        long = parseFloat(cordinate_lst[1])
        cordinate = { lat: lat, lng: long };
        new google.maps.Marker({
            position: cordinate,
            map: map,
          });
    });
}

function getLocations(){
    cords = []
    doctors = document.querySelectorAll(".doctor")
    doctors.forEach(doctor => {
        cords.push(doctor.getAttribute("data-geo"))
    });
    return cords
}

$(function () {
    var selectedDates = [];
    datePicker = $('[id*=txtdate]').datepicker({
        startDate: new Date(),
        minDate: 0,
        multidate: false,
        format: "mm/dd/yyyy",
        daysOfWeekHighlighted: "0,6",
        language: 'en',
        daysOfWeekDisabled: [0, 6]
    });
});