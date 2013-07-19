$ ->
  if $('#brigade').length > 0
    map = L.mapbox.map('map', 'milafrerichs.map-ezn7qjpd').setView([0, 0], 2)
    markers = new L.MarkerClusterGroup()
    brigade_id = $('.page-id').data('id')
    brigade_locations_url = Routes.application_locations_brigade_path(brigade_id)
    $.get(brigade_locations_url).done (data) ->
      lat_lngs = []
      for application in data
        app = { 
          lat: application.location.latitude
          lng: application.location.longitude
          deployed: application.deployed
        }
        lat_lngs.push([app.lat,app.lng])
        marker = L.marker(new L.LatLng(app.lat,app.lng), {
                    icon: L.mapbox.marker.icon({'marker-symbol': 'town-hall'})
                })
        markers.addLayer(marker)
      map.addLayer(markers)
      map.fitBounds(lat_lngs)