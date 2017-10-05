// Create a Stripe client
var stripe = Stripe($('#payment-form').attr('data-stripe-key'));

// Create an instance of Elements
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
var style = {
  base: {
    color: '#32325d',
    lineHeight: '24px',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
    $('#submitbutton').addClass('disabled');
  } else {
    displayError.textContent = '';
    $('#submitbutton').removeClass('disabled');
  }
});

// Handle form submission
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  $('#loader').show();
  $('#submitbutton').hide();
  var extraDetails = {
    name: form.querySelector('input[name=cardholder-name]').value,
  };
  stripe.createToken(card, extraDetails).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
      $('#loader').hide();
      $('#submitbutton').show();
    
    } else {
      // Send the token to your server
      formpay = $('#payment-form');
      $.ajax({
        url: formpay.attr("data-settings-url"),
        type : "POST",
        data: formpay.serialize() + '&token='+ JSON.stringify(result.token),
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
    }
  });
});