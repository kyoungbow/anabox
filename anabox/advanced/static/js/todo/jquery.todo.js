/**
* Theme: Minton Admin Template
* Author: Coderthemes
* Todo - Application
*/

!function($) {
    "use strict";
    var TodoApp = function() {
        this.$body = $("body"),
        this.$todoContainer = $('#todo-container'),
        this.$todoMessage = $("#todo-message"),
        this.$todoRemaining = $("#todo-remaining"),
        this.$todoTotal = $("#todo-total"),
        this.$archiveBtn = $("#btn-archive"),
        this.$todoList = $("#todo-list"),
        this.$todoDonechk = ".todo-done",
        this.$todoForm = $("#todo-form"),
        this.$todoInput = $("#todo-input-text"),
        this.$todoBtn = $("#todo-btn-submit"),

        this.$todoData = [
        {
            'id': '1',
            'text': '오늘의 스케줄을 적어보세요.',
            'done': true
        }
        ];

        this.$todoCompletedData = [];
        this.$todoUnCompletedData = [];
    };

    //mark/unmark - you can use ajax to save data on server side
    TodoApp.prototype.markTodo = function(todoId, complete) {
       for (var count = 0; count < this.$todoData.length; count++) {
            if (this.$todoData[count].id == todoId) {
                this.$todoData[count].done = complete;
            }
        }
        sessionStorage.setItem('todoData', JSON.stringify(this.$todoData));
    },
    //adds new todo
    TodoApp.prototype.addTodo = function(todoText) {
         const newItem = {
            'id': this.$todoData.length + 1, // 중복 방지를 위해 +1
            'text': todoText,
            'done': false
        };

        this.$todoData.push(newItem);

        // ✅ sessionStorage에 저장
        sessionStorage.setItem('todoData', JSON.stringify(this.$todoData));

        // regenerate list
        this.generate();
    },
    //Archives the completed todos
    TodoApp.prototype.archives = function() {
    	this.$todoUnCompletedData = [];
        this.$todoCompletedData = [];

        for (var count = 0; count < this.$todoData.length; count++) {
            var todoItem = this.$todoData[count];
            if (todoItem.done) {
                this.$todoCompletedData.push(todoItem);
            } else {
                this.$todoUnCompletedData.push(todoItem);
            }
        }

        this.$todoData = [].concat(this.$todoUnCompletedData);

        // ✅ 저장
        sessionStorage.setItem('todoData', JSON.stringify(this.$todoData));

        this.generate();
    },
    //Generates todos
    TodoApp.prototype.generate = function() {
        //clear list
        this.$todoList.html("");
        var remaining = 0;
        for(var count=0; count<this.$todoData.length;count++) {
            //geretaing html
            var todoItem = this.$todoData[count];
            if(todoItem.done == true)
                this.$todoList.prepend('<li class="list-group-item"><div class="checkbox checkbox-primary"><input class="todo-done" id="' + todoItem.id + '" type="checkbox" checked><label for="' + todoItem.id + '">' + todoItem.text + '</label></div></li>');
            else {
                remaining = remaining + 1;
                this.$todoList.prepend('<li class="list-group-item"><div class="checkbox checkbox-primary"><input class="todo-done" id="' + todoItem.id + '" type="checkbox"><label for="' + todoItem.id + '">' + todoItem.text + '</label></div></li>');
            }
        }

        //set total in ui
        this.$todoTotal.text(this.$todoData.length);
        //set remaining
        this.$todoRemaining.text(remaining);
    },
    //init todo app
    TodoApp.prototype.init = function () {
        var $this = this;

        // ✅ sessionStorage에서 불러오기
        const stored = sessionStorage.getItem('todoData');
        if (stored) {
            this.$todoData = JSON.parse(stored);
        }

        this.generate();

        // 기존 이벤트 바인딩 생략 없이 유지
        this.$archiveBtn.on("click", function(e) {
            e.preventDefault();
            $this.archives();
            return false;
        });

        $(document).on("change", this.$todoDonechk, function() {
            $this.markTodo($(this).attr('id'), this.checked);
            $this.generate();
        });

        this.$todoBtn.on("click", function() {
            if (!$this.$todoInput.val()) {
                if($("#userId").val() == "" || $("#userId").val() == "None"){
                    sweetAlert("스케줄", "로그인 후 이용 해주세요!", "error");
                } else{

                    sweetAlert("스케줄", "해야 할 일을 적어주세요!", "error");
                    $this.$todoInput.focus();
                }
            } else {
                $this.addTodo($this.$todoInput.val());
                $this.$todoInput.val(""); // 입력창 초기화
            }
        });
    },
    //init TodoApp
    $.TodoApp = new TodoApp, $.TodoApp.Constructor = TodoApp
    
}(window.jQuery),

//initializing todo app
function($) {
    "use strict";
    $.TodoApp.init()
}(window.jQuery);