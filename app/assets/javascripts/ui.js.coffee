# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in home.js.

$(document).ready ->
  $('#app-spinner dl').hover ->
    $(this).animate({'opacity':'0.6'})
