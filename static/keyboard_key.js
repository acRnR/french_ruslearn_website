_dom=document.all?3:(document.getElementById?1:(document.layers?2:0));
//alert(_dom);
_mode=1;

if(_dom==3){
}

if(_dom==1){
window.onkeyup =  test;
textEl=0;
}

<!-- общие функции -->

ImgBase = "i/";

function change_mode(){
pic=document.getElementById('recoder');
if(_mode) {
_mode=0;
pic.src=ImgBase + "on_recoder.gif"
}
else {
_mode=1;
pic.src=ImgBase + "off_recoder.gif"
}
}


<!-- функции для mozilla -->

function test (e)
{
//alert(e.keyCode);
textEl=eval(form_name);
if(_mode) {click_mz(e);
}
//textEl.focus();
}

function switch_lang(to_lang, style) {
	switch(to_lang) {
	case 'russian':
		keyboard_img.src = ImgBase + 'new_keyb.gif';
		keyboard_img.useMap = "#newkeyboard";
		lang= "russian";
		break;
	case 'russian_abc':
		keyboard_img.src = ImgBase + 'new_keyb_abc.gif';
		keyboard_img.useMap = "#newkeyboard_abc";
		lang= "russian";
		break;
	case 'german':
		keyboard_img.src = ImgBase + 'german_keyb.gif';
		keyboard_img.useMap = "#german_keyboard";
		lang = "german";
		break;
	case 'france':
		keyboard_img.src = ImgBase + 'french_keyb.gif';
		keyboard_img.useMap = "#france_keyboard";
		lang = "france";
		break;
	case 'spanish':
		keyboard_img.src = ImgBase + 'spanish_keyb.gif';
		keyboard_img.useMap = "#spanish_keyboard";
		lang = "spanish";
		break;
	case 'italian':
		keyboard_img.src = ImgBase + 'italian_keyb.gif';
		keyboard_img.useMap = "#italian_keyboard";
		lang = "italian";
		break;
	}
	if(style) {
		parent_td = document.getElementById('menu').childNodes;
		for (i=0; i<parent_td.length; i++) {
			//alert(parent_td[i].tagName);
			if(parent_td[i].tagName == "A") parent_td[i].style.cssText = "text-decoration : underline;"
		}
		style.cssText = "text-decoration : none; color: black";
	}
}

function press_mz(key, rus_small, rus_big, event)
{
if (key)
	{
	//	document.getElementById(key).className = "down";
	//	setTimeout("release('"+key+"')", 100);
	}
	ch = event.shiftKey ? rus_big : rus_small;
	insertText(textEl,ch);
	//textEl.focus();

}

function insertText(element,text)
{
if (element && element.caretPos)
element.caretPos.text=text;
else if (element && element.selectionStart+1 && element.selectionEnd+1) {
var caretpos=element.selectionStart;
//alert(caretpos);
//alert(element.value.substring(0,element.selectionStart-1));
//alert(text);
//alert(element.value.substring(element.selectionEnd,element.value.length));
element.value=element.value.substring(0,element.selectionStart-1)+text+element.value.substring(element.selectionEnd,element.value.length)

element.selectionStart=caretpos;
element.selectionEnd=caretpos;


//alert('ok');
}
else if (element)
element.value+=text;
}

