$(document).ready(function() {
  var data = $('.data-chips');
  var chips_data = []
  for (var i = 0; i < data.length; i++) {
    chips_data.push( {tag: data[i].innerText });
  }
  console.log(chips_data)
  $('.chips').material_chip();
  $('.chips-placeholder').material_chip({
    placeholder: '+Keyword',
    secondaryPlaceholder: 'Enter a keyword',
    data: chips_data
  });
  $('select').material_select();
});
