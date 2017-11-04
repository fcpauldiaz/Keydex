$(document).ready(function() {
  //For getting CSRF token
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
           var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
         }
        }
      }
    return cookieValue;
  }
  $('#coupon').on('keyup', function(e) {
    e.preventDefault();
    if (selected === undefined) {
      Materialize.toast('Please click a plan to select', 3000);
      $('#coupon').addClass('invalid');
    } else {
      var formpay = $('#payment-form');
      $.ajax({
        url: formpay.attr("data-settings-url"),
        type : "POST",
        data: { 
          csrfmiddlewaretoken : getCookie('csrftoken'), 
          coupon: $(this).val().toUpperCase(),
          plan: selected
        },
        dataType: 'json',
        success: function (data) {
          if (data.valid_coupon === true) {
            $('#coupon').addClass('valid');
            $('#showTotal').text('Total:' + ' $' + data.total_amount);
            discount = data.discount
            total = data.total_amount
          }
          else {
            $('#coupon').addClass('invalid');
            if (selected == 'Yearly') {
              $('#showTotal').text('Total:' + ' $50');
              discount = 0;
            }
            if (selected == 'Monthly') {
              $('#showTotal').text('Total:' + ' $5');
              discount = 0;
            }
          }
        },
        error: function(request, status, error) {
          Materialize.toast('Server error', 3000);
          $('#loader').hide();
          $('#submitbutton').show();
        }
      });
    }
  });
});