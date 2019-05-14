var start = 3;
var limit = 3;

$(document).ready(function () {
    var btnMore = document.getElementById('btn_more');
    var loader = document.getElementById('loader');
    loader.style.visibility = 'hidden';
    //$('.app-footer').hide()


	$(window).scroll(function () {
        if ($(window).scrollTop() == $(document).height() - $(window).height()) {
            loader.style.visibility = 'visible';
            getData();
        }
    });

    function getData() {
        request = $.ajax({
            url: '/processor',
            type: 'POST',
            data: {
                action: 'loadmorepost',
                start: start
            }
        });
        request.done(function (data) {
            if (data.result == 'failed') {
                loader.style.visibility = 'hidden';
                btnMore.style.visibility = 'hidden';
                //$('.app-footer').show()
            }
            else {
                loader.style.visibility = 'hidden';
                $('#blog_container').append(data.result);
                start += limit;
            }
        });

        event.preventDefault();

    }
});


function getData() {
    var btnMore = document.getElementById('btn_more');
    var loader = document.getElementById('loader');
    request = $.ajax({
        url: '/processor',
        type: 'POST',
        data: {
            action: 'loadmorepost',
            start: start
        }
    });
    request.done(function (data) {
        if (data.result == 'failed') {
            loader.style.visibility = 'hidden';
            btnMore.style.visibility = 'hidden';
            //$('.app-footer').show()
        }
        else {
            loader.style.visibility = 'hidden';
            $('#blog_container').append(data.result);
            start += limit;
        }
    });
    event.preventDefault();
}





function showprivacy(){
    $('#privacymenu').slideDown('slow').addClass('show');
}; 

function hideprivacy(){
    $('#privacymenu').slideUp().removeClass('show');
}; 