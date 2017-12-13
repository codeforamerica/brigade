window.Brigade = window.Brigade || {};

window.Brigade.initializeMap = function(geoJSON) {
  // Provide your access token
  L.mapbox.accessToken = 'pk.eyJ1IjoiY29kZWZvcmFtZXJpY2EiLCJhIjoiSTZlTTZTcyJ9.3aSlHLNzvsTwK-CYfZsG_Q';

  // Create a map in the div #map
  var map = L.mapbox.map('map', 'codeforamerica.map-hhckoiuj');

  map.addControl(L.mapbox.geocoderControl('mapbox.places', { keepOpen: true, autocomplete : true }).setPosition('topright'));
  map.addEventListener('ready', function () {
    $('.leaflet-control-mapbox-geocoder-form input').attr("placeholder","Search map");
  });

  map.legendControl.setPosition('bottomright');
  map.legendControl.addLegend('<img src="https://www.codeforamerica.org/brigade/static/images/red-marker.png" style="vertical-align: middle;"><strong>Official Brigade</strong>');
  map.zoomControl.setPosition('topright');

  var latlon = [27, -85], zoom = 2;

  map.setView(latlon, zoom);
  map.featureLayer.setGeoJSON(geoJSON);

  map.featureLayer.on('click', function(e) {
    var brigadeName = e.layer.feature.properties.name;

    ga('send', 'event', {
      eventCategory: 'Map Click',
      eventAction: 'click',
      eventLabel: brigadeName,

      // see: https://developers.google.com/analytics/devguides/collection/analyticsjs/events
      // Supported in modern non-Safari browsers.
      transport: 'beacon'
    });

    var brigadeId = brigadeName.replace(/\s+/g, '-');
    window.open(brigadeId, "_self");
  });

  // Add hover tooltips with Brigade name to map markers
  map.featureLayer.eachLayer(function(layer) {
    layer.bindPopup(layer.feature.properties.name);
  });
  map.featureLayer.on('mouseover', function(e) {
    e.layer.openPopup();
  });
  map.featureLayer.on('mouseout', function(e) {
    e.layer.closePopup();
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

  // Track all link clicks as explicit events.
  //
  // The event's label will be given by either the <a title> attribute or the
  // link URL.
  //
  // Override the event's category with `data-target-category`, e.g.:
  //   <a data-target-category="Some Other Event Category">
  $(document).on('click', 'a', function(el) {
    const targetHref = el.target.href;
    const targetTitle = el.target.title;
    const targetCategory = el.target.dataset.analyticsCategory;
    const isExternal = !targetHref.startsWith(window.location.origin);

    ga('send', 'event', {
      eventCategory: targetCategory || (isExternal ? 'External Link Click' : 'Link Click'),
      eventAction: 'click',
      eventLabel: targetTitle || targetHref,

      // see: https://developers.google.com/analytics/devguides/collection/analyticsjs/events
      // Supported in modern non-Safari browsers.
      transport: 'beacon'
    })
  });
};

document.addEventListener('DOMContentLoaded', window.Brigade.init);
