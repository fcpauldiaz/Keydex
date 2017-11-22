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
$(document).ready(function() {
    $('.modal').modal();
    $('select').material_select();
    var handler = StripeCheckout.configure({
      key: $('#payment-form').attr('data-stripe-key'),
      image: "https://s3-us-west-2.amazonaws.com/stripe-checkmykeywords/quack-s3.png",
      name: "Check My Keywords",
      panelLabel: "Subscribe",
      allowRememberMe: false,
      locale: 'auto',
      token: function(token) {
        $('#loader').hide();
        $('#submitbutton').show();
        // Send the token to your server
        formpay = $('#payment-form');
        var data = formpay.serializeArray();
        data.push(
          { name:   'plan',  value: formpay.data('subscription_plan') },
        );
        data = jQuery.param(data);
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
            Materialize.toast('Request error', 3000);
            $('#loader').hide();
            $('#submitbutton').show();
          }
        });
      }
    });
    var button = $('.data-monthly, .data-yearly');
    var mobile = $('#mobile-signup');
    mobile.on('click', function (event) {
      event.preventDefault();
      $('#loader').show();
      $('#mobile-signup').hide();
      var value = $('#mobile-stripe option:selected').val();
      if (value !== null && value !== undefined && value !== '') {
        formpay = $('#payment-form');
        formpay.data('subscription_plan', value);
        var charge_value = 5000;
        var name = 'Invalid option';
        if (value == 'Monthly') {
          name = 'Monthly ($5)';
          charge_value = 500;
        }
        if (value == 'Yearly') {
          charge_value = 5000;
          name = 'Yearly ($50)'
        }
        handler.open({
          description: name,
          zipCode: true,
          amount: charge_value
        });
      }
      // get selected
    })
    for (var i = 0; i < button.length; i++) {
     button[i].addEventListener("click", function(event) {
      event.preventDefault();
      $('#loader').show();
      $('.data-yearly').hide();
      $('.data-monthly').hide();
      setInterval(function(){
        $('#loader').hide();
          $('.data-yearly').show();
          $('.data-monthly').show();
      }, 2000);
      formpay = $('#payment-form');
      var name = 'Yearly Plan ($50 per year)';
      var value = 1;
      var charge_value = 5000;
      var dataClass = $(this).attr('class').split(' ')[0].trim();
      if (dataClass === 'data-yearly') {
        name = 'Yearly Plan ($50 per year)';
        formpay.data('subscription_plan', 'Yearly');
        charge_value = 5000;
      }
      else if (dataClass === 'data-monthly') {
        name = 'Monthly Plan ($5 per month)';
        formpay.data('subscription_plan', 'Monthly');
        value = 1;
        charge_value = 500;
      }
      handler.open({
        description: name,
        zipCode: true,
        amount: charge_value
      });

    });
   }
  });