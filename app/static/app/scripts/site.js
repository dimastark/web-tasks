$('.alt').hide();
$('.js').show();


$(document).ready(function () {
    var chLeft = $('#characterLeft');
    if (chLeft) {
        chLeft.text('Осталось: 120');
        $('#message').keydown(function () {
            var max = 120;
            var len = $(this).val().length;
            if (len >= max) {
                $('#characterLeft').text('Всё, хватит');
                $('#btnSubmit').addClass('disabled');
            } else {
                var ch = max - len;
                $('#characterLeft').text('Осталось: ' + ch);
                $('#btnSubmit').removeClass('disabled');
            }
        });
    }
    var typer = $('#typer');
    if (typer) {
        typer.typeIt({
            speed: 50,
            autoStart: false
        })
        .tiType('Добро пожаловать на мой прекрасный')
        .tiPause(1000)
        .tiDelete(10)
        .tiType('скромный сайт.');
    }
});


function getNextLocation(current, dir) {
    if (current.indexOf('image') === 1) {
        var int = Number(current.slice(6)) + dir;
        var element = document.getElementById('image' + int);
        if (element !== null) {
            return '#image' + int;
        } else {
            return dir === 1 ? '#image0' : '#image12';
        }
    }
    return current;
}


function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}


function onLoadBody() {
    var wallpaperCookie = getCookie('wallpaper');
    if (wallpaperCookie) {
        setWallpaper(wallpaperCookie);
    }
}


function onKeyDown(e) {
    switch (e.keyCode) {
        case 27:
            document.getElementById('cross').click();
            break;
        case 37:
            location.hash = getNextLocation(location.hash, -1);
            break;
        case 39:
            location.hash = getNextLocation(location.hash, 1);
            break;
        case 112:
            document.getElementById('help-toggle').click();
            break;
    }
}


function onButtonDown(string) {
    var name = string.slice(7);
    setWallpaper(name);
    document.cookie = "wallpaper=" + name;
}


function setWallpaper(name) {
    if (['wall1', 'wall3', 'wall4'].indexOf(name) == -1) {
        return;
    }
    var style = "url('static/app/gallery/" + name + ".png') ";
    document.body.style.background = style + 'no-repeat fixed center center';
}
