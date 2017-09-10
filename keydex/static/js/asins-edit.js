$(document).ready(function() {
  var data = $('.data-keywords');
  var data_phrases = $('.data-phrases');
  var chips_data = []
  var phrases_data = [];
  for (var i = 0; i < data.length; i++) {
    chips_data.push( {tag: data[i].innerText });
  }
  for (var i = 0; i < data_phrases.length; i++) {
    phrases_data.push( {tag: data_phrases[i].innerText });
  }
  $('#div-1').material_chip();
  $('#div-1').material_chip({
    secondaryPlaceholder: 'Enter a keywords',
    data: chips_data
  });
  $('#div-1-counter').text(chips_data.length);
  $('#div-2').material_chip();
  $('#div-2').material_chip({
    secondaryPlaceholder: 'Enter phrases',
    data: phrases_data
  });
  $('#div-2-counter').text(phrases_data.length);
  
  $('select').material_select();
});
