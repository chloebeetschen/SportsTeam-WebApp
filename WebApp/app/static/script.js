//home

//slideshow functions
var num = 1;
function next_slide(n){
    slideShow(num += n);
}
function dot_slide(n) {
    slideShow(num = n);
}

function slideShow(n) {
    let images = document.getElementsByClassName("slides");
    let dots = document.getElementsByClassName("dot");
    
    if (n > images.length) {num = 1;}
    if (n < 1) {num = images.length;}
    for (var i = 0; i < images.length; i++) {
      	images[i].style.display = "none";
    }
    for (var i = 0; i < dots.length; i++) {
      	dots[i].className = dots[i].className.replace(" active", "");
    }
    
	images[num - 1].style.display = "block";
    dots[num - 1].className += " active";

};
