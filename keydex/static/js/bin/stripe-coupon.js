$(document).ready(function() {
  $('#coupon').on('change', function(e) {
    e.preventDefault();
    $.ajax({
      url: formpay.attr("data-settings-url"),
      type : "POST",
      data: data + '&token='+ JSON.stringify(token),
      dataType: 'json',
      success: function (data) {
        if (data.valid === true) {
          Materialize.toast('Payment Accepted', 3000);
          $('#loader').hide();
          $('#submitbutton').show();
          $('#modal1').modal('close');
          Materialize.toast('Upgrading Account', 3000);
          location.reload();
        }
        else {
          var errorElement = document.getElementById('card-errors');
          errorElement.textContent = data.message;
          $('#loader').hide();
          $('#submitbutton').show();
        }
      },
      error: function(request, status, error) {
        Materialize.toast('Server error', 3000);
        $('#loader').hide();
        $('#submitbutton').show();
      }
    });
  });
});