window.Brigade = window.Brigade || {};

window.Brigade.initializeMap = function(geoJSON) {
  // Provide your access token
  L.mapbox.accessToken = 'pk.eyJ1IjoiY29kZWZvcmFtZXJpY2EiLCJhIjoiY2pldDMwMzlnMHF3ZjMzbzUyMzNpdms4MSJ9.ZN9PlYN-2GGF_HQtY0zWWw';

  // Create a map in the div #map
  var map = L.mapbox.map('map', 'codeforamerica.map-hhckoiuj', {
    tileLayer: false,
  });

  L.mapbox.styleLayer('mapbox://styles/mapbox/bright-v8')
    .addTo(map);

  var geocoderControl = L.mapbox.geocoderControl('mapbox.places', {
    keepOpen: true,
    autocomplete : true,
    queryOptions: {
      country: "us"
    }
  });
  geocoderControl.setPosition('topright');
  geocoderControl.addTo(map);

  /*
   * Disable scrolling until the user moves the mouse over the map for the
   * first time. This should hopefully result in users scrolling past the map
   * when using a scroll wheel if they don't move the mouse.
   */
  map.scrollWheelZoom.disable();
  map.addEventListener('mousemove', function() {
    if (!map.scrollWheelZoom.enabled()) {
      map.scrollWheelZoom.enable();
    }
  });

  map.addEventListener('ready', function() {
    $('.leaflet-control-mapbox-geocoder-form input').attr("placeholder","Search map");

    // After selecting a geocoder result, replace the search text with the place name and hide the geocoder results
    geocoderControl.on('select', function(result){
      $('#map input').val(result.feature.place_name);
      $('#map .leaflet-control-mapbox-geocoder-results').hide();
    });

    // Make sure the geocoder results are showing when input is entered into geocoder search
    $('#map input').keyup(function(){
      $('#map .leaflet-control-mapbox-geocoder-results').show();
    });

    // Prevent the page from jumping to the top when clicking on the geocoder 'searchglass' icon
    $('a.leaflet-control-mapbox-geocoder-toggle').on('click', function(event){
      event.preventDefault();
    });
  });

  map.zoomControl.setPosition('topright');

  var latlon = [44, -98], zoom = 3;

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

    var brigadeSlug = brigadeName.replace(/\s+/g, '-');
    window.open('/brigades/' + brigadeSlug, "_self");
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


  // Handle toggling the mobile nav. Copied from the v4 style guide.
  $(document).on('click', '.global-header a.js-toggle-mobile-navigation', function(e) {
    e.preventDefault();
    $('body').toggleClass('mobile-navigation-is-active');
  });
};

// Enable smooth scrolling for on-page links
// Taken from: https://css-tricks.com/snippets/jquery/smooth-scrolling/
$('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') &&
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex', '-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
  });

document.addEventListener('DOMContentLoaded', window.Brigade.init);
