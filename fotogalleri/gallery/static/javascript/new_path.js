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

$(function() {
    $('#new-path-button').click(function() {
        if (!!$('#new-path').val()) {
            const crsfToken = getCookie('csrftoken');
            const [{ name, value } = {}] = $('#new-path-form').serializeArray();

            const postData = { csrfmiddlewaretoken: crsfToken };
            postData[name] = value;

            $.post('/newfolder/', postData)
                .done(function(data) {
                    const { is_valid, path, full_path } = data;

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
                    }
                })
                .fail(function(error) {
                    alert('Creating new path failed.');
                });

            $('#new-path').val('');
        }
    });
});
