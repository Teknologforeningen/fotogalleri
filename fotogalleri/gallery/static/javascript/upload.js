$(function() {
    $(".js-upload-photos").click(function() {
        $("#fileupload").click();
    });

    $("#fileupload").fileupload({
        dataType: 'json',
        done: function(e, data) {
            if (data.result.is_valid) {
                console.log(data.result.url);
            } else console.log('NOPE');
        }
    });
});
