addEventListener("load", () => {
    var index = 0;
    const slides = document.querySelectorAll(".slides");
    const classHide = "slides-hidden", count = slides.length;

    nextSlide();


    function nextSlide() {
        // If its an image
        if(isImage(slides[(index+1) % count])) {
          slides[(index++) % count].classList.add(classHide);
          slides[index % count].classList.remove(classHide);
          setTimeout(nextSlide, 5000);
          console.log("imagem");
        } // If its a video
        else {
          console.log("video");

          slides[(index++) % count].classList.add(classHide);
          slides[index % count].classList.remove(classHide);
          vid = document.getElementById("my-video");
          vid.play();
          vid.onended = function() {
            setTimeout(nextSlide, 0);
          };

        }
    }

    function isImage(i) {
      return i instanceof HTMLImageElement;
    }
});