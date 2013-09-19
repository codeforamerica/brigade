
$(function() {
  var brigade_id, brigade_locations_url, map, markers;
    if ((brigade_id = $('#map').data('target'))) {
    map = L.mapbox.map('map', 'codeforamerica.map-hhckoiuj', {attributionControl: false});
    $.getJSON("/brigades/"+ brigade_id +".json", function(data){
      console.log(data)

      for(d in data){
        var brigade = data[d]
        if(brigade.location){

          if(brigade.location.latitude && brigade.location.longitude){
            var lat = brigade.location.latitude;
            var lng = brigade.location.longitude;
            
            lat_lngs.push([lat,lng])

            marker = L.marker(new L.LatLng(lat,lng), {
              icon: L.mapbox.marker.icon({'marker-symbol': 'town-hall'})
            })
            marker.bindPopup("<a href='/brigades/"+brigade.id+"'>"+brigade.name+" - "+brigade.location.name+"</a>");
            map.addLayer(marker);
          }
        } 
      }
      console.log(lat_lngs)
      map.fitBounds(lat_lngs, {padding:[40,40]})
    });
  }
  if ($('#brigades').length > 0) {
    console.log("inside loop 2");
    map = L.mapbox.map('map', 'codeforamerica.map-hhckoiuj', {attributionControl: false}).setView([0, 0], 2);
    markers = new L.MarkerClusterGroup();
    brigade_locations_url = Routes.locations_brigades_path();
    return $.get(brigade_locations_url).done(function(data) {
      var brigade, lat, lat_lngs, lng, location, marker, name, _i, _len;
      lat_lngs = [];
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        brigade = data[_i];
        if (brigade.location) {
          lat = brigade.location.latitude;
          lng = brigade.location.longitude;
          name = brigade.name;
          location = brigade.location.name;
          if (lat && lng) {
            lat_lngs.push([lat, lng]);
            marker = L.marker(new L.LatLng(lat, lng), {
              icon: L.mapbox.marker.icon({
                'marker-symbol': 'town-hall'
              })
            });
            marker.bindPopup("" + name + "<br/>" + location);
            markers.addLayer(marker);
          }
        }
      }
      map.addLayer(markers);
      return map.fitBounds(lat_lngs);
    });
  }
});