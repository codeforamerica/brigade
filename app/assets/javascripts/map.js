$(function(){

  var map = L.mapbox.map('map', 'codeforamerica.map-hhckoiuj', {scrollWheelZoom:false})
  var lat_lngs = [];
  $.getJSON("/brigades.json", function(data){
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
});




