$('.alt').hide();
$('.js').show();


$(document).ready(function(){
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
