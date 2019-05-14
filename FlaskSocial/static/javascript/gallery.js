function getGallery(media) {
    request = $.ajax({
        url: '/processor',
        type: 'POST',
        data: {
            action: 'loadgallery',
            media: media
        }
    });
    request.done(function (data) {
        if (data.result == 'failed'){
            return;
        }
        else{
            $('.btn').removeClass('btn-primary').addClass('btn-secondary');
            $('#'+media).removeClass('btn-secondary').addClass('btn-primary');
            $('#gallery').html(data.result);
        }
    });

    event.preventDefault();

}
