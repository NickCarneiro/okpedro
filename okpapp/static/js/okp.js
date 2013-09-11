$(function() {
    $('#apply-button').on('click', function() {
        showApplyDialog();
    });
    $('#apply-dialog-background').on('click', function() {
        hideApplyDialog();
    });
    $('#apply-form-button').on('click', function(e) {
        e.preventDefault();
    });

});

function showApplyDialog() {
    var $applyDialog = $('#apply-dialog');
    $applyDialog.show();

    $('#apply-dialog-background').show();
    var leftMargin = ($(window).width() - $applyDialog.width()) / 2;
    $applyDialog.css('margin-left', leftMargin);
}

function hideApplyDialog() {
    $('#apply-dialog').hide();
    $('#apply-dialog-background').hide();
}