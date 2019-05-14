var socket = io.connect('http://' + document.domain + ':' + location.port);
var public_socket = io('http://' + document.domain + ':' + location.port + '/public');
var private_socket = io('http://' + document.domain + ':' + location.port + '/private');
var notify_socket = io('http://' + document.domain + ':' + location.port + '/notification');


function checkAlert(){
  notify_socket.emit('notify');
  private_socket.emit('online_user');
};
setInterval(checkAlert, 1000);


function checkAgo(){
  notify_socket.emit('posts_time')
};
setInterval(checkAgo, 60000);


$('.btn').on('click', function(){
  checkAlert();
});


notify_socket.on('notice', function(response){
  if (response.unseen < 1){
    $('#unseen').hide();
  }
  else{
    $('#unseen').show().text(response.unseen);
  }
  if (response.unread < 1){
    $('#unread').hide();
  }
  else{
  $('#unread').show().text(response.unread);
  }
});


notify_socket.on('time_spent', function(response){
  var len = response.length;
  for(i=0;i<len;i++){
      var friend = document.getElementById((response[i])['section']);
      friend.innerHTML = (response[i])['time'];
      }
});


$(document).ready(function(){
  notify_socket.emit('notify');
  private_socket.emit('online_user');
  $('#clubmenu').slideUp().removeClass('show');
  $('#pagemenu').slideUp().removeClass('show');
  
  socket.on('connect', function(){
    socket.emit('connected');
  });


  socket.on('disconnect', function(){
    socket.emit('disconnected');
  });


  socket.on('friend_online', function(response){
    $('#alert').html('<center>'+response.username+' is online</center>').fadeIn(5000).fadeOut(3000);
    var friend = document.getElementById(response.id);
    if (friend != null){
      friend.innerHTML = "--Online";
      }
  });

});



function showmenu(){
  $('#avatar-dropdown').fadeIn().addClass('show');
};

function closemenu(){
  $('#avatar-dropdown').fadeOut().removeClass('show');
}; 

function showpagemenu(){
  $('#pagemenu').slideDown('slow').addClass('show');
}; 

function showclubmenu(){
  $('#clubmenu').slideDown('slow').addClass('show');
}; 

function hidemenu(){
  $('#clubmenu').slideUp().removeClass('show');
  $('#pagemenu').slideUp().removeClass('show');
}; 



function showCommentsModal(postid) {
  request = $.ajax({
      url: '/processor',
      type: 'POST',
      data: {
          action: 'getcomments',
          post: postid,
      }
  });
  request.done(function (data) {
      if (data.result == 'failed') {
          $('#cbox'+data.postid).removeClass('fade').addClass('show').slideDown();
          return;
      }
      else {
          if(data.result){
              $('#cbox'+data.postid).removeClass('fade').addClass('show').slideDown();
              var commentSection = document.getElementById('cbody'+data.postid);
              commentSection.innerHTML = data.result;
              $('#span'+data.postid).html(data.count + '  Comments')
          }
          else
              return;
      }
  });

  event.preventDefault();

};


function hideModal(postid) {
  if (postid == 'None'){
    $('.modal').slideUp().removeClass('show').addClass('fade');
  }
  else{
    $('#cbox'+postid).slideUp().removeClass('show').addClass('fade');
  }
};


function postComments(postid) {
  var comment = $('#comment'+postid).val()
  request = $.ajax({
      url: '/processor',
      type: 'POST',
      data: {
          action: 'postcomments',
          post: postid,
          comment: comment
      }
  });
  request.done(function (data) {
      var cmtBox = document.getElementById('cbody'+data.postid);
      if (data.result == 'failed') {
          return;
      }
      else {
          var html = '<li class="list-group-item" id="delete'+data.postid+'"><blockquote><p><b>'+data.username+'</b></p><article><b>'+data.result+'</b></article>'
          //html += '<btn id="c_like'+data.postid+'"><button class="btn btn-default" onClick="myFunctions'+"(action='c_like', postid='"+data.postid+"', section='c_like"+data.postid+"')"
          //html += 'type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"><i class="glyphicon glyphicon-heart" data-aos="flip-right"></i>'
          //html += '<span>0 Likes</span></button></btn><br/></blockquote></li>'
          $('#cbody'+data.postid).append(html);
          cmtBox.scrollTop = cmtBox.scrollHeight;
          $('#comment'+data.postid).val(" ")
          //console.log($('#span'+data.postid).text())
      }
  });

  event.preventDefault();

};


