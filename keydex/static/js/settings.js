function userData() {
  if (document.getElementById('test6').checked) 
  {
    var first = document.getElementById('id_first_name');
    var second = document.getElementById('id_last_name');
    document.getElementById('id_credit_card_name').value = first.value + ' ' + second.value;
  } else {
    document.getElementById('id_credit_card_name').value = '';

  }
}
function revealStripe() {
  $('#card-element').show();
  $('.card_hide').hide(); 
}
