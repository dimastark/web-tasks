$('.alt').hide();
$('.js').show();


$(document).ready(function () {
    var chLeft = $('#characterLeft');
    if (chLeft) {
        chLeft.text('Осталось: 255');
        $('#message').keydown(function () {
            var max = 255;
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
    new List('test-list', {
        valueNames: ['filter-value'],
        plugins: [ ListFuzzySearch() ]
    });
    onLoadForm();
});


function getNextLocation(current, dir) {
    if (current.indexOf('image') === 1 && current.indexOf('wall') === -1) {
        var int = Number(current.slice(6)) + dir;
        var element = document.getElementById('image' + int);
        if (element !== null) {
            return '#image' + int;
        } else {
            return dir === 1 ? '#image0' : '#image13';
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
    if (window.document.addEventListener) {
        window.document.addEventListener("keydown", avoidInvalidKeyStorkes, false);
    } else {
        window.document.attachEvent("onkeydown", avoidInvalidKeyStorkes);
        document.captureEvents(Event.KEYDOWN);
    }
}


function avoidInvalidKeyStorkes(evtArg) {
    var evt = (document.all ? window.event : evtArg);
    var isIE = !!document.all;
    var KEYCODE = (document.all ? window.event.keyCode : evtArg.which);

    if (KEYCODE == "112") {
        if (isIE) {
            document.onhelp = function() {
                return (false);
            };
            window.onhelp = function() {
                return (false);
            };
        }
        evt.returnValue = false;
        evt.keyCode = 0;
        evt.preventDefault();
        evt.stopPropagation();
        location.hash = '#help';
    }

    window.status = "Done";
}


function onKeyDown(e) {
    switch (e.keyCode) {
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
    var now = new Date();
    now.setHours(now.getHours() + 1);
    var name = string.slice(7);
    setWallpaper(name);
    document.cookie = "wallpaper=" + name + ';expires=' + now.toUTCString() + ';path=/';
}

function encodeStr(value) {
    var lt = /</g,
    gt = />/g,
    ap = /'/g,
    ic = /"/g;
    return value
        .toString()
        .replace(lt, "&lt;")
        .replace(gt, "&gt;")
        .replace(ap, "&#39;")
        .replace(ic, "&#34;");
}

function setWallpaper(name) {
    if (['wall1', 'wall3', 'wall4'].indexOf(name) == -1) {
        return;
    }
    var style = "url('/static/app/gallery/" + name + ".png') ";
    document.body.style.background = style + 'no-repeat center center fixed';
}

function setResponse(next) {
    document.getElementById('response').value = next;
    document.getElementById('response_form').scrollIntoView(true);
}

function onLoadForm() {
    var form = $('#response_form');
    if (form.length) {
        form.on('submit', function (event) {
            event.preventDefault();
            create_post();
        });
        setInterval(updateComments, 5000);
    }
}

function appendComment(json) {
    var order = encodeStr(json.order);
    var message = encodeStr(json.message);
    var username = encodeStr(json.username);
    var created = json.created;
    var next = encodeStr(json.next);
    $('#comments').append(
        '<div style="margin-left: calc(4 * (' + order.length + 'px - 5px))"'
        + ' class="bottom-top-tile light-border row comment">'
        + '<div class="col-md-12 comment-message">'
        + '<pre class="comment-pre">' + message + '</pre>'
        + '</div>'
        + '<div class="col-md-12">'
        + '<span class="nickname">' + username + '</span>'
        + '<div class="response-and-timestamp">'
        + '<span class="timestamp">' + created + '</span>'
        + '<button onclick="setResponse(\'' + next + '\')" class="response">ответить</button>'
        + '</div>'
        + '</div>'
        + '</div>'
    );
}

function create_post() {
    $.ajax({
        url: "comments",
        type: "POST",
        cache: false,
        dataType: "json",
        data : { message: $('#message').val(), order: $('#response').val() },

        success : function(json) {
            $('#message').val('');
            appendComment(json);
        },

        error : function(xhr,errmsg,err) {
            $('#results').html(
                "<div class='alert-box alert radius' data-alert>" +
                "Ошибочка)" +
                "<a href='#' class='close'>&times;</a></div>"
            );
        }
    });
}

function updateComments() {
    $.ajax({
        url: "comments/",
        type: "POST",
        cache: false,
        dataType: "json",
        data : { last_update: Date.now() - 5000 },

        success : function(json) {
            json.comments.forEach(appendComment);
        },

        error : function(xhr,errmsg,err) {
            $('#results').html(
                "<div class='alert-box alert radius' data-alert>" +
                "Ошибочка)" +
                "<a href='#' class='close'>&times;</a></div>"
            );
        }
    });
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
