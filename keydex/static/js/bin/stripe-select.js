var selected = undefined;
var discount = undefined;
var total = undefined;
var name = undefined;
$('.data-yearly').on('click', function(e){
e.preventDefault();
$(this).css('border', 'solid 4px blue');
$('#pricing_DIV_5').css('width', '261px');
$('#DIV_5').css('width', '269px');
$('#DIV_1_upgrade').css('border', 'none');
if (discount == undefined) {
  $('#showTotal').text('Total:' + ' $50');
  total = 50;
} 
else {
  total = 50-(50*parseFloat(discount));
  $('#showTotal').text('Total:' + ' $'+total);
}
selected = 'Yearly';
name = 'Yearly ($50)';

$('#coupon').removeClass('valid');
});
$('.data-monthly').on('click', function(e){
e.preventDefault();
$(this).css('border', 'solid 4px blue');
$('#DIV_5').css('width', '261px');
$('#pricing_DIV_5').css('width', '269px');
$('#pricing_DIV_1_upgrade').css('border', 'none');
if (discount == undefined) {
  $('#showTotal').text('Total:' + ' $5');
  total = 5;
}
else {
  total = 5-(5*parseFloat(discount));
  $('#showTotal').text('Total:' + ' $'+total);
}
selected = 'Monthly';
name = 'Monthly ($5)';
$('#coupon').removeClass('valid');
    });