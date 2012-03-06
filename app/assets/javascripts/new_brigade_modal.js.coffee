$ ->
  $('select.brigade-selector').live 'change', (event) ->

    if $(@).val() is 'Add Brigade'

      $('#add_brigade_container').modal('show')

  $('form.new_brigade').bind 'ajax:success', (data, status, xhr) ->
    $('#add_brigade_container').modal('hide')
    $('select.brigade-selector option').removeAttr('selected')
    $('select.brigade-selector').append("<option value=\"#{status.id}\" selected='selected'>#{status.name}</option>")

  $('form.new_brigade').bind 'ajax:error', (xhr, status, error) ->
    # Going for the extremely simple solution until we decide how this will actually work - RMC
    alert "Name #{jQuery.parseJSON(status.responseText).name[0]}"
