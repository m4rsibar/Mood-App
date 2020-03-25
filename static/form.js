//Code for glidejs
new Glide(".js-carousel", {
  dragThreshold: 0,
  keyboard: false
}).mount();

// Code for range slider
var output = document.getElementById("output");

var inputRange = document.getElementsByClassName("range")[0],
  maxValue = 50,
  speed = 5,
  currValue,
  rafID;

inputRange.oninput = function() {
  value = this.value / 10;
  output.innerHTML = Math.round(value);
};

inputRange.min = 0;
inputRange.max = maxValue;

function animateHandler() {
  // calculate gradient transition
  var transX = currValue - maxValue;
  // update input range
  inputRange.value = currValue;
  //Change slide thumb color on mouse up
  if (currValue < 20) {
    inputRange.classList.remove("ltpurple");
  }
  if (currValue < 40) {
    inputRange.classList.remove("purple");
  }
  if (currValue < 60) {
    inputRange.classList.remove("pink");
  }

  if (currValue > -1) {
    window.requestAnimationFrame(animateHandler);
  }

  // decrement value
  currValue = currValue - speed;
}

// move gradient
inputRange.addEventListener("input", function() {
  //Change slide thumb color on way up
  if (this.value > 20) {
    inputRange.classList.add("ltpurple");
  }
  if (this.value > 40) {
    inputRange.classList.add("purple");
  }
  if (this.value > 60) {
    inputRange.classList.add("pink");
  }

  //Change slide thumb color on way down
  if (this.value < 20) {
    inputRange.classList.remove("ltpurple");
  }
  if (this.value < 40) {
    inputRange.classList.remove("purple");
  }
  if (this.value < 60) {
    inputRange.classList.remove("pink");
  }
});
