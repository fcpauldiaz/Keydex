$('[name="choices_group2"]').on('change', function(e) {
  var value = e.currentTarget.attributes.value.value;
  var group3 = $('[name="choices_group3"]');
  if (value === 'type5') {
    for (i = 0; i < group3.length; i ++) {
      group3[i].checked = false;
      $('#group3_choices').hide();
    }
  }
  if (value === 'type6') {
    var force = true;
    for (i = 0; i < group3.length; i++) {
      var current = group3[i].checked;
      if (current === true) {
        force = false;
      }
    }
    if (force === true) {
      var choices = $('#id_choices_group3_0');
      choices[0].checked = true;
      $('#group3_choices').show();

    }
  }
});
$('[name="choices_group3"]').on('change', function(e) {
  var value = e.currentTarget.attributes.value.value;
  if (value === 'type7' || value === 'type8' 
    || value === 'type9' || value === 'type10') { 
    var op1 = $('#id_choices_group2_0')[0]
    var op2 = $('#id_choices_group2_1')[0]
    if (op1.checked === true || op2.checked === false) {
      op2.checked = true;
      op1.checked = false;
    }
  }
});