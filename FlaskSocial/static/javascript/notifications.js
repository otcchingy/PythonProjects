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
            var postSection = document.getElementById(data.section);
            postSection.remove();
		    return;
		  }
		  else {
			if (data.result == 'accepted'){
                var postSection = document.getElementById(data.section);
                postSection.remove();
			}
			if (data.result == 'declined'){
                var postSection = document.getElementById(data.section);
                postSection.remove();
			}
			if(data.result == 'followed'){
				var postSection = document.getElementById(section);
				postSection.innerHTML = '<button class="btn btn-default" onClick="myFriend'+"(action='unfollow', friend='"+data.friend+"', section='"+data.section+"')"+'"'  + ' type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>Unfollow</span></button>';
			}
			if(data.result == 'unfollowed'){
				var postSection = document.getElementById(section);
				postSection.innerHTML = '<button class="btn btn-default" onClick="myFriend'+"(action='follow', friend='"+data.friend+"', section='"+data.section+"')"+'"'  + ' type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>Follow</span></button>';
			}
			if(data.result == 'deleted'){
				var postSection = document.getElementById(data.section);
				postSection.remove();
			}
			else
				return;
		  }
	  });
  
	  event.preventDefault();
  
  };


  function check(action, noteid, section) {
	doit = $.ajax({
		url: '/processor',
		type: 'POST',
		data: {
			action: action,
			note: noteid,
			section : section
		}
	});
	doit.done(function (data) {
		if (data.result == 'failed') {
			var postSection = document.getElementById(data.section);
			postSection.remove();
			return;
		}
		else {
			if (data.result == 'seen'){
				var postSection = document.getElementById(data.section);
				postSection.innerHTML = '<button class="btn btn-default"'+ 'onclick="check('+"action='deletenote', note='"+data.note+"', section='delete"+data.note+"')"+'"' +' type="button" style="color:#eb3b60;background-image:url(&quot;none&quot;);background-color:transparent;"> <i class="glyphicon glyphicon-heart" data-aos="flip-right"></i><span>Delete</span></button>';
			}
			if (data.result == 'deleted'){
				var postSection = document.getElementById(data.section);
				postSection.remove();
			}
			else
				return;
		}
	});

	event.preventDefault();

	};