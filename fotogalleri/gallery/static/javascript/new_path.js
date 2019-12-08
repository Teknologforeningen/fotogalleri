/**
 * The following code is taken from:
 *  https://docs.djangoproject.com/en/dev/ref/csrf/\#ajax
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function () {
    $('#new-path-button').click(function () {
        if (!!$('#new-path').val()) {
            // TODO: error message is only removed when a valid folder name is posted.
            // It should be removed when the modal is closed
            $('#error-msg').remove();
            const crsfToken = getCookie('csrftoken');
            const [{ name, value } = {}] = $('#new-path-form').serializeArray();
            var pathname = window.location.pathname;

            const postData = {
                csrfmiddlewaretoken: crsfToken,
                name: value,
                pathname: pathname,
            };

            $.post('/newfolder/', postData)
                .done(function (data) {
                    const { is_valid, path, full_path, error_msg } = data;

                    if (is_valid) {
                        $('#all-folders').append(`
                            <a
                              href="/view/${full_path}"
                              class="folder-link"
                            >
                              <i class="fas fa-folder" aria-hidden="true"></i>
                              <div>${path}</div>
                            </a>
                        `);
                    } else {
                        $("#new-path").parent().append(
                            `
                            <p id="error-msg" class="has-text-danger is-size-7">
                                ${error_msg}
                            </p>
                            `
                        );
                    }
                })
                .fail(function (error) {
                    alert('Creating new path failed.');
                });

            $('#new-path').val('');
        }
    });
});
