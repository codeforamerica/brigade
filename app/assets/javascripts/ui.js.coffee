# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in home.js.
#

$ ->
  $('.inlinesparkline').each (index) ->
    $(this).sparkline $(this).parent().parent().parent().prev('#repository_participation').text().replace('[', '').replace(']', '').split(','),
      type: "discrete"
      lineColor: "#2d4611"

  #$('ul#user-grid li').mouseover ->
  #  name = $(this).data('name')
  #  $('#user-name').html(name)

  #$('ul#user-grid li').mouseout ->
  #  $('#user-name').html("")

  if $('#hacking_form #location').length > 0
    $('#hacking_form #location').autocomplete
      source: $('#hacking_form #location').data('autocomplete-source')

  $('input#location').focus()

  $('.deploy-button').click ->
    $(this).parent().addClass('active')
    console.log('Class added');