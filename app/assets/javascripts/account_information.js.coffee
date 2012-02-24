$ ->
  $('#user_location_id').live 'change', (event) ->

    if $(@).val() is 'Add Location'

      $('#add_location_container').modal('show')

  $('form.new_location').bind 'ajax:success', (data, status, xhr) ->
    $('#add_location_container').modal('hide')
    $('#user_location_id option').removeAttr('selected')
    $('#user_location_id').append("<option value=\"#{status.id}\" selected='selected'>#{status.name}</option>")

  $('form.new_location').bind 'ajax:error', (xhr, status, error) ->
    # Going for the extremely simple solution until we decide how this will actually work - RMC
    alert "Name #{jQuery.parseJSON(status.responseText).name[0]}"
