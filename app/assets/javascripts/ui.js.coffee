# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in home.js.

$ ->
		data = [2,3,4,5,5,7,6,5,4,2,2,3,4,5,5,7,9,5,3,2,2,3]
		console.log(data);
  $('.inlinesparkline').sparkline data,
  	type: "bar"
  	barColor: "#a1997e"

