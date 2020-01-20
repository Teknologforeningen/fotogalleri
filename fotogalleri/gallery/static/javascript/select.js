function selectLinkOnClick(link) {
    const checkbox = $(link).children('[type="checkbox"]');
    const checkboxIsHidden = checkbox.is(':hidden');

    if (checkboxIsHidden) {
        const linkUrl = $(link).attr('data-url');
        window.location.href = linkUrl;
    } else {
        const checkboxIsChecked = checkbox.is(':checked');
        if (checkboxIsChecked) {
            checkbox.removeAttr('checked');
        } else {
            checkbox.attr('checked', 'checked');
        }
    }
}

function selectCommon(component) {
    const checkbox = $(component).children('[type="checkbox"]');
    checkbox.toggle();
}

function selectFolderLink(component) {
    selectCommon(component);

    const folderIcon = $(component).children('i.fa-folder');
    folderIcon.toggle();
}

$(function() {
    const selectButton = $('#select-objects-button')
    selectButton.click(function() {
        const deleteButton = $('#delete-button');
        deleteButton.toggle();
        selectButton.find("button").toggleClass("styled-button-admin-selected")

        $('[selectable="true"]').each(function(index, selectable) {
            const classNames = selectable.className.split(' ');
            const filteredNames = classNames.filter(function(className) {
                return className !== 'selectable';
            });

            filteredNames.forEach(function(className) {
                switch (className) {
                    case 'img-link':
                        selectCommon(selectable);
                        return;
                    case 'folder-link':
                        selectFolderLink(selectable);
                        return;
                    default:
                        break;
                }
            });
        });
    });
});
