$('[name="choices_group2"]').on('change', function(e) {
    var value = e.currentTarget.attributes.value.value;
    var group3 = $('[name="choices_group3"]');
    if (value === 'type5') {
      for (i = 0; i < group3.length; i ++){
        group3[i].checked = false;
      }
    }
});