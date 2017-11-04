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
            console.log(data);
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
      console.log(total, name);
      if (total == undefined && name == 'undefined') {
        Materialize.toast('Please select a plan', 3000);
      }
      else {
        handler.open({
          description: name,
          zipCode: true,
          amount: total*100
        });
      }
     
    });
   
  
  });