//START_SONG = 3900
var start_song = 0
var process_all = False
var scroll_step = 10
var search_step = 200

function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
}

function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}

function prepare_text(text) {
  //if (platform.system() == 'Windows'):
      //return text.encode('cp1251')
  //else:
  return encode_utf8(text);
}

function fix_encoding(text) {
    var ln = '';
    txt = decode_utf8(text);
    for (var i=0; i < txt.length; i++) {
      var code = txt.charCodeAt(i);
      var chr = txt[i];
      if (code >= OxC0 and code <= 0xFF) {
        ln += String.fromCharCode(code + 0x350);
      }
      ln = ln + String.fromCharCode(code);
        //if (ord(c) >= 0xC0 and ord(c)<=0xFF):
            //c = unichr(ord(c)+0x350)
        //ln = ln + c
    }
    return encode_utf8(ln);
}

function has_wrong_chars(text) {
  try {
    text = prepare_text(text);
    tt = decode_utf8(text);
  } catch (e) {
    return false;
  }
  for (var i = 0; i < tt; i++) {
    var code = txt.charCodeAt(i);
    if (code >= OxC0 and code <= 0xFF) {
      return true;
    }
  }
  return false;
}

function process_field(id) {
  value = prepare_text(document.getElementById(id).value);
  valueLen = value.length;

  fixed = decode_utf8(fix_encoding(value));
  fixed = fixed.replace('"','\\"')
  document.getElementById(id).value = fixed;

  if (valueLen != document.getElementById(id).value.length) {
    throw Exception("Possible fix error - value length changed")
  }
}

function open_menu(idx, song) {
    function sendEvent(elem, name) {
        var event = document.createEvent("MouseEvents");
        event.initMouseEvent(name,true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        elem.dispatchEvent(event);
    }
    var row = document.getElementsByClassName('songRow')["""+str(idx)+"""];
    var menu = row.getElementsByClassName('fade-out-with-menu')[0];
    sendEvent(menu,'mouseover');
    bt = menu.getElementsByClassName('goog-flat-button')[0];
    sendEvent(bt, 'click');
    editItem = document.getElementById(":d")
    sendEvent(editItem,'mousedown');
    sendEvent(editItem,'mouseup');
}

function process_song(idx, song) {
  open_menu(idx, song);
  process_field("edit-name");
  process_field("edit-song-artist");
  process_field("edit-album-artist");
  process_field("edit-album");
  process_field("edit-composer");
  $('.modal-dialog-buttons').find('button').click();
}

function process() {
  var num = 0;

  if (process_all) {
    # browse to all songs
    $("#all").click()
  }

  if (start_song > 0) {
    var dt = 0;
    while (dt < start_song) {
      dt = dt + search_step;
      document.getElementById('main').scrollTop=23*dt;
      sleep(wait_time/2);
    }
    document.getElementById('main').scrollTop=23*start_song;
    sleep(wait_time/2);
  }
  songs = $('.songRow');
  for (var i = start_song; i < songs.length; i++) {
    var text = $(songs[i]).text();
    if (has_wrong_chars(text)) {
      process_song(i, songs[i]);
      //time.sleep(self.wait_time/2)
    }
    if ((i-start_song) % scroll_step == 0) {
      document.getElementById('main').scrollTop+=230;
    }
    if ((i-start_song) % search_step == 0) {
      #re-search songs every SEARCH_STEP (default 200) steps - new songs can be AJAX-loaded
      songs = $('.songRow');
    }
    var num = i;
  }
  sleep(wait_time);
}
