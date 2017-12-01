
$(document).ready(function(){
  // Add smooth scrolling to all links in navbar + footer link
  $("#nav a").on('click', function(event) {

  // Make sure this.hash has a value before overriding default behavior
  if (this.hash !== "") {

    // Prevent default anchor click behavior
    event.preventDefault();
    $("#nav a").removeClass('active');
    $(this).addClass('active');
    

    // Store hash
    var hash = this.hash;

    // Using jQuery's animate() method to add smooth page scroll
    // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
    $('html, body').animate({
      scrollTop: $(hash).offset().top
    }, 900, function(){

      // Add hash (#) to URL when done scrolling (default click behavior)
      window.location.hash = hash;
      });
    } // End if 
  });
  
  $("#nav3 a, .footer-up a").on('click', function(event) {

  // Make sure this.hash has a value before overriding default behavior
  if (this.hash !== "") {

    // Prevent default anchor click behavior
    event.preventDefault();
    

    // Store hash
    var hash = this.hash;

    // Using jQuery's animate() method to add smooth page scroll
    // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
    $('html, body').animate({
      scrollTop: $(hash).offset().top
    }, 900, function(){

      // Add hash (#) to URL when done scrolling (default click behavior)
      window.location.hash = hash;
      });
    } // End if 
  });
  
  
  //scroll enimation
  
  $(window).scroll(function() {
  $(".slideanim").each(function(){
    var pos = $(this).offset().top;

    var winTop = $(window).scrollTop();
    if (pos < winTop + 600) {
      $(this).addClass("animated fadeInDown visible");
    }
  });
});

$(window).scroll(function() {
  $(".none").each(function(){
    var pos = $(this).offset().top;

    var winTop = $(window).scrollTop();
    if (pos < winTop - 200) {
      $(this).addClass("animated fadeInUp yeap");
    }
  });
});

$(window).scroll(function() {
  $(".non").each(function(){
    var pos = $(this).offset().top;

    var winTop = $(window).scrollTop();
    if (pos < winTop - 1000) {
      $(this).addClass("animated fadeInUp yeap");
    }
  });
});

//counte down
var clock;

			

				// Grab the current date
				var currentDate = new Date();

				// Set some date in the future. In this case, it's always Jan 1
				var futureDate  = new Date(currentDate.getFullYear(), 11, 9);

				// Calculate the difference in seconds between the future and current date
				var diff = futureDate.getTime() / 1000 - currentDate.getTime() / 1000;

				// Instantiate a coutdown FlipClock
				clock = $('.clock').FlipClock(diff, {
					clockFace: 'DailyCounter',
					countdown: true
				});
			
			
			
			
			$('#nav1 a[href="#myPage"]').click(function(){
				$('#about').addClass('no');
				$('#hh').addClass('no');
				$('#beta').removeClass('no');
				$('#bb').removeClass('no');
			});
			
			$('#nav1 a[href="#about"]').click(function(){
				$('#about').removeClass('no');
				$('#hh').removeClass('no');
				$('#beta').addClass('no');
				$('#bb').addClass('no');
			});
  
  
  

 
});

 $(function () {
            
            // $('#counter').mbComingsoon({ expiryDate: new Date(2017, 11, 9, 0, 0), speed:100 });
            // setTimeout(function () {
            //     $(window).resize();
            // }, 200);
        });
        



  	
  	