function click_mz(event)
{


switch (lang) {
		case 'russian': {
			switch (event.keyCode) {
			case 13: collect(); break;
			case 220: press_mz("", "\\", "/", event); break;
			case 223: press_mz("", "ё", "Ё", event); break;
			case 52: press_mz("", "4", ";", event); break;
			case 54: press_mz("", "6", ":", event); break;
			case 55: press_mz("", "7", "?", event); break;
			case 81: press_mz("q", "й", "Й", event); break;
			case 87: press_mz("w", "ц", "Ц", event); break;
			case 69: press_mz("e", "у", "У", event); break;
			case 82: press_mz("r", "к", "К", event); break;
			case 84: press_mz("t", "е", "Е", event); break;
			case 89: press_mz("y", "н", "Н", event); break;
			case 85: press_mz("u", "г", "Г", event); break;
			case 73: press_mz("i", "ш", "Ш", event); break;
			case 79: press_mz("o", "щ", "Щ", event); break;
			case 80: press_mz("p", "з", "З", event); break;
			case 219: press_mz("ob", "х", "Х", event); break;
			case 221: press_mz("cb", "ъ", "Ъ", event); break;
			case 65: press_mz("a", "ф", "Ф", event); break;
			case 83: press_mz("s", "ы", "Ы", event); break;
			case 68: press_mz("d", "в", "В", event); break;
			case 70: press_mz("f", "а", "А", event); break;
			case 71: press_mz("g", "п", "П", event); break;
			case 72: press_mz("h", "р", "Р", event); break;
			case 74: press_mz("j", "о", "О", event); break;
			case 75: press_mz("k", "л", "Л", event); break;
			case 76: press_mz("l", "д", "Д", event); break;
			case 186: press_mz("sc", "ж", "Ж", event); break;
			case 192: press_mz("ap", "э", "Э", event); break;
			case 90: press_mz("z", "я", "Я", event); break;
			case 88: press_mz("x", "ч", "Ч", event); break;
			case 67: press_mz("c", "с", "С", event); break;
			case 86: press_mz("v", "м", "М", event); break;
			case 66: press_mz("b", "и", "И", event); break;
			case 78: press_mz("n", "т", "Т", event); break;
			case 77: press_mz("m", "ь", "Ь", event); break;
			case 188: press_mz("co", "б", "Б", event); break;
			case 190: press_mz("fs", "ю", "Ю", event); break;
			case 191: press_mz("sl", ".", ",", event); break;
			}
			break;
			}
		case 'german':	{
		//alert(event.keyCode)
			switch (event.keyCode) {
			case 13: collect(); break;
			case 220: press_mz("", "\\", "/", event); break;
			case 221: press_mz("", "]", "[", event); break;
			case 89: press_mz("y", "z", "Z", event); break;
			case 219: press_mz("ob", String.fromCharCode(252), String.fromCharCode(220), event); break;
			case 221: press_mz("cb", "ъ", "Ъ", event); break;
			case 59: press_mz("sc", String.fromCharCode(246), String.fromCharCode(214), event); break;
			case 222: press_mz("ap", String.fromCharCode(228), String.fromCharCode(196), event); break;
			case 90: press_mz("z", "y", "Y", event); break;
			case 188: press_mz("co", String.fromCharCode(223), String.fromCharCode(223), event); break;
			case 190: press_mz("fs", String.fromCharCode(956), String.fromCharCode(956), event); break;
			case 223: press_mz("sl", ".", ",", event); break;

	// общие места
			case 52: press_mz("", "4", ";", event); break;
			case 54: press_mz("", "6", ":", event); break;
			case 55: press_mz("", "7", "?", event); break;
			case 81: press_mz("q", "q", "Q", event); break;
			case 87: press_mz("w", "w", "W", event); break;
			case 69: press_mz("e", "e", "E", event); break;
			case 82: press_mz("r", "r", "R", event); break;
			case 84: press_mz("t", "t", "T", event); break;
			case 85: press_mz("u", "u", "U", event); break;
			case 73: press_mz("i", "i", "I", event); break;
			case 79: press_mz("o", "o", "O", event); break;
			case 80: press_mz("p", "p", "P", event); break;
			case 65: press_mz("a", "a", "A", event); break;
			case 83: press_mz("s", "s", "S", event); break;
			case 68: press_mz("d", "d", "D", event); break;
			case 70: press_mz("f", "f", "F", event); break;
			case 71: press_mz("g", "g", "G", event); break;
			case 72: press_mz("h", "h", "H", event); break;
			case 74: press_mz("j", "j", "J", event); break;
			case 75: press_mz("k", "k", "K", event); break;
			case 76: press_mz("l", "l", "L", event); break;
			case 88: press_mz("x", "x", "X", event); break;
			case 67: press_mz("c", "c", "C", event); break;
			case 86: press_mz("v", "v", "V", event); break;
			case 66: press_mz("b", "b", "B", event); break;
			case 78: press_mz("n", "n", "N", event); break;
			case 77: press_mz("m", "m", "M", event); break;
			}
			break;
			}

			case 'france':	{
		//alert(event.keyCode)
			switch (event.keyCode) {
			case 13: collect(); break;
			case 220: press_mz("", "\\", "/", event); break;
			case 89: press_mz("y", "y", "Y", event); break;
			case 219: press_mz("ob", "", "", event); break;
			case 221: press_mz("cb", "", "", event); break;
			case 186: press_mz("sc", "", "", event); break;
			case 222: press_mz("ap", "", "", event); break;
			case 90: press_mz("z", "z", "Z", event); break;
			case 190: press_mz("co", String.fromCharCode(231), String.fromCharCode(199), event); break;
			case 188: press_mz("fs", String.fromCharCode(339), String.fromCharCode(338), event); break;
			case 191: press_mz("sl", ".", ",", event); break;

	// общие места
			case 223: press_mz("", "ё", "Ё", event); break;
			case 52: press_mz("", "4", ";", event); break;
			case 54: press_mz("", "6", ":", event); break;
			case 55: press_mz("", "7", "?", event); break;
			case 81: press_mz("q", "q", "Q", event); break;
			case 87: press_mz("w", "w", "W", event); break;
			case 69: press_mz("e", "e", "E", event); break;
			case 82: press_mz("r", "r", "R", event); break;
			case 84: press_mz("t", "t", "T", event); break;
			case 85: press_mz("u", "u", "U", event); break;
			case 73: press_mz("i", "i", "I", event); break;
			case 79: press_mz("o", "o", "O", event); break;
			case 80: press_mz("p", "p", "P", event); break;
			case 65: press_mz("a", "a", "A", event); break;
			case 83: press_mz("s", "s", "S", event); break;
			case 68: press_mz("d", "d", "D", event); break;
			case 70: press_mz("f", "f", "F", event); break;
			case 71: press_mz("g", "g", "G", event); break;
			case 72: press_mz("h", "h", "H", event); break;
			case 74: press_mz("j", "j", "J", event); break;
			case 75: press_mz("k", "k", "K", event); break;
			case 76: press_mz("l", "l", "L", event); break;
			case 88: press_mz("x", "x", "X", event); break;
			case 67: press_mz("c", "c", "C", event); break;
			case 86: press_mz("v", "v", "V", event); break;
			case 66: press_mz("b", "b", "B", event); break;
			case 78: press_mz("n", "n", "N", event); break;
			case 77: press_mz("m", "m", "M", event); break;
			}
			break;
			}

			case 'spanish':	{
		alert(event.keyCode)
			switch (event.keyCode) {
			case 13: collect(); break;
			case 220: press_mz("", "\\", "/", event); break;
			case 89: press_mz("y", "y", "Y", event); break;
			case 219: press_mz("ob", "", "", event); break;
			case 221: press_mz("cb", "", "", event); break;
			case 186: press_mz("sc", "", "", event); break;
			case 222: press_mz("ap", "", "", event); break;
			case 90: press_mz("z", "z", "Z", event); break;
			case 190: press_mz("co", String.fromCharCode(231), String.fromCharCode(199), event); break;
			case 188: press_mz("fs", String.fromCharCode(339), String.fromCharCode(338), event); break;
			case 191: press_mz("sl", ".", ",", event); break;

	// общие места
			case 223: press_mz("", "ё", "Ё", event); break;
			case 52: press_mz("", "4", ";", event); break;
			case 54: press_mz("", "6", ":", event); break;
			case 55: press_mz("", "7", "?", event); break;
			case 81: press_mz("q", "q", "Q", event); break;
			case 87: press_mz("w", "w", "W", event); break;
			case 69: press_mz("e", "e", "E", event); break;
			case 82: press_mz("r", "r", "R", event); break;
			case 84: press_mz("t", "t", "T", event); break;
			case 85: press_mz("u", "u", "U", event); break;
			case 73: press_mz("i", "i", "I", event); break;
			case 79: press_mz("o", "o", "O", event); break;
			case 80: press_mz("p", "p", "P", event); break;
			case 65: press_mz("a", "a", "A", event); break;
			case 83: press_mz("s", "s", "S", event); break;
			case 68: press_mz("d", "d", "D", event); break;
			case 70: press_mz("f", "f", "F", event); break;
			case 71: press_mz("g", "g", "G", event); break;
			case 72: press_mz("h", "h", "H", event); break;
			case 74: press_mz("j", "j", "J", event); break;
			case 75: press_mz("k", "k", "K", event); break;
			case 76: press_mz("l", "l", "L", event); break;
			case 88: press_mz("x", "x", "X", event); break;
			case 67: press_mz("c", "c", "C", event); break;
			case 86: press_mz("v", "v", "V", event); break;
			case 66: press_mz("b", "b", "B", event); break;
			case 78: press_mz("n", "n", "N", event); break;
			case 77: press_mz("m", "m", "M", event); break;
			}
			break;
			}

		}
}

