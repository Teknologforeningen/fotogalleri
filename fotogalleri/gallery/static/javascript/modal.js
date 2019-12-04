$(function () {
    $('[data-toggle="modal"]').click(function() {
        const modalId = $(this).attr('data-target');
        $(`#${modalId}`).addClass('is-active');
    });

    $('header.modal-card-head > button.delete').click(function() {
        const parents = $(this).parentsUntil('.modal');
        const lastParent = parents.get(-1);
        const modal = lastParent.parentElement;
        $(modal).removeClass('is-active');
    });
});
