var dontclosehelp;

function getVkb(name) {
    var path = "{{ url_for('keyboard') }}";
    //path = "";
    grmDialog = window.open(path, name, "width=600, height=300, scrollbars=yes, resizable=yes");
    grmDialog.focus();

    return void(0);
}

//function adjustIFrameSize (iframeWindow) {
    var frameheight = 500;
    var height = document.body.clientHeight;
    var iframeElement;
    if (iframeWindow.document.height) {
        iframeElement = document.getElementById(iframeWindow.name);
        frameheight = iframeWindow.document.height;
    }
    else if (document.all) {
        iframeElement = document.all[iframeWindow.name];
        if (iframeWindow.document.compatMode && iframeWindow.document.compatMode != 'BackCompat')
            frameheight = iframeWindow.document.documentElement.scrollHeight + 5;
        else
            frameheight = iframeWindow.document.body.scrollHeight + 5;
    }
    if (frameheight > height - 150){
        if (document.getElementById("closeinfoframe")) //opera
            document.getElementById("closeinfoframe").style.top = '30px';
        else if (document.getElementById("closeinfo"))
            document.getElementById("closeinfo").style.top = '98px';
        iframeElement.style.top = '30px';
        if (frameheight > height - 50)
            frameheight = height - 50;
    }
    iframeElement.style.height = frameheight + 'px';
    dontclosehelp = 0;
}


function encodeHex(c) {
  var str = "";
  while (c > 0) {
    var d = c % 16;
    if (d < 10)
      str = String.fromCharCode(0x30 + d) + str;
    else
      str = String.fromCharCode(0x41 + d - 10) + str;
    c = (c - d) / 16;
  }
  return "%" + str;
}


function utf8_decode(utftext) {
  var str = "";
  for (var i = 0; i < utftext.length; ++i) {
    var c = utftext.charCodeAt(i);
    if (c < 128) {
      str += encodeURIComponent(String.fromCharCode(c));
    } else if (c >= 0x410 && c <= 0x44F) {
      str += encodeHex(c - 0x410 + 0xC0);
    } else if (c == 0x401) {
      str += encodeHex(0xA8);
    } else if (c == 0x451) {
      str += encodeHex(0xB8);
    } else {
      str += "";
    }
  }
  return str;
}

function get_params(form) {
 url = "";
 for(var i = 0; i < form.elements.length; i++) {
   var elem = form.elements[i];
   var name = elem.name;
   var value = elem.value;
   if (name != "" && value != "") {
     if (elem.type != "checkbox" && elem.type != "radio" || elem.checked) {
       if (url != "") url += "&";
       url += name;
       url += "=";
       url += encodeURIComponent(value); //utf8_decode(value); //value;
     }
   }
 }
 return url;
}

function clearCGI(form) {
 window.open("http://search1.ruscorpora.ru/search.xml?" + get_params(form)); //form.action + "?" + get_params(form)
 return false;
}

function clearCGI2(form) {
 window.open("http://search1.ruscorpora.ru/search.xml?" + get_params(form)); //form.action + "?" + get_params(form)
 return false;
}
