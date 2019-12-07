function selectImgLink(component) {
    const checkbox = $(component).children('[type="checkbox"]');
    checkbox.toggle();
}

function selectViewCard(component) {}

$(function() {
    $('#select-objects-button').click(function() {
        $('[selectable="true"]').each(function(index, selectable) {
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
