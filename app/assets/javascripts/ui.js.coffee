# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in home.js.
#

$ ->
  $('#hacking_form #location').autocomplete
    source: $('#hacking_form #location').data('autocomplete-source')
