$(function() {
    $('#new-folder-button').click(function() {
        if (!!$('#new-path').val()) {
            const formData = $('#new-folder-form').serialize();
            $.post('/newfolder/', formData)
                .done(function(data) {
                    const { is_valid, path, full_path } = data;

                    if (is_valid) {
                        $('#all-images').append(`
                            <div class="view-card">
                              <a
                                href="/view/${full_path}"
                                class="folder-link"
                              >
                                <i class="fas fa-folder" aria-hidden="true"></i>
                                <div>${path}</div>
                              </a>
                            </div>
                        `);
                    }
                })
                .fail(function() {
                    alert('Creating new path failed.');
                });
        }
    });
});
