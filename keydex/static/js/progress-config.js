function initProgress() {
  var container = document.getElementById('progress');
  var bar = new ProgressBar.Line(container, {
  strokeWidth: 4,
  easing: 'easeInOut',
  duration: 1400,
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
  from: {color: '#FFEA82'},
  to: {color: '#ED6A5A'},
  step: (state, bar) => {
    bar.setText(Math.round(bar.value() * 100) + ' %');
  }
  });

  bar.animate(1.0); 
}