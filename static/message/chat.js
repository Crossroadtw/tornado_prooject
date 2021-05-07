window.onload = function () {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function () {
    };
    var send_input = document.querySelector("#send_input")
    var send_button = document.querySelector('#send_button')
    document.onkeydown = function (event) {
        console.log('css')
        var event = event || window.event;
        var key = event.which || event.keyCode || event.charCode;
        if (key == 13) {
            /*Do something. 调用一些方法*/
            newMessage(send_input.value)
            send_input.value = ''
        }

    }
    send_button.addEventListener('click', function () {
        console.log('发送消息', send_input.value)
        newMessage(send_input.value)
        send_input.value = ''

    })

    updater.start();
    var showmessage = document.querySelector('.show_message')
    showmessage.scrollTop = showmessage.scrollHeight

    setTimeout(function () {
        console.log('测试')
        var xreq = new XMLHttpRequest()
        xreq.open('put', '/messages/email')
        xreq.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
        var number_node = document.querySelector('#chat_num')
        xreq.onreadystatechange = function () {
            if (xreq.readyState == 4 && (xreq.status == 200 || xreq.status == 304)) {
                console.log('更新在线人数', xreq.responseText)
                var peoples = JSON.parse(xreq.responseText)
                number_node.innerHTML = peoples['chat_num']
            }
        }
        xreq.send()

    }, 100)

    setInterval(function () {
        console.log('测试')
        var xreq = new XMLHttpRequest()
        xreq.open('put', '/messages/email')
        xreq.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
        var number_node = document.querySelector('#chat_num')
        xreq.onreadystatechange = function () {
            if (xreq.readyState == 4 && (xreq.status == 200 || xreq.status == 304)) {
                console.log('更新在线人数', xreq.responseText)
                var peoples = JSON.parse(xreq.responseText)
                number_node.innerHTML = peoples['chat_num']
            }
        }
        xreq.send()

    }, 10000)

};

function newMessage(text) {

    updater.socket.send(text);

}

var updater = {
    socket: null,

    start: function () {
        var url = "ws://" + location.host + "/messages/chat";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function (event) {
            updater.showMessage(JSON.parse(event.data));
        }
    },

    showMessage: function (message) {
        var showmessage = document.querySelector('.show_message')
        var message_text = message.text
        var message_time = message.time
        console.log('message;', message)
        console.log('text', message_text)
        console.log('time', message_time)

        var temp_message = '<div class="message">' + message_text + '<small>' + message_time + '</small></div>'
        showmessage.innerHTML = showmessage.innerHTML + temp_message
        showmessage.scrollTop = showmessage.scrollHeight

    }
};

var shake = document.querySelector("#shake_me")

shake.addEventListener('click', function () {

    console.log('点击我')
    document.getElementById("shake_me").setAttribute("disabled", true);
    xreq = new XMLHttpRequest()
    var self = this
    self.innerHTML = "别点了,正在上线啦!!!"
    xreq.open('post', '/messages/email')
    xreq.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xreq.onreadystatechange = function () {

        if (xreq.readyState == 4 && (xreq.status == 200 || xreq.status == 304)) {
            console.log('返回的数据', xreq.responseText)
            var status = JSON.parse(xreq.responseText)
            if (status['status'] == 1) {
                self.innerHTML = "抖一抖"
                document.getElementById("shake_me").removeAttribute("disabled");
            } else {
                self.innerHTML = "好像出问题了,稍后提醒吧"
            }
        }
    }
    xreq.send()


})
