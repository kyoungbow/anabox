/**
* Theme: Notika Template
* Author: Kalam
* Chat application 
*/

!function($) {
    "use strict";
    
    var ChatApp = function() {
        this.$body = $("body"),
        this.$chatInput = $('.chat-input'),
        this.$chatList = $('.widgets-chat-scrollbar'),
        this.$chatSendBtn = $('.chat-send .btn')
        
    };
    

    //saves chat entry - You should send ajax call to server in order to save chat enrty
    ChatApp.prototype.save = function() {
        var chatText = this.$chatInput.val();
        var chatTime = moment().format("h:mm");

        if (chatText == "") {
            if($("#userId").val() == "" || $("#userId").val() == "None"){
                sweetAlert("챗봇", "로그인 후 이용 해주세요!", "error");
            } else{
                sweetAlert("챗봇", "챗봇에게 물어보고 싶은 말을 적어주세요!", "error");
                this.$chatInput.focus();
            }
        } else {
            // 사용자의 말 출력
            $('<li class="clearfix odd">' +
                '<div class="chat-avatar">' +
                    '<img src="/static/img/post/me.png" alt="mine">' +
                    '<i>' + chatTime + '</i>' +
                '</div>' +
                '<div class="conversation-text">' +
                    '<div class="ctext-wrap chat-widgets-cn">' +
                        '<p>' + chatText + '</p>' +
                    '</div>' +
                '</div>' +
            '</li>').appendTo('ul.conversation-list');

            // 입력창 초기화
            this.$chatInput.val('');
            this.$chatInput.focus();
            this.$chatList.mCustomScrollbar("scrollTo", "bottom");

            var $this = this;

            var loadingMsg = $(
            '<li class="clearfix loading-msg">' +  
                '<div class="chat-avatar">' +
                '<img src="/static/img/post/contaBot.png" alt="bot">' +
                '<i>' + moment().format("h:mm") + '</i>' +
                '</div>' +
                '<div class="conversation-text">' +
                '<div class="ctext-wrap">' +
                    '<p>답변 준비중..</p>' +
                '</div>' +
                '</div>' +
            '</li>'
            );
            $('ul.conversation-list').append(loadingMsg);
            $this.$chatList.mCustomScrollbar("scrollTo", "bottom");

            $.ajax({
            type: "POST",
            url: "/chat/sql-query",
            contentType: "application/json",
            data: JSON.stringify({ message: chatText }),
            success: function(response) {
                var chatbotReply = response.result.split("[결과]")[0];
                var botTime = moment().format("h:mm");

                // 3. “생성중입니다...” 메시지를 실제 답변으로 **대체**
                loadingMsg.html(
                '<div class="chat-avatar">' +
                    '<img src="/static/img/post/contaBot.png" alt="bot">' +
                    '<i>' + botTime + '</i>' +
                '</div>' +
                '<div class="conversation-text">' +
                    '<div class="ctext-wrap">' +
                    '<p>' + chatbotReply + '</p>' +
                    '</div>' +
                '</div>'
                );

                $this.$chatList.mCustomScrollbar("scrollTo", "bottom");
            },
            error: function(err) {
                sweetAlert("챗봇", "챗봇 응답에 실패했습니다. 관리자에게 문의하세요!\n" + err.responseText, "error");
                
                // 실패 시에도 “생성중입니다...” 메시지 지우기 또는 에러 메시지로 변경 가능
                loadingMsg.remove();
            }
            });
        }
    },
    ChatApp.prototype.loadHistory = function () {
        var $this = this;

        $.get("/chat/history", function(history) {
            history.forEach(function(entry) {
                var cls = entry.role === "user" ? "odd" : "";
                var cwc = entry.role === "user" ? "chat-widgets-cn" : "";
                var avatar = entry.role === "user" ? "/static/img/post/me.png" : "/static/img/post/contaBot.png";
                var time = moment().format("h:mm");

                $('<li class="clearfix ' + cls + '">' +
                    '<div class="chat-avatar">' +
                        '<img src="' + avatar + '" alt="' + entry.role + '">' +
                        '<i>' + time + '</i>' +
                    '</div>' +
                    '<div class="conversation-text">' +
                        '<div class="ctext-wrap ' + cwc + '">' +
                            '<p>' + entry.message + '</p>' +
                        '</div>' +
                    '</div>' +
                '</li>').appendTo('ul.conversation-list');
            });
            $this.$chatList.mCustomScrollbar("update");
            $this.$chatList.mCustomScrollbar("scrollTo", "bottom");
        });
    },
    ChatApp.prototype.init = function () {
        var $this = this;

        this.$chatList.mCustomScrollbar({
            theme: "minimal-dark",
            scrollInertia: 1500,
            autoHideScrollbar: true,
            setHeight: 460
        });
        
        $this.loadHistory();
        //binding keypress event on chat input box - on enter we are adding the chat into chat list - 
        $this.$chatInput.keypress(function (ev) {
            var p = ev.which;
            if (p == 13) {
                $this.save();
                return false;
            }
        });


        //binding send button click
        $this.$chatSendBtn.click(function (ev) {
           $this.save();
           return false;
        });
    },
    //init ChatApp
    $.ChatApp = new ChatApp, $.ChatApp.Constructor = ChatApp
    
}(window.jQuery),

//initializing main application module
function($) {
    "use strict";
    $.ChatApp.init();
}(window.jQuery);