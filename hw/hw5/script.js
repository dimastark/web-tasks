var need = 'EHLO'
var i = 0;

function onKeyDown(e) {
  var char = String.fromCharCode(e.keyCode || e.charCode);
  if (need[i] === char) {
    i++;
  } else {
    i = 0;
  }
  if (i === need.length) {
    alert('Говорил же не нажимать!');
    alert('Короче, эта страничка должна закрыться, но какая-то фигня и ничего не закрывается');
    close();
  }
}
