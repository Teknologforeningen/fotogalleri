function imgLinkOnClick(link) {
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
