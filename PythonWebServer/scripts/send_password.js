var port_number = 15328;
var ws;
var sendBuffer = null;
$(function () {
    open();
});
    function open() {
        ws = new WebSocket("ws://" + location.hostname + ":"+port_number+"/command");
        ws.onopen = onopen;
        ws.onmessage = onmessage;
        ws.onclose = onclose;
        ws.onerror = onerror;
    }
    function onopen() {
    }
    function onclose() {
        ws = null;
    }
    function send(msg) {
        if (ws == null) {
            sendBuffer = msg;
            open();
        } else {
            ws.send(msg);
        }
    }
    function onerror(msg) {
    }
    function onmessage(msg) {
        var dataStr = msg.data;
        var index = dataStr.indexOf(':');
        if ((index > 0) && (index < 30)) {
            var command = dataStr.substr(0, index);
            var arg = "";
            if (dataStr.length > index + 1) {
                var arg = dataStr.substr(index + 1);
            }
            if (command == "RET_AUTHENTICATION") {
                window.location.href = '/'+arg;
            }
        }
    }

