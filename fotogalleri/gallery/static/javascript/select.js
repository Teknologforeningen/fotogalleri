function selectImgLink(component) {}

function selectViewCard(component) {}

$(function() {
    $('#select-objects-button').click(function() {
        const selectables = $('.selectable');
        selectables.each(function(index) {
            const selectable = selectables.get(index);
            const classNames = selectable.className.split(' ');
            const filteredNames = classNames.filter(function(className) {
                return className !== 'selectable';
            });

            filteredNames.forEach(function(className) {
                switch (className) {
                    case 'img-link':
                        selectImgLink(selectable);
                        return;
                    case 'view-card':
                        selectViewCard(selectable);
                        return;
                    default:
                        break;
                }
            });
        });
    });
});
