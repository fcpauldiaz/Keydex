// Create a Stripe client
var stripe = Stripe('pk_test_ErbhTwsusQbKZNGHYnlAVsCj');

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
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  var extraDetails = {
    name: form.querySelector('input[name=credit_card_name]').value,
  };
  stripe.createToken(card, extraDetails).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server
      $('#save').hide();
      $('#loader').show();
      form = $('#payment-form');
      $.ajax({
        url: form.attr("data-settings-url"),
        type : "POST",
        data: form.serialize() + '&token='+ JSON.stringify(result.token),
        dataType: 'json',
        success: function (data) {
          if (data.data === 'ok') {
            Materialize.toast('Settings updated', 3000);
            $('#save').show();
            $('#loader').hide();
          }
          else {
            Materialize.toast('An error ocurred', 3000);
            $('#save').show();
            $('#loader').hide();
          }
        },
        error: function(request, status, error) {
          Materialize.toast('Server error', 3000);
          $('#save').show();
          $('#loader').hide();
        }
      });
    }
  });
});