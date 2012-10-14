//START_SONG = 3900
var start_song = 0;
var process_all = true;
var scroll_step = 10;
var search_step = 200;
var wait_time = 100;
var log_changes = true;

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
  var songs = $('.songRow');
  //for (var i = start_song; i < songs.length; i++) {
  var text = $(songs[i]).text();
  var offset = $(songs[i]).offset().top;
  if (offset) {
    document.getElementById('main').scrollTop = offset - 200;
  } else {
    console.log('Empty offset');
    timeout = 2000;
  }
  if (has_wrong_chars(text)) {
    process_song(songs[i]);
    console.log('.');
    //time.sleep(self.wait_time/2)
    timeout = wait_time;
  }
  //if ((i-start_song) % scroll_step == 0) {
    //document.getElementById('main').scrollTop+=230;
    ////timeout = wait_time;
  //}
  //if ((i-start_song) % search_step == 0) {
    ////re-search songs every SEARCH_STEP (default 200) steps - new songs can be AJAX-loaded
    //songs = $('.songRow');
  //}
  if (i == songs.length) {
    console.log('finish');
    return;
  } else {
    setTimeout(function() {
      process_songs(i+1);
    }, timeout);
  }
}

function process() {
  console.log('start');
  if (process_all) {
    $('li[data-type="all"]').click();
  }
  //if (start_song > 0) {
    //var dt = 0;
    //while (dt < start_song) {
      //dt = dt + search_step;
      //document.getElementById('main').scrollTop=23*dt;
    //}
    //document.getElementById('main').scrollTop=23*start_song;
  //}
  process_songs(0);
}

jQuery(function() {
  $('<a><span class="nav-option">FIX ENCODING</span></a>')
    .prependTo($('<li>')
    .prependTo($('.menu-bar')))
    .on("click", function() {
      process();
    });
});
