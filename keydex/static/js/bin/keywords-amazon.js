  var data = [];
  $('#textarea').keyup(function(event) {
    var type = $('#select_type').find(":selected").val();
    if (event.keyCode === 32 && type === 'keyword') {
      var txt = $('#textarea')
      txt.val(txt.val() + "\n");
    }

  });
  $('form').on('submit', function(event) {
    event.preventDefault();
    var lines = this.textarea.value.split('\n');
    var type = $('select').find(":selected").text();
    if (lines.length === 0 && this.textarea.value !== '' && data.length <= 250 && !data.includes(this.textarea.value.toLowerCase())) {
      var row = table.insertRow(-1);
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      var cell3 = row .insertCell(2);
      cell1.innerHTML = this.textarea.value.trim().replace(/[^\x00-\x7F]/g, "");
      cell2.innerHTML = type;
      cell3.innerHTML = "<td><i class='small material-icons'>close</i></td>";
    }
    var table = document.getElementById('table');
    for(var i = 0; i < lines.length; i++) {
      var text = lines[i].trim().replace(/[^\x00-\x7F]/g, "");;
      if (text === '' || data.includes(text.toLowerCase())) {
        continue;
      }
      if (data.length > 250) {
        Materialize.toast('Reached maximum 250 keywords for a product', 3000);
        continue;
      }
      
      var row = table.insertRow(-1);
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      var cell3 = row .insertCell(2);
      cell1.innerHTML = lines[i];
      cell2.innerHTML = type;
      cell3.innerHTML = "<td><i class='small material-icons'>close</i></td>";
      data.push(text.toLowerCase());
    }
    this.textarea.value = '';
  });
  $(document).on('click', '.material-icons', function(event) {
    var p = $(this).closest('tr');
    var tds = p[0].getElementsByTagName('td');
    var index = data.indexOf(tds[0].innerHTML.trim());
    if (index > -1) {
      data.splice(index, 1);
    }
    var deleteRow = $(this).closest('tr').index()
    var table = document.getElementById('table');
    var row = table.deleteRow(deleteRow);
  });
  $('select').on('change', function() {
    var txt = $('#textarea')
    txt.val('');
    var type = $('#select_type').find(':selected').val();
    if (type === 'phrase') {
      txt.prop('placeholder', "Copy paste here your phrases \nOne phrase per line");
    } else {
      txt.prop('placeholder', 'Copy paste here your keywords \nOne keyword per line');
    }
  });
  $('#textarea').bind('paste', function() {
    setTimeout(function() {
      var type = $('#select_type').find(':selected').val();
      if (type === 'keyword') {
        var txt = $('#textarea');
        var splitted = txt.val().split(' ');
        for (i = 0; i < splitted.length; i++) {
          if (i === 0) {
            txt.val(splitted[i].toLowerCase().replace(/[^\x00-\x7F]/g, " ") + "\n");
          } else {
            txt.val(txt.val() + splitted[i].toLowerCase().replace(/[^\x00-\x7F]/g, " ") + "\n");
          }
        }
      }
    }, 20);
  });

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
$("#finish").on("click", function (e) {  
    e.preventDefault();
    $('#chip-button').hide();
    $('#loader').show();
    table = document.getElementById('table');
    var keywords = [];
    var phrases = [];
    for (var i = 0; i < table.rows.length; i++) {
      var tds = table.rows[i].getElementsByTagName('td');

      if (tds[1].innerText === 'Keyword' && !keywords.includes(tds[1].innerText)) {
        keywords.push(tds[0].innerText);
      }
      else if (tds[1].innerText === 'Phrase' && !phrases.includes(tds[1].innerText)) {
        phrases.push(tds[0].innerText);
      }
    }
    var form = $('form');
    $.ajax({
      url: form.attr("data-keywords-url"),
      type : "POST",
      data: { 
        csrfmiddlewaretoken : getCookie('csrftoken'), 
        chips_keywords: JSON.stringify(keywords),
        chips_phrases: JSON.stringify(phrases) 
      },
      dataType: 'json',
      success: function (data) {
        var data_key = JSON.parse(data.data_key);
        var data_phrase = JSON.parse(data.data_phrase)
        if (data_key.length === 0 && data_phrase.length === 0) {
          Materialize.toast('Please add some keywords', 3000);
          $('#chip-button').show();
          $('#loader').hide();
        }
        else {
          window.location.href = '/product/save/';
        }
      },
      error: function(request, status, error) {
        console.log(error);
      }
    });

  });