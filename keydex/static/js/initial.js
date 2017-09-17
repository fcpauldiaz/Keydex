(function($){
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-104307868-1', 'auto');
  ga('send', 'pageview');
  $(function() {
    var messages = document.getElementsByClassName('message-body')
    for (var j = 0; j < messages.length; j++) {
      var m = messages[j]
      if (m.className.includes('error')) {
      Materialize.toast(m.innerText, 3000, 'error');  
      } else {
        Materialize.toast(m.innerText, 3000);
      }
     }
  }); // end of document ready
  
})(jQuery); // end of jQuery name space
