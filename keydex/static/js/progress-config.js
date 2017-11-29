function initProgress() {
  var container = document.getElementById('progress');
  var bar = new ProgressBar.Line(container, {
  strokeWidth: 4,
  easing: 'easeInOut',
  duration: 0,
  color: '#4094ED',
  trailColor: '#eee',
  trailWidth: 0,
  svgStyle: {width: '100%', height: '100%'},
  text: {
    style: {
      color: '#000000',
      position: 'absolute',
      left: '60px',
      top: '90px',
      'font-size': '22px',
      padding: 0,
      margin: 0,
      transform: null
    },
    autoStyleContainer: false
  },
  from: {color: '#e51c23'},
  to: {color: '#177FEF'},
  step: (state, bar) => {
      bar.path.setAttribute('stroke', state.color);
      bar.path.setAttribute('stroke-width', state.width);

      var value = Math.round(bar.value() * 100);
      if (value === 0) {
        bar.setText('');
      } else {
        bar.setText(value);
      }
  }
  });
  bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
  bar.text.style.fontSize = '2rem';
  return bar;
}