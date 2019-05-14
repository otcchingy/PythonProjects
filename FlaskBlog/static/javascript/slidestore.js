function getSlides() {
    searchname = $('#searchname').val();
    console.log(searchname);
    request = $.ajax({
        url: '/processor/apps',
        type: 'POST',
        data: {
            action: 'search',
            app: 'slidestore',
            by: searchname
        }
    });
    request.done(function (data) {
        $('#searchname').val('');
        if (data.result == 'failed'){
            return;
        }
        else{
            $('#slideresult').html(data.result);
        }
    });

    event.preventDefault();

}
