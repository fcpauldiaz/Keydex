Array.prototype.contains = function(element){
    return this.indexOf(element) > -1;
  }
function search() {
  var txt = document.getElementById('search-criteria').value;
  var divs = document.querySelectorAll('.searchable');
  var foundIds = [];
  Array.prototype.forEach.call(divs, function(element, index) {
    text = element.innerText || element.textContent;
    id = element.getAttribute('data-product');
    if (text.toLowerCase().indexOf(txt.toLowerCase()) == -1 ) {
      //hide
      if (!foundIds.contains(id)) {
        document.getElementById(id).style.display = 'none';
      }
    } else {
      document.getElementById(id).style.display = 'block';
      foundIds.push(id);
    }
    
  });
}