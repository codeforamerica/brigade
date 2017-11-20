window.Brigade = window.Brigade || {};

window.Brigade.initializeMap = function(geoJSON) {
  // Provide your access token
  L.mapbox.accessToken = 'pk.eyJ1IjoiY29kZWZvcmFtZXJpY2EiLCJhIjoiSTZlTTZTcyJ9.3aSlHLNzvsTwK-CYfZsG_Q';

  // Create a map in the div #map
  var map = L.mapbox.map('map', 'codeforamerica.map-hhckoiuj');

  map.legendControl.setPosition('topright');
  map.legendControl.addLegend('<img src="https://www.codeforamerica.org/brigade/static/images/red-marker.png" style="vertical-align: middle;"><strong>Official Brigade</strong>');
  map.zoomControl.setPosition('topright');

  var latlon = [27, -85], zoom = 2;

  map.setView(latlon, zoom);
  map.featureLayer.setGeoJSON(geoJSON);

  map.featureLayer.on('click', function(e) {
    var brigadeId = e.layer.feature.properties.name.replace(/\s+/g, '-');
    window.open(brigadeId, "_self");
  });
};

window.Brigade.initializeProjects = function(id, query, status) {
  $(id).masonry({
    itemSelector: '.project',
    "gutter" : 20
  });

  if (query) {
    ga('send', 'event', 'Project Search', 'search', query, 1);
  }

  if (status) {
    ga('send', 'event', 'Project Search', 'search', status, 1);
  }
};

window.Brigade.init = function() {
  // Generate list of brigades
  if ($(window).width() > 480){
    $('#map').css("height", $(window).height() - $(".global-header").height() - 1);
    $('#overlay').css("height", ($(window).height() - $(".global-header").height()));
  }
};

document.addEventListener('DOMContentLoaded', window.Brigade.init);
