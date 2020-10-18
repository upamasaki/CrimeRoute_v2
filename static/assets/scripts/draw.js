// ----------------------------------------------------------------------
//  photo.js
//
//                          Jun/19/2017
// ----------------------------------------------------------------------
window.onload = function()
{
    var canvas = document.getElementById ("wall")

    var ctx = canvas.getContext('2d')

    var img = new Image()
    img.src = "/static/assets/images/wall_sample1.jpg"

    img.onload = function()
        {
        ctx.drawImage(img, 0, 0)

        ctx.lineWidth = 5
        ctx.strokeStyle = "rgb(0, 0, 255)"
        ctx.strokeRect (858,230,137,137)
        ctx.strokeRect (316,227,122,122)
        ctx.strokeRect (548,261,120,120)
        ctx.strokeRect (73,350,112,112)
        ctx.strokeRect (1026,358,108,108)

        ctx.strokeRect (14, 11, 100, 100)

        ctx.strokeRect (  0, 100, 100, 100)
        ctx.strokeRect (100, 100, 100, 100)
        ctx.strokeRect (200, 100, 100, 100)
        ctx.strokeRect (300, 100, 100, 100)
        ctx.strokeRect (400, 100, 100, 100)
        ctx.strokeRect (500, 100, 100, 100)
        
        ctx.strokeRect (600, 100, 100, 100)
        ctx.strokeRect (700, 100, 100, 100)
        ctx.strokeRect (800, 100, 100, 100)
        ctx.strokeRect (900, 100, 100, 100)
        ctx.strokeRect (1000, 100, 100, 100)

        ctx.strokeRect (1100, 100, 100, 100)


        }
}

document.getElementById( "wall" ).onclick = function( event ) {
	var clickX = event.pageX ;
	var clickY = event.pageY ;
  console.log(clickX);
  console.log(clickY);

	// 要素の位置を取得
	var clientRect = this.getBoundingClientRect() ;
	var positionX = clientRect.left + window.pageXOffset ;
	var positionY = clientRect.top + window.pageYOffset ;

	// 要素内におけるクリック位置を計算
	var x = clickX - positionX ;
	var y = clickY - positionY ;

  console.log(x);
  console.log(y);

  // get canvas info
  var canvas = document.getElementById ("wall");
  var ctx = canvas.getContext('2d');

  // draw rect
  ctx.strokeRect (x ,y , 100, 100);

  
  
}

// ----------------------------------------------------------------------