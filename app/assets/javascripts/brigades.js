$(function(){
  var brigade_id = $('#map').data('target');
  var map = L.mapbox.map('map', 'codeforamerica.map-hhckoiuj', {scrollWheelZoom:false, attributionControl: false});
  var lat_lngs = [];
  if($("div#map.brigades").length > 0){

    $.getJSON("/brigades.json", function(data){
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
      map.fitBounds(lat_lngs, {padding:[40,40]})
    });



  }else if($("div#map.brigade").length > 0){

    $.getJSON("/brigades/"+brigade_id+".json", function(brigade){
      if(brigade.location){

        if(brigade.location.latitude && brigade.location.longitude){
          var lat = brigade.location.latitude;
          var lng = brigade.location.longitude;
          
          marker = L.marker(new L.LatLng(lat,lng), {
            icon: L.mapbox.marker.icon({'marker-symbol': 'town-hall'})
          });
          //marker.bindPopup("<a href='/brigades/"+brigade.id+"'>"+brigade.name+" - "+brigade.location.name+"</a>");
          map.addLayer(marker);

        }
      } 
      
      map.setView([lat,lng], 8);
    });

  }
});