function myFunctions(action, postid, section) {
    request = $.ajax({
        url: '/processor',
        type: 'POST',
        data: {
            action: action,
            post: postid,
            section : section
        }
    });
    request.done(function (data) {
        if (data.result == 'failed') {
            return;
        }
        else {
            if (data.result == 'liked'){
              var postSection = document.getElementById(section);
              postSection.innerHTML = '<button class="btn btn-default" onClick="myFunctions'+"(action='unlike', postid='"+data.postid+"', section='"+data.section+"')"+'"' + ' type="button" style="color:#873beb;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>'+data.countlikes+' Likes</span></button>';
            }
            if (data.result == 'c_liked'){
              var postSection = document.getElementById(section);
              postSection.innerHTML = '<button class="btn btn-default" onClick="myFunctions'+"(action='c_unlike', postid='"+data.postid+"', section='"+data.section+"')"+'"' + ' type="button" style="color:#873beb;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>'+data.countlikes+' Likes</span></button>';
            }
            if(data.result == 'unliked'){
              var postSection = document.getElementById(section);
              postSection.innerHTML = '<button class="btn btn-default" onClick="myFunctions'+"(action='like', postid='"+data.postid+"', section='"+data.section+"')"+'"'  + ' type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>'+data.countlikes+' Likes</span></button>';
            }
            if(data.result == 'c_unliked'){
              var postSection = document.getElementById(section);
              postSection.innerHTML = '<button class="btn btn-default" onClick="myFunctions'+"(action='c_like', postid='"+data.postid+"', section='"+data.section+"')"+'"'  + ' type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>'+data.countlikes+' Likes</span></button>';
            }
            if(data.result == 'deleted'){
              postSection = document.getElementById(data.section);
              postSection.remove();
            }
            else
                return;
        }
    });
  
    event.preventDefault();
  
  };


  function doThis(action, friend){
    var userid = $('.userid').attr('id');
    if (userid == null || userid == undefined){
      userid = friend;
    }
    if (action=='addfriend'){
      request = $.ajax({
        url: '/processor',
        type: 'POST',
        data: {
          action: 'addfriend',
          friend: userid,
          section: 'None'
        }
      });
      request.done(function(data){
        if(data.result == failed){
          return;
        }
        else{
          $('#btn').html('<button class="btn btn-default" type="button" style="width:100%;background-image:url(&quot;none&quot;);background-color:#da052b;color:#fff;padding:16px 32px;margin:0px 0px 6px;border:none;box-shadow:none;text-shadow:none;opacity:0.9;text-transform:uppercase;font-weight:bold;font-size:13px;letter-spacing:0.4px;line-height:1;outline:none;" onclick="doThis('+"action='friendrequestsent', friend='"+userid+"')"+'"'+'>Friend Request Sent</button>')
          $('#alert').html('<center>friend request sent</center>').fadeIn(5000).fadeOut(3000);
        }
      });
    }
    if (action=='unfriend'){
      request = $.ajax({
        url: '/processor',
        type: 'POST',
        data: {
          action: 'unfriend',
          friend: userid,
          section: 'None'
        }
      });
      request.done(function(data){
        if(data.result == failed){
          return;
        }
        else{
          $('#btn').html('<button class="btn btn-default" type="button" style="width:100%;background-image:url(&quot;none&quot;);background-color:#da052b;color:#fff;padding:16px 32px;margin:0px 0px 6px;border:none;box-shadow:none;text-shadow:none;opacity:0.9;text-transform:uppercase;font-weight:bold;font-size:13px;letter-spacing:0.4px;line-height:1;outline:none;" onclick="doThis('+"action='addfriend', friend='"+userid+"')"+'"'+'>Add Friend</button>')
          //$('#alert').html('<center></center>').fadeIn(5000).fadeOut(3000);
        }
      });
    }
    if (action=='privatemessage'){
      $('#pmessage').removeClass('fade').addClass('show').slideDown();
      $('#messages').html('<br/><br/>	<br/><br/><br/><div id="disqus_thread" class="disqus-loading"><center><div><span  id="loader" class="spinner spinner_active spinner_large"><span class="spinner__dot spinner__dot_1"></span><span class="spinner__dot spinner__dot_2"></span><span class="spinner__dot spinner__dot_3"></span></span></div></center></div>')
      private_socket.emit('current_chat_buddy', userid)
      request = $.ajax({
        url: '/processor',
        type: 'POST',
        data: {
            action: 'previous_messages',
            friend: userid,
            start: 0
        }
      });
      request.done(function (data) {
        if (data.result == 'failed') {
            return;
        }
        else {
            $('#messages').html(data.result);
            var msgBox = document.getElementById('messages');
            msgBox.scrollTop = msgBox.scrollHeight;
        }
     });
    }
    if (action=='sendmessage'){
      var msg = $('#messagecontent').val();
      if (msg != ''){
        var data = { userid: userid, message: msg };
        private_socket.emit('private_message', data);
        $('#messages').append(' <div style="text-align: right;"><div class="message-from-other message"><strong>Me</strong></div><div class="message-spacer message">'+$('#messagecontent').val()+'</div></div><br/>');
        $('#messagecontent').val("");
        var msgBox = document.getElementById('messages');
        msgBox.scrollTop = msgBox.scrollHeight;
      }
      else{
        return;
      }
    }
  };



  var start = 20;
  var limit = 20;
  function scrollCheck(){
      msgBox = document.getElementById('messages');
      var friend = $('.userid').attr('id');
      if (msgBox.scrollTop == 0){
          if(document.getElementById('loader') == null){
              $('#messages').prepend('<center><div id="loader" class="loader"></div></center>');
              getMessages(friend);
          }
      }
  };
  
  
  function getMessages(friend){
      var msgBox = document.getElementById('messages');
      request = $.ajax({
          url: '/processor',
          type: 'POST',
          data: {
              action: 'previous_messages',
              friend: friend,
              start: start
          }
      });
      request.done(function (data) {
          if (data.result == 'failed') {
              $('#loader').remove();
          }
          else {
              $('#loader').remove();
              console.log(msgBox)
              var oldHeight = msgBox.scrollHeight;
              $('#messages').prepend(data.result);
              msgBox.scrollTop = msgBox.scrollHeight-oldHeight;
              start += limit;
          }
      });
  
      event.preventDefault();
  };
  

private_socket.on('new_p_message', function(response){
  $('#alert').html('<center>'+response.username+' sent you a message</center>').remove('hide').fadeIn(2000).fadeOut(2000);
  $('#messages').append('<div class="message-from-other message"><strong>'+response.username+'</strong></div><div class="message-spacer message">message : '+response.message+'</div><br/>');
  var msgBox = document.getElementById('messages');
  if (msgBox != null){
    msgBox.scrollTop = msgBox.scrollHeight;
  }
});


private_socket.on('reset_unread', function(response){
  var section = document.getElementById(response)
  section.innerHTML = ''
});


private_socket.on('new_unread', function(response){
  var section = document.getElementById(response.sender)
  section.innerHTML = response.count
});