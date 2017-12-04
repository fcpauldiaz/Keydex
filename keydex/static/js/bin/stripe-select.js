var selected = 'Monthly';
var discount = undefined;
var total = 10;
var name = undefined;
$('.data-monthly').css('border', 'solid 4px blue');
$('#DIV_5').css('width', '261px');
$('#pricing_DIV_5').css('width', '269px');
$('#pricing_DIV_1_upgrade').css('border', 'none');
$('#showTotal').text('Total:' + ' $'+total);

$('.data-yearly').on('click', function(e){
  e.preventDefault();
  $(this).css('border', 'solid 4px blue');
  $('#pricing_DIV_5').css('width', '261px');
  $('#DIV_5').css('width', '269px');
  $('#DIV_1_upgrade').css('border', 'none');
  if (discount == undefined) {
    $('#showTotal').text('Total:' + ' $100');
    total = 100;
  } 
  else {
    total = 100-(100*parseFloat(discount));
    $('#showTotal').text('Total:' + ' $'+total);
  }
  selected = 'Yearly';
  name = 'Yearly ($'+total+')';

  $('#coupon').removeClass('valid');
});
$('.data-monthly').on('click', function(e){
  e.preventDefault();
  $(this).css('border', 'solid 4px blue');
  $('#DIV_5').css('width', '261px');
  $('#pricing_DIV_5').css('width', '269px');
  $('#pricing_DIV_1_upgrade').css('border', 'none');
  if (discount == undefined) {
    $('#showTotal').text('Total:' + ' $10');
    total = 10;
  }
  else {
    total = 10-(10*parseFloat(discount));
    $('#showTotal').text('Total:' + ' $'+total);
  }
  name = 'Monthly ($'+total+')';
  selected = 'Monthly';
  
  $('#coupon').removeClass('valid');
});
$('select').on('change', function() {
  selected = this.value;
  $('#coupon').removeClass('valid');
  if (selected == 'Monthly') {
    if (discount == undefined) {
      $('#showTotal').text('Total:' + ' $10');
      total = 10;
    }
    else {
      total = 10-(10*parseFloat(discount));
      $('#showTotal').text('Total:' + ' $'+total);
    }
    name = 'Monthly ($'+total+')';
  }
  else if (selected == 'Yearly') {
    
    if (discount == undefined) {
      $('#showTotal').text('Total:' + ' $100');
      total = 100;
    } 
    else {
      total = 100-(100*parseFloat(discount));
      $('#showTotal').text('Total:' + ' $'+total);
    }
    name = 'Yearly ($'+total+')';
  }
  else {
    name = 'Invalid';
  }
});
$('select').on('click',function(ev){
  $('#coupon').removeClass('valid');
});
