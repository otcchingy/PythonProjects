$(document).ready(function () {
    var start = 3;
    var limit = 3;
    var loader = document.getElementById('loader');
    loader.style.visibility = 'hidden';


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
                action: 'exploremore',
                start: start
            }
        });
        request.done(function (data) {
            if (data.result == 'failed') {
                loader.style.visibility = 'hidden';
                return;

            }
            else {
                loader.style.visibility = 'hidden';
                $('#list-group').append(data.result);
                start += limit;
            }
        });

        event.preventDefault();

    }
});