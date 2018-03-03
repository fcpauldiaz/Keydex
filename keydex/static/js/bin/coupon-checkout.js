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
    var handler = StripeCheckout.configure({
      key: $('#payment-form').attr('data-stripe-key'),
      image: "https://s3-us-west-2.amazonaws.com/stripe-checkmykeywords/quack-s3.png",
      name: "Check My Keywords",
      panelLabel: "Subscribe",
      allowRememberMe: false,
      locale: 'auto',
      token: function(token) {
        $('#loader').show();
        $('#subscribe').hide();
        // Send the token to your server
        formpay = $('#payment-form');
        $.ajax({
          url: formpay.attr("data-upgrade-url"),
          type : "POST",
          data: { 
            csrfmiddlewaretoken : getCookie('csrftoken'), 
            coupon: $('#coupon').val(),
            plan: selected,
            token_id: token['id']
          },
          dataType: 'json',
          success: function (data) {
            if (data.valid === true) {
              Materialize.toast('Payment Accepted', 3000);
              $('#loader').hide();
              $('#subscribe').show();
              Materialize.toast('Upgrading Account', 3000);
              window.location = '/';
            }
            else { 
              Materialize.toast('Invalid transaction', 3000);
              $('#loader').hide();
              $('#subscribe').show();
            }
          },
          error: function(request, status, error) {
            Materialize.toast('Request error', 3000);
            $('#loader').hide();
            $('#subscribe').show();
          }
        });
      }
    });

    document.getElementById('subscribe').addEventListener('click', function (event) {
      event.preventDefault();
      
      if (total == undefined && name == 'undefined') {
        Materialize.toast('Please select a plan', 3000);
      }
      else if (total >= 1){
        handler.open({
          description: name,
          zipCode: true,
          amount: total*100
        });
      }
      else {
        $('#loader').show();
        $('#subscribe').hide();
        formpay = $('#payment-form');
        $.ajax({
          url: formpay.attr("data-free-url"),
          type : "POST",
          data: { 
            csrfmiddlewaretoken : getCookie('csrftoken'), 
            coupon: $('#coupon').val(),
            plan: selected
          },
          dataType: 'json',
          success: function (data) {
            if (data.valid === true) {
              ga('send', 'event', 'subscription', 'confirm subscription');
              Materialize.toast('Payment Accepted', 3000);
              $('#loader').hide();
              $('#subscribe').show();
              Materialize.toast('Upgrading Account', 3000);
              window.location = '/';
            }
            else { 
              ga('send', 'event', 'subscription', 'invalid subscription');
              Materialize.toast('Invalid transaction', 3000);
              $('#loader').hide();
              $('#subscribe').show();
            }
          },
          error: function(request, status, error) {
            Materialize.toast('Request error', 3000);
            $('#loader').hide();
            $('#subscribe').show();
          }
        });
      }
     
    });
   
  
  });