$(document).ready(function(){
  
  
    $(".card").flip({
      // trigger: 'hover'
    }); 
  
  
  var msnry = createMasonry();

  });
  

function createMasonry() {
  return new Masonry('.grid', {
    // options...
    itemSelector: '.grid-item',
    // gutter: 2,
    isFitWidth: true,
  });
}