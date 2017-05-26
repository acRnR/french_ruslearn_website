var shift=0;
var caps=0;
var uml = 0;
var circ = 0;
var grave = 0;
var acute = 0;

function ping(capa){
element=eval('this.'+form_name);
var text_ch ="";

switch (capa){
	case "UML" : {uml = (uml==1) ? 0 : 1; return;};
	case "CIRC" : {circ = (circ==1) ? 0 : 1; return;};
	case "GRAVE" : {grave = (grave==1) ? 0 : 1; return;};
	case "ACUTE" : {acute = (acute==1) ? 0 : 1; return;};
	case "CLEAR_ALL" : {element.value="";return;};
	case "BACK" : {var text_ch=element.value; element.value = text_ch.substr(0, (text_ch.length-1)); return;};
	case "ENTER" : {collect();return;};
	case "CAPS" : caps= (caps==0) ? 1 : 0;
	case "SHIFT" : {shift= (shift==1) ? 0 : 1; return;};
	default : {
		if (uml == 1) {
			if(shift == 0) {
				switch (capa) {
					case "a" : element.value += String.fromCharCode(228); break;
					case "e" : element.value += String.fromCharCode(235); break;
					case "i" : element.value += String.fromCharCode(239); break;
					case "o" : element.value += String.fromCharCode(246); break;
					case "u" : element.value += String.fromCharCode(252); break;
					case "y" : element.value += String.fromCharCode(255); break;
					default: element.value += capa;
				}
			}
			else {
				switch (capa) {
					case "a" : element.value += String.fromCharCode(196); break;
					case "e" : element.value += String.fromCharCode(203); break;
					case "i" : element.value += String.fromCharCode(207); break;
					case "o" : element.value += String.fromCharCode(214); break;
					case "u" : element.value += String.fromCharCode(220); break;
					default: element.value += capa;
				}
			}
			uml = 0;
		}
		else if (circ == 1) {
			if(shift == 0) {
				switch (capa) {
					case "a" : element.value += String.fromCharCode(226); break;
					case "e" : element.value += String.fromCharCode(234); break;
					case "i" : element.value += String.fromCharCode(238); break;
					case "o" : element.value += String.fromCharCode(244); break;
					case "u" : element.value += String.fromCharCode(251); break;
					default: element.value += capa;
				}
			}
			else {
				switch (capa) {
					case "a" : element.value += String.fromCharCode(194); break;
					case "e" : element.value += String.fromCharCode(202); break;
					case "i" : element.value += String.fromCharCode(206); break;
					case "o" : element.value += String.fromCharCode(212); break;
					case "u" : element.value += String.fromCharCode(219); break;
					default: element.value += capa;
				}
			}
			circ = 0;
		}
		else if (grave == 1) {
			if(shift == 0) {
				switch (capa) {
					case "a" : element.value += String.fromCharCode(224); break;
					case "e" : element.value += String.fromCharCode(232); break;
					case "i" : element.value += String.fromCharCode(236); break;
					case "o" : element.value += String.fromCharCode(242); break;
					case "u" : element.value += String.fromCharCode(249); break;
					default: element.value += capa;
				}
			}
			else {
				switch (capa) {
					case "a" : element.value += String.fromCharCode(192); break;
					case "e" : element.value += String.fromCharCode(200); break;
					case "i" : element.value += String.fromCharCode(204); break;
					case "o" : element.value += String.fromCharCode(210); break;
					case "u" : element.value += String.fromCharCode(217); break;
					default: element.value += capa;
				}
			}
			grave = 0;
		}
		else if (acute == 1) {
			if(shift == 0) {
				switch (capa) {
					case "a" : element.value += String.fromCharCode(225); break;
					case "e" : element.value += String.fromCharCode(233); break;
					case "i" : element.value += String.fromCharCode(237); break;
					case "o" : element.value += String.fromCharCode(243); break;
					case "u" : element.value += String.fromCharCode(250); break;
					default: element.value += capa;
				}
			}
			else {
				switch (capa) {
					case "a" : element.value += String.fromCharCode(193); break;
					case "e" : element.value += String.fromCharCode(201); break;
					case "i" : element.value += String.fromCharCode(205); break;
					case "o" : element.value += String.fromCharCode(211); break;
					case "u" : element.value += String.fromCharCode(218); break;
					default: element.value += capa;
				}
			}
			acute = 0;
		}
		else if (shift == 0) element.value=element.value + capa
		else if (shift == 1) {
			switch (capa) {
				case "`" : text_ch="~"; break;
				case "1" : text_ch="!"; break;
				case "2" : text_ch="@"; break;
				case "3" : text_ch="#"; break;
				case "4" : text_ch="$"; break;
				case "5" : text_ch="%"; break;
				case "6" : text_ch="^"; break;
				case "7" : text_ch="&"; break;
				case "8" : text_ch="*"; break;
				case "9" : text_ch="("; break;
				case "0" : text_ch=")"; break;
				case "-" : text_ch="_"; break;
				case "=" : text_ch="+"; break;
				case ";" : text_ch=":"; break;
				case "й" : text_ch="Й"; break;
				case "ц" : text_ch="Ц"; break;
				case "у" : text_ch="У"; break;
				case "к" : text_ch="К"; break;
				case "е" : text_ch="Е"; break;
				case "н" : text_ch="Н"; break;
				case "г" : text_ch="Г"; break;
				case "ш" : text_ch="Ш"; break;
				case "щ" : text_ch="Щ"; break;
				case "з" : text_ch="З"; break;
				case "х" : text_ch="Х"; break;
				case "ъ" : text_ch="Ъ"; break;
				case "{" : text_ch="}"; break;
				case "ф" : text_ch="Ф"; break;
				case "ы" : text_ch="Ы"; break;
				case "в" : text_ch="В"; break;
				case "а" : text_ch="А"; break;
				case "п" : text_ch="П"; break;
				case "р" : text_ch="Р"; break;
				case "о" : text_ch="О"; break;
				case "л" : text_ch="Л"; break;
				case "д" : text_ch="Д"; break;
				case "ж" : text_ch="Ж"; break;
				case "э" : text_ch="Э"; break;
				case "я" : text_ch="Я"; break;
				case "ч" : text_ch="Ч"; break;
				case "с" : text_ch="С"; break;
				case "м" : text_ch="М"; break;
				case "и" : text_ch="И"; break;
				case "т" : text_ch="Т"; break;
				case "ь" : text_ch="Ь"; break;
				case "б" : text_ch="Б"; break;
				case "ю" : text_ch="Ю"; break;
				case "ё" : text_ch="Ё"; break;
				case "," : text_ch="."; break;
				case "<" : text_ch=">"; break;
				case "'" : text_ch='"'; break;
				case "]" : text_ch="["; break;
				case "/" : text_ch="?"; break;
				case "\\" : text_ch="|"; break;
				case "q" : text_ch="Q"; break;
				case "w" : text_ch="W"; break;
				case "e" : text_ch="E"; break;
				case "r" : text_ch="R"; break;
				case "t" : text_ch="T"; break;
				case "y" : text_ch="Y"; break;
				case "u" : text_ch="U"; break;
				case "i" : text_ch="I"; break;
				case "o" : text_ch="O"; break;
				case "p" : text_ch="P"; break;
				case "a" : text_ch="A"; break;
				case "s" : text_ch="S"; break;
				case "d" : text_ch="D"; break;
				case "f" : text_ch="F"; break;
				case "g" : text_ch="G"; break;
				case "h" : text_ch="H"; break;
				case "j" : text_ch="J"; break;
				case "k" : text_ch="K"; break;
				case "l" : text_ch="L"; break;
				case "z" : text_ch="Z"; break;
				case "x" : text_ch="X"; break;
				case "c" : text_ch="C"; break;
				case "v" : text_ch="V"; break;
				case "b" : text_ch="B"; break;
				case "n" : text_ch="N"; break;
				case "m" : text_ch="M"; break;
				case String.fromCharCode(228): text_ch=String.fromCharCode(196); break;
				case String.fromCharCode(246): text_ch=String.fromCharCode(214); break;
				case String.fromCharCode(252): text_ch=String.fromCharCode(220); break;
				case String.fromCharCode(339): text_ch=String.fromCharCode(338); break;
				case String.fromCharCode(231): text_ch=String.fromCharCode(199); break;
				case String.fromCharCode(241): text_ch=String.fromCharCode(209); break;

				default : text_ch=capa
			}
			element.value=element.value + text_ch
		}
		shift = (caps==1) ? 1 : 0;
	}

};
element.focus();
}

	//case "ENTER" : {element.value=element.value + "\n";return;};