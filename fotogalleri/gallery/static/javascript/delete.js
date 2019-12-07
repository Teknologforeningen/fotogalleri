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
    $('#delete-button').click(function() {
        const images = $('a.img-link');

        if (confirm(`Do you want to delete ${images.length} images?`)) {
            images.each(function(index, image) {
                const checkbox = $(image).children('[type="checkbox"]');
                const isChecked = $(checkbox).is(':checked');

                if (isChecked) {
                    const crsfToken = getCookie('csrftoken');
                    const objectId = $(image).attr('data-id');
                    const objectType = 'image';
                    const postData = {
                        objectId,
                        objectType,
                        csrfmiddlewaretoken: crsfToken
                    };

                    $.post('/delete/', postData)
                        .done(function(data) {
                            const { success, object_id } = data;
                            // TODO: else
                            if (success) {
                                image.remove();
                            }
                        })
                        .fail(function(error) {
                            alert('Deleting image failed');
                        });
                }
            });
        }
    });
});
