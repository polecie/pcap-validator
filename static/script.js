document.addEventListener( 'click', function (e) {

  circle1
    .tune({ x: e.pageX, y: e.pageY  })
    .replay();

  circle2
    .tune({ x: e.pageX, y: e.pageY  })
    .replay();

});