var f = function(id) {
    var e = document.getElementById(id)
    if (e)
    {
        e.style.display = "none";
        alert (e.style.display);
    }
    else alert ("no e")
}

var g = function() {
    f("header");
    f("footer");
}
