//START_SONG = 3900
var start_song = 0;
var process_all = true;
var scroll_step = 10;
var search_step = 200;
var wait_time = 100;
var log_changes = true;
var songs;

function fix_encoding(text) {
    var result = '';
    for (var i=0; i < text.length; i++) {
      var code = text.charCodeAt(i);
      if (code >= 0xC0 && code <= 0xFF) {
        result += String.fromCharCode(code + 0x350);
      } else {
        result = result + String.fromCharCode(code);
      }
    }
    if (log_changes && text !== result) {
      console.log(text + ' -> ' + result);
    }
    return result;
}

function has_wrong_chars(text) {
  for (var i = 0; i < text.length; i++) {
    var code = text.charCodeAt(i);
    if (code >= 0xC0 && code <= 0xFF) {
      return true;
    }
  }
  return false;
}

function process_field(id) {
  value = document.getElementById(id).value;
  valueLen = value.length;

  fixed = fix_encoding(value);
  fixed = fixed.replace('"','\\"')
  document.getElementById(id).value = fixed;

  if (valueLen != document.getElementById(id).value.length) {
    throw Exception("Possible fix error - value length changed")
  }
}

function open_menu(song) {
    function sendEvent(elem, name) {
        var event = document.createEvent("MouseEvents");
        event.initMouseEvent(name,true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        elem.dispatchEvent(event);
    }
    var menu = song.find('.fade-out-with-menu')[0];
    sendEvent(menu,'mouseover');
    bt = menu.getElementsByClassName('goog-flat-button')[0];
    sendEvent(bt, 'click');
    editItem = document.getElementById(":w")
    sendEvent(editItem,'mousedown');
    sendEvent(editItem,'mouseup');
}

function process_song(song) {
  open_menu(song);
  process_field("edit-name");
  process_field("edit-song-artist");
  process_field("edit-album-artist");
  process_field("edit-album");
  process_field("edit-composer");
  process_field("edit-genres");
  $('.modal-dialog-buttons').find('button[name="save"]').click();
}

function process_songs(i) {
  var timeout = 5;
  //for (var i = start_song; i < songs.length; i++) {
  var pos = $(songs[i]).position().top;
  var c = $(songs[i]).css('color');
  $(songs[i]).css('color', 'red');
  if (pos) {
    //$('#main').scrollTop(pos);
    songs[i].scrollIntoView();
  } else {
    console.log('Empty offset');
    $('#main').scrollTop($('#main').scrollTop() + 100);
    timeout = 2000;
  }
  var text = $(songs[i]).text();
  if (has_wrong_chars(text)) {
    process_song(songs[i]);
    console.log('.');
    timeout = wait_time;
  }
  if (i+1 == songs.length) {
    $('#main').scrollTop($('#main').scrollTop() + 100);
    songs = $('.songRow');
    timeout = 2000;
    if (i+1 == songs.length) {
      $(songs[i]).css('color', c);
      console.log('finish');
      return;
    }
  } else {
    setTimeout(function() {
      $(songs[i]).css('color', c);
      process_songs(i+1);
    }, timeout);
  }
}

function process() {
  console.log('start');
  if (process_all) {
    $('li[data-type="all"]').click();
  }
  songs = $('.songRow');
  process_songs(start_song);
}

jQuery(function() {
  $('<a><span class="nav-option">FIX ENCODING</span></a>')
    .prependTo($('<li>')
    .prependTo($('.menu-bar')))
    .on("click", function() {
      process();
    });
});