<!-- функции для IE -->
function press_ie(key, rus_small, rus_big, event)
{
	if(!eval(form_name)) return;
	if (key)
	{
	//	eval("document.all['" +key+ "']").className = "down"
	//	setTimeout("release('"+key+"')", 100);
	}
	ch = event.shiftKey ? rus_big : rus_small;
    if (textEl.createTextRange && textEl.caretPos)
	{
		var caretPos = textEl.caretPos;
        caretPos.text = ch;
    }
    else
	{
    	textEl.value  = ch;
	}
	textEl.focus();
	event.returnValue = false;
}



function click_ie(event)
{

if(!eval(form_name)) return;
textEl=eval(form_name);
	textEl.focus();

	if(!_mode) return;
	if (event.ctrlKey || event.altKey) return;
	if (!textEl.createTextRange()) return;
	textEl.caretPos = document.selection.createRange().duplicate();
	switch (lang) {
		case 'russian': {
			switch (event.keyCode) {
			case 13: collect(); break;
			case 220: press_ie("", "\\", "/", event); break;
			case 223: press_ie("", "ё", "Ё", event); break;
			case 52: press_ie("", "4", ";", event); break;
			case 54: press_ie("", "6", ":", event); break;
			case 55: press_ie("", "7", "?", event); break;
			case 81: press_ie("q", "й", "Й", event); break;
			case 87: press_ie("w", "ц", "Ц", event); break;
			case 69: press_ie("e", "у", "У", event); break;
			case 82: press_ie("r", "к", "К", event); break;
			case 84: press_ie("t", "е", "Е", event); break;
			case 89: press_ie("y", "н", "Н", event); break;
			case 85: press_ie("u", "г", "Г", event); break;
			case 73: press_ie("i", "ш", "Ш", event); break;
			case 79: press_ie("o", "щ", "Щ", event); break;
			case 80: press_ie("p", "з", "З", event); break;
			case 219: press_ie("ob", "х", "Х", event); break;
			case 221: press_ie("cb", "ъ", "Ъ", event); break;
			case 65: press_ie("a", "ф", "Ф", event); break;
			case 83: press_ie("s", "ы", "Ы", event); break;
			case 68: press_ie("d", "в", "В", event); break;
			case 70: press_ie("f", "а", "А", event); break;
			case 71: press_ie("g", "п", "П", event); break;
			case 72: press_ie("h", "р", "Р", event); break;
			case 74: press_ie("j", "о", "О", event); break;
			case 75: press_ie("k", "л", "Л", event); break;
			case 76: press_ie("l", "д", "Д", event); break;
			case 186: press_ie("sc", "ж", "Ж", event); break;
			case 192: press_ie("ap", "э", "Э", event); break;
			case 90: press_ie("z", "я", "Я", event); break;
			case 88: press_ie("x", "ч", "Ч", event); break;
			case 67: press_ie("c", "с", "С", event); break;
			case 86: press_ie("v", "м", "М", event); break;
			case 66: press_ie("b", "и", "И", event); break;
			case 78: press_ie("n", "т", "Т", event); break;
			case 77: press_ie("m", "ь", "Ь", event); break;
			case 188: press_ie("co", "б", "Б", event); break;
			case 190: press_ie("fs", "ю", "Ю", event); break;
			case 191: press_ie("sl", ".", ",", event); break;
			}
			break;
			}
		case 'german':	{
		//alert(event.keyCode)
			switch (event.keyCode) {
			case 13: collect(); break;
			case 220: press_ie("", "\\", "/", event); break;
			case 221: press_ie("", "]", "[", event); break;
			case 89: press_ie("y", "z", "Z", event); break;
			case 219: press_ie("ob", String.fromCharCode(252), String.fromCharCode(220), event); break;
			case 221: press_ie("cb", "ъ", "Ъ", event); break;
			case 186: press_ie("sc", String.fromCharCode(246), String.fromCharCode(214), event); break;
			case 222: press_ie("ap", String.fromCharCode(228), String.fromCharCode(196), event); break;
			case 90: press_ie("z", "y", "Y", event); break;
			case 188: press_ie("co", String.fromCharCode(223), String.fromCharCode(223), event); break;
			case 190: press_ie("fs", String.fromCharCode(956), String.fromCharCode(956), event); break;
			case 191: press_ie("sl", ".", ",", event); break;

	// общие места
			case 223: press_ie("", "ё", "Ё", event); break;
			case 52: press_ie("", "4", ";", event); break;
			case 54: press_ie("", "6", ":", event); break;
			case 55: press_ie("", "7", "?", event); break;
			case 81: press_ie("q", "q", "Q", event); break;
			case 87: press_ie("w", "w", "W", event); break;
			case 69: press_ie("e", "e", "E", event); break;
			case 82: press_ie("r", "r", "R", event); break;
			case 84: press_ie("t", "t", "T", event); break;
			case 85: press_ie("u", "u", "U", event); break;
			case 73: press_ie("i", "i", "I", event); break;
			case 79: press_ie("o", "o", "O", event); break;
			case 80: press_ie("p", "p", "P", event); break;
			case 65: press_ie("a", "a", "A", event); break;
			case 83: press_ie("s", "s", "S", event); break;
			case 68: press_ie("d", "d", "D", event); break;
			case 70: press_ie("f", "f", "F", event); break;
			case 71: press_ie("g", "g", "G", event); break;
			case 72: press_ie("h", "h", "H", event); break;
			case 74: press_ie("j", "j", "J", event); break;
			case 75: press_ie("k", "k", "K", event); break;
			case 76: press_ie("l", "l", "L", event); break;
			case 88: press_ie("x", "x", "X", event); break;
			case 67: press_ie("c", "c", "C", event); break;
			case 86: press_ie("v", "v", "V", event); break;
			case 66: press_ie("b", "b", "B", event); break;
			case 78: press_ie("n", "n", "N", event); break;
			case 77: press_ie("m", "m", "M", event); break;
			}
			break;
			}
			case 'france':	{
		//alert(event.keyCode)
			switch (event.keyCode) {
			case 13: collect(); break;
			case 220: press_ie("", "\\", "/", event); break;
			case 89: press_ie("y", "y", "Y", event); break;
			case 219: press_ie("ob", "", "", event); break;
			case 221: press_ie("cb", "", "", event); break;
			case 186: press_ie("sc", "", "", event); break;
			case 222: press_ie("ap", "", "", event); break;
			case 90: press_ie("z", "z", "Z", event); break;
			case 190: press_ie("co", String.fromCharCode(231), String.fromCharCode(199), event); break;
			case 188: press_ie("fs", String.fromCharCode(339), String.fromCharCode(338), event); break;
			case 191: press_ie("sl", ".", ",", event); break;

	// общие места
			case 223: press_ie("", "ё", "Ё", event); break;
			case 52: press_ie("", "4", ";", event); break;
			case 54: press_ie("", "6", ":", event); break;
			case 55: press_ie("", "7", "?", event); break;
			case 81: press_ie("q", "q", "Q", event); break;
			case 87: press_ie("w", "w", "W", event); break;
			case 69: press_ie("e", "e", "E", event); break;
			case 82: press_ie("r", "r", "R", event); break;
			case 84: press_ie("t", "t", "T", event); break;
			case 85: press_ie("u", "u", "U", event); break;
			case 73: press_ie("i", "i", "I", event); break;
			case 79: press_ie("o", "o", "O", event); break;
			case 80: press_ie("p", "p", "P", event); break;
			case 65: press_ie("a", "a", "A", event); break;
			case 83: press_ie("s", "s", "S", event); break;
			case 68: press_ie("d", "d", "D", event); break;
			case 70: press_ie("f", "f", "F", event); break;
			case 71: press_ie("g", "g", "G", event); break;
			case 72: press_ie("h", "h", "H", event); break;
			case 74: press_ie("j", "j", "J", event); break;
			case 75: press_ie("k", "k", "K", event); break;
			case 76: press_ie("l", "l", "L", event); break;
			case 88: press_ie("x", "x", "X", event); break;
			case 67: press_ie("c", "c", "C", event); break;
			case 86: press_ie("v", "v", "V", event); break;
			case 66: press_ie("b", "b", "B", event); break;
			case 78: press_ie("n", "n", "N", event); break;
			case 77: press_ie("m", "m", "M", event); break;
			}
			break;
			}


case 'spanish':	{
		//alert(event.keyCode)
			switch (event.keyCode) {
			case 13: collect(); break;
			case 220: press_ie("", "\\", "/", event); break;
			case 89: press_ie("y", "y", "Y", event); break;
			case 219: press_ie("ob", "", "", event); break;
			case 221: press_ie("cb", "", "", event); break;
			case 186: press_ie("sc", "", "", event); break;
			case 222: press_ie("ap", "", "", event); break;
			case 90: press_ie("z", "z", "Z", event); break;
			case 190: press_ie("co", String.fromCharCode(231), String.fromCharCode(199), event); break;
			case 188: press_ie("fs", String.fromCharCode(241), String.fromCharCode(209), event); break;
			case 191: press_ie("sl", ".", ",", event); break;

	// общие места
			case 223: press_ie("", "ё", "Ё", event); break;
			case 52: press_ie("", "4", ";", event); break;
			case 54: press_ie("", "6", ":", event); break;
			case 55: press_ie("", "7", "?", event); break;
			case 81: press_ie("q", "q", "Q", event); break;
			case 87: press_ie("w", "w", "W", event); break;
			case 69: press_ie("e", "e", "E", event); break;
			case 82: press_ie("r", "r", "R", event); break;
			case 84: press_ie("t", "t", "T", event); break;
			case 85: press_ie("u", "u", "U", event); break;
			case 73: press_ie("i", "i", "I", event); break;
			case 79: press_ie("o", "o", "O", event); break;
			case 80: press_ie("p", "p", "P", event); break;
			case 65: press_ie("a", "a", "A", event); break;
			case 83: press_ie("s", "s", "S", event); break;
			case 68: press_ie("d", "d", "D", event); break;
			case 70: press_ie("f", "f", "F", event); break;
			case 71: press_ie("g", "g", "G", event); break;
			case 72: press_ie("h", "h", "H", event); break;
			case 74: press_ie("j", "j", "J", event); break;
			case 75: press_ie("k", "k", "K", event); break;
			case 76: press_ie("l", "l", "L", event); break;
			case 88: press_ie("x", "x", "X", event); break;
			case 67: press_ie("c", "c", "C", event); break;
			case 86: press_ie("v", "v", "V", event); break;
			case 66: press_ie("b", "b", "B", event); break;
			case 78: press_ie("n", "n", "N", event); break;
			case 77: press_ie("m", "m", "M", event); break;
			}
			break;
			}

			case 'italian':	{
		//alert(event.keyCode)
			switch (event.keyCode) {
			case 13: collect(); break;
			case 220: press_ie("", "\\", "/", event); break;
			case 89: press_ie("y", "y", "Y", event); break;
			case 219: press_ie("ob", "", "", event); break;
			case 221: press_ie("cb", "", "", event); break;
			case 186: press_ie("sc", "", "", event); break;
			case 222: press_ie("ap", "", "", event); break;
			case 90: press_ie("z", "z", "Z", event); break;
			case 190: press_ie("co", String.fromCharCode(231), String.fromCharCode(199), event); break;
			case 188: press_ie("fs", String.fromCharCode(176), String.fromCharCode(176), event); break;
			case 191: press_ie("sl", ".", ",", event); break;

	// общие места
			case 223: press_ie("", "ё", "Ё", event); break;
			case 52: press_ie("", "4", ";", event); break;
			case 54: press_ie("", "6", ":", event); break;
			case 55: press_ie("", "7", "?", event); break;
			case 81: press_ie("q", "q", "Q", event); break;
			case 87: press_ie("w", "w", "W", event); break;
			case 69: press_ie("e", "e", "E", event); break;
			case 82: press_ie("r", "r", "R", event); break;
			case 84: press_ie("t", "t", "T", event); break;
			case 85: press_ie("u", "u", "U", event); break;
			case 73: press_ie("i", "i", "I", event); break;
			case 79: press_ie("o", "o", "O", event); break;
			case 80: press_ie("p", "p", "P", event); break;
			case 65: press_ie("a", "a", "A", event); break;
			case 83: press_ie("s", "s", "S", event); break;
			case 68: press_ie("d", "d", "D", event); break;
			case 70: press_ie("f", "f", "F", event); break;
			case 71: press_ie("g", "g", "G", event); break;
			case 72: press_ie("h", "h", "H", event); break;
			case 74: press_ie("j", "j", "J", event); break;
			case 75: press_ie("k", "k", "K", event); break;
			case 76: press_ie("l", "l", "L", event); break;
			case 88: press_ie("x", "x", "X", event); break;
			case 67: press_ie("c", "c", "C", event); break;
			case 86: press_ie("v", "v", "V", event); break;
			case 66: press_ie("b", "b", "B", event); break;
			case 78: press_ie("n", "n", "N", event); break;
			case 77: press_ie("m", "m", "M", event); break;
			}
			break;
			}


		}
}