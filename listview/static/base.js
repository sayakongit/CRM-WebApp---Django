var a;
var filter_box = document.getElementById("content");
var table = document.getElementById("table");
var filter_icon = document.getElementById("filter");

function show_hide() {
  if (a == 1) {
    document.getElementById("content").style.display = "none";
    document.getElementById("table").style.width = "100%";
    document.getElementById("filter").style.background = "#1aae6f";
    document.getElementById("filter").style.color = "#fff";
    return (a = 0);
  } else {
    document.getElementById("content").style.display = "inline";
    document.getElementById("filter").style.background = "#2c9467";
    document.getElementById("filter").style.color = "white";

    return (a = 1);
  }
}

function select() {
  var check = document.getElementById("t_head");
}
