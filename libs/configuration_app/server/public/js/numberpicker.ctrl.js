$(document).ready(function(){
  $('input[type="number"]').niceNumber({

    // auto resize the number input
    autoSize: false,
  
    // the number of extra character
    autoSizeBuffer: 1,
  
    // custom button text
    buttonDecrement: '-',
    buttonIncrement: "+",
  
    // 'around', 'left', or 'right'
    buttonPosition: 'around'
    
  });

});