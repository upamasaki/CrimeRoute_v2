// ----------------------------------------------------------------------
//  photo.js
//
//                          Jun/19/2017
// ----------------------------------------------------------------------

console.log(">>>>> draw.js");


var mark_type = "route";




document.getElementById( "canvas2" ).onclick = function( event ) {
	var clickX = event.pageX ;
  var clickY = event.pageY ;
  
  var rect_size = 50;

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
  var canvas = document.getElementById ("canvas2");
  var ctx = canvas.getContext('2d');
  ctx.font = 'bold 30px Times Roman';
  ctx.textAlign = 'end'  

  if(mark_type == "start"){
    ctx.strokeStyle = "#e0a008";
    ctx.fillStyle = "#e0a008";
    ctx.fillText('S', x - rect_size/2,y  - rect_size/2);
  }
  if(mark_type == "route"){
    ctx.strokeStyle = "#2651be";
  }
  if(mark_type == "goal"){
    ctx.strokeStyle = "#ad1e40";
    ctx.fillStyle = "#ad1e40";
    ctx.fillText('G', x - rect_size/2,y  - rect_size/2);
  }

  // draw rect
  ctx.strokeRect (x - rect_size/2,y  - rect_size/2, 50, 50);
  // ctx.strokeRect (x ,y , 100, 100);

  console.log("mark_type : " + mark_type);
}

document.getElementById("start_btn").onclick = function() {
  console.log("start_btn");
  mark_type = "start";
  
}

document.getElementById("route_btn").onclick = function() {
  console.log("route_btn");
  mark_type = "route";

}

document.getElementById("goal_btn").onclick = function() {
  console.log("goal_btn");
  mark_type = "goal";
  
}

document.getElementById("show_btn").onclick = function() {
  img_path = "/static/assets/images/wall_sample1.jpg";
  console.log("img_path : " + img_path);
  draw_canvas(img_path);
}

function draw_canvas(img_path){

  var scale = 0.9; // 縦横を50%縮小
  var canvas = document.getElementById ("canvas2");

  var ctx = canvas.getContext('2d');

  var img = new Image();
  img.src = img_path;

  console.log("img : " + img_path);
  console.log("img.width  : " + img.width);
  console.log("img.height : " + img.height);

  var wall_img =  document.getElementById ("wall_img");
  console.log("wall_img.width  : " + wall_img.clientWidth);
  console.log("wall_img.height : " + wall_img.clientHeight);  

  var wall_img2 =  document.getElementById ("wall_img2");
  console.log("wall_img.width2  : " + wall_img2.clientWidth);
  console.log("wall_img.height2 : " + wall_img2.clientHeight);  

  img.onload = function()
    {
    // ctx.drawImage(img, 0, 0)

    var dstWidth = img.width * scale;
    var dstHeight = img.height * scale

    console.log("dstWidth  : " + dstWidth);
    console.log("dstHeight : " + dstHeight);
    console.log("canvas.width : " + canvas.width);
    console.log("canvas.height: " + canvas.height);

    if(wall_img2.clientWidth < dstWidth){
      scale2 = wall_img2.clientWidth / dstWidth;
      dstWidth = dstWidth * scale * scale2;
      dstHeight = img.height * scale * scale2;
    }

    canvas.width = dstWidth;
    canvas.height = dstHeight;
    console.log("scale      : " + scale);
    console.log("dstWidth2  : " + dstWidth);
    console.log("dstHeight2 : " + dstHeight);

    ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, dstWidth, dstHeight);

    ctx.lineWidth = 5;
    ctx.strokeStyle = "#2955c8";

    var src = ctx.getImageData(0, 0, canvas.width, canvas.height);
    var dst = ctx.createImageData(canvas.width, canvas.height);
    for (var i = 0; i < src.data.length; i=i+1) {
      // グレースケール
      // var pixel = (src.data[i] + src.data[i+1] + src.data[i+2]) / 3;
      // dst.data[i] = dst.data[i+1] = dst.data[i+2] = pixel;
      // dst.data[i+3] = src.data[i+3];

      dst.data[i] = src.data[i] * 0.7;
      
    }

    ctx.putImageData(dst, 0, 0);
    // ctx.strokeRect (858,230,137,137)
    // ctx.strokeRect (316,227,122,122)
    // ctx.strokeRect (548,261,120,120)
    // ctx.strokeRect (73,350,112,112)
    // ctx.strokeRect (1026,358,108,108)

    // ctx.strokeRect (14, 11, 100, 100)

    // ctx.strokeRect (  0, 100, 100, 100)
    // ctx.strokeRect (100, 100, 100, 100)
    // ctx.strokeRect (200, 100, 100, 100)
    // ctx.strokeRect (300, 100, 100, 100)
    // ctx.strokeRect (400, 100, 100, 100)
    // ctx.strokeRect (500, 100, 100, 100)
    
    // ctx.strokeRect (600, 100, 100, 100)
    // ctx.strokeRect (700, 100, 100, 100)
    // ctx.strokeRect (800, 100, 100, 100)
    // ctx.strokeRect (900, 100, 100, 100)
    // ctx.strokeRect (1000, 100, 100, 100)

    // ctx.strokeRect (1100, 100, 100, 100)


    }

}

// ----------------------------------------------------------------------