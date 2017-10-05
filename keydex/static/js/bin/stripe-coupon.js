$(document).ready(function() {
  $('.modal').modal();
  $('select').material_select();
  $('input[name=coupon]').change(function() {
    $('#loader').show();
    $('#submitbutton').hide();
    formpay = $('#payment-form');
    $.ajax({
      url: formpay.attr("data-coupon-url"),
      type : "POST",
      data: formpay.serialize(),
      dataType: 'json',
      success: function (data) {
        if (data.valid_coupon === true) {
          $('#showTotal').text('Total: ' + data.total_amount + ' with discount applied');
          $('#showTotal').show();
          $('#loader').hide();
          $('#submitbutton').show();
        }
        else {
          $('#showTotal').text('Invalid coupon');
          $('#showTotal').show();
          $('#loader').hide();
          $('#submitbutton').show();
        }
      },
      error: function(request, status, error) {
        Materialize.toast('Server error', 3000);
        console.log(error);
      }
    });
  });
});