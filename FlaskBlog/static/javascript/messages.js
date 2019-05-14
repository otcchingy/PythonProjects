var alerts = 0;


$(document).ready(function(){

    private_socket.on('online_friends', function(online_friends){
        var len = online_friends.length;
        for(i=0;i<len;i++){
            var friend = document.getElementById(online_friends[i]);
            friend.innerHTML = "--Online";
            }
    });



    public_socket.on('newaugMessage', function(response){
        var msgBox = document.getElementById('augmessages');
        if (msgBox == null){
            if (alerts == 5){
                $('#alert').html('<center>Hangroom is HOT</center>').fadeIn(3000).fadeOut(3000);
                alerts = 0;
            }else{ alerts += 1 };
        }
        else{
            $("#augmessages").append('<div class="message-from-other message"><p><strong>'+response.username+'</strong></p></div><div class="message-spacer message"><p>'+response.message+'</p></div>');
            msgBox.scrollTop = msgBox.scrollHeight;
        }
    });


});


function sendFriend(userid){
    var msg = $('#messagecontent').val();
    var file = $('#media').val();
    console.log(file);
    if (msg != ''){
        var data = { userid: userid, message:msg };
        private_socket.emit('private_message', data);
        $('#messages').append(' <div style="text-align: right;"><div class="message-from-other message"><strong>Me</strong></div><div class="message-spacer message">'+$('#messagecontent').val()+'</div></div><br/>');
        $('#messagecontent').val("");
        var msgBox = document.getElementById('messages');
        msgBox.scrollTop = msgBox.scrollHeight;
    }
    else{
        return;
    }
};

    
function privateMessage(userid){
    var sendButton = document.getElementById('send-button');
    sendButton.innerHTML = '<button onclick="sendFriend'+"(userid='"+userid+"')"+'"'+'class="btn btn-default msg-button-send" id="send_private_message" type="button">SEND </button> <input type="file" value="Add Media" name="media" id="media" multiple="" style="background-image:url(&quot;none&quot;);background-color:#da052b;color:#fff;margin:0px 0px 6px;border:none;box-shadow:none;text-shadow:none;opacity:0.9;text-transform:uppercase;font-weight:bold;font-size:13px;letter-spacing:0.4px;line-height:1;outline:none;">'
    var msgBox = document.getElementById('message-box');
    msgBox.innerHTML = '<li class="list-group-item" onscroll="scrollCheck()" id="messages" style="overflow:auto;height:300px;margin-bottom:55px;background-color:rgba(140, 146, 148, 0.616) "></li>'
    var user = document.getElementById('user');
    user.innerHTML = '<user class="userid" id="'+userid +'"></user>';
    private_socket.emit('current_chat_buddy', userid)
    doThis(action='privatemessage', friend=userid);
};


function joinaugMessage(){
    if (document.getElementById('send_message') == null){
        public_socket.emit('hangroom');
        var sendButton = document.getElementById('send-button');
        sendButton.innerHTML = '<button onclick="sendmessage()" class="btn btn-default msg-button-send" id="send_message" type="button">SEND </button>';
        var msgBox = document.getElementById('message-box');
        msgBox.innerHTML = '<li class="list-group-item" id="augmessages" style="overflow:auto;height:300px;margin-bottom:55px;background-color:rgb(124, 223, 176);"></li>';
        $('#augmessages').html('<p><center>Welcome to the Hang Room</center></p>')
    }
};


function sendmessage(){
    var msg = $('#messagecontent').val();
    var msgBox = document.getElementById('augmessages');

    if (msg == '@clear'){
        msgBox.innerHTML = " ";
        $('#messagecontent').val(" ");
    }
    else if (msg == ''){
       return;
    }
    else if (msg == '@leave'){
        $('#messagecontent').val("");
        public_socket.emit('augMessage', msg);
        $("#augmessages").append('<div style="text-align: right;"><div class="message-spacer message"><p><b>You Left</p></div></b></div><br/><p><center>use @join to re-enter</center></p>');
        var sendButton = document.getElementById('send-button');
        sendButton.innerHTML = '<button class="btn btn-default msg-button-send" onclick="joinaug()" id="offline" type="button">SEND </button>';
        msgBox.scrollTop = msgBox.scrollHeight;
    }
    else{
        public_socket.emit('augMessage', msg)
        $("#augmessages").append('<div style="text-align: right;"><div class="message-from-other message"><p><strong>Me</strong></p></div><div class="message-spacer message"><p>'+msg+'</p></div></div>');
        msgBox.scrollTop = msgBox.scrollHeight;
        $('#messagecontent').val("");
    }	
};


function joinaug(){
    var msg = $('#messagecontent').val();
    if (msg == '@join'){
        joinaugMessage();
        $('#messagecontent').val(" ");
    }
    else{
        $('#augmessages').append('<p><center>use @join to re-enter</center></p>');
        $('#messagecontent').val(" ");
    }
};