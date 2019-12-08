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

function isChecked(index, object) {
    const checkbox = $(object).children('[type=checkbox]');
    const isChecked = $(checkbox).is(':checked');

    return isChecked;
}

function mapWithType(typeString) {
    const curry = function(object) {
        return [object, typeString];
    }

    return curry;
}

function formatWarning(length, typeString) {
    const warning = length === 1
        ? `${length} ${typeString}`
        : `${length} ${typeString}s`;

    return warning;
}

function deleteObject(objectArray) {
    const [object, objectType] = objectArray;
    const crsfToken = getCookie('csrftoken');
    const objectId = $(object).attr('data-id');
    const postData = {
        objectId,
        objectType,
        csrfmiddlewaretoken: crsfToken
    };

    $.post('/delete/', postData)
        .done(function(data) {
            const { success, object_id, errorMessage } = data;

            if (success) {
                object.remove();
            } else {
                alert(`Something went wrong: ${errorMessage}`);
            }
        })
        .fail(function(error) {
            alert(`Deleting ${objectType} failed`);
        });
}

$(function() {
    $('#delete-button').click(function() {
        const imageSelection = $('a.img-link').filter(isChecked);
        const folderSelection = $('a.folder-link').filter(isChecked);

        const images = $.makeArray(imageSelection).map(mapWithType('image'));
        const folders = $.makeArray(folderSelection).map(mapWithType('folder'));

        const imagesWarning = formatWarning(images.length, 'image');
        const foldersWarning = formatWarning(folders.length, 'folder');

        if (!(imagesWarning || foldersWarning)) {
            alert('Please select images or folders');
        } else if (confirm(`Do you want to delete ${imagesWarning} and ${foldersWarning}?`)) {
            const objects = [...images, ...folders];
            objects.forEach(deleteObject);
        }
    });
});
