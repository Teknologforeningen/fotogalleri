$(function() {
    $('#js-upload-photos').click(function() {
        $('#uploaded-file-path').val(
            $('#uploaded-file-path').val()
            || window.location.pathname.split('/').slice(2).join('/')
        );

        $('#fileupload').click();
    });

    $('#fileupload').fileupload({
        dataType: 'json',
        sequentialUploads: true,
        formData: function() {
            return $('#upload-form').serializeArray();
        },
        url: '/upload/',
        done: function(e, data) {
            if (data.result.is_valid) {
                const { url, name, width, height } = data.result;
                // 300 is the default thumbnail size that we use
                const widthratio = width / height * 300;
                const padding = height / width * 100;

                $('#all-images').append(`
                    <a
                      href="${url}"
                      class="img-link"
                      style="width: ${widthratio}px; flex-grow: ${widthratio}px;"
                    >
                      <i style="padding-bottom: ${padding}%"></i>
                      <img class="thumbnail-small" src="${url}" alt="${name}" />
                    </a>
                `);
            }
        }
    });
});
