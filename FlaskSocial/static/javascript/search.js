function myFriend(action, friend, section) {
    request = $.ajax({
        url: '/processor',
        type: 'POST',
        data: {
            action: action,
            friend: friend,
            section : section
        }
    });
    request.done(function (data) {
        if (data.result == 'failed') {
            return;
        }
        else {
            if (data.result == 'friendrequestsent'){
              var postSection = document.getElementById(section);
              postSection.innerHTML = '<button class="btn btn-default" onClick="myFriend'+"(action='friendrequestsent', friend='"+data.friend+"', section='"+data.section+"')"+'"' + ' type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>Friend Request Sent</span></button>';
            }
            if(data.result == 'declined' || data.result == 'unfriended'){
              var postSection = document.getElementById(section);
              postSection.innerHTML = '<button class="btn btn-default" onClick="myFriend'+"(action='addfriend', friend='"+data.friend+"', section='"+data.section+"')"+'"'  + ' type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>Addfriend</span></button>';
            }
            if(data.result == 'followed'){
              var postSection = document.getElementById(section);
              postSection.innerHTML = '<button class="btn btn-default" onClick="myFriend'+"(action='unfollow', friend='"+data.friend+"', section='"+data.section+"')"+'"'  + ' type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>Unfollow</span></button>';
            }
            if(data.result == 'unfollowed'){
              var postSection = document.getElementById(section);
              postSection.innerHTML = '<button class="btn btn-default" onClick="myFriend'+"(action='follow', friend='"+data.friend+"', section='"+data.section+"')"+'"'  + ' type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>Follow</span></button>';
            }
            else
                return;
        }
    });

    event.preventDefault();

};