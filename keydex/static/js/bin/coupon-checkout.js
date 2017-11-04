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
      else {
        handler.open({
          description: name,
          zipCode: true,
          amount: total*100
        });
      }
     
    });
   
  
  });