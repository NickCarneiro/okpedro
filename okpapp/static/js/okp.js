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
    var topMargin = ($(window).height() - $applyDialog.height()) / 2;
    $applyDialog.css('margin-left', leftMargin);
    $applyDialog.css('margin-top', topMargin);
}

function hideApplyDialog() {
    $('#apply-dialog').hide();
    $('#apply-dialog-background').hide();
}

$(function() {
    $('#apply-form-button').on('click', function(e) {
        var $form = $(this);

        // Disable the submit button to prevent repeated clicks
        $(this).prop('disabled', true);
        var formError = getFormError();
        if (formError) {
            $(this).prop('disabled', false);
            showError(formError);
            return;
        }

        submitApplication(submitApplication({
            'emailAddress': $('#apply-email').val(),
            'facebookUrl': $('#apply-facebook-url').val(),
            'specialRequests': $('#apply-requests').val()
        })
    );

        // Prevent the form from submitting with the default action
        return false;
    });
});

//validates non-cc fields. returns error message if something is wrong, False if it is OK
function getFormError() {
    var email = $('#apply-email').val();
    if (!email || email.indexOf('@') === -1) {
        return 'Enter a valid email address.'
    }
    var facebookUrl = $('#apply-facebook-url').val();
    if (!facebookUrl) {
        return 'Enter a valid facebook url';
    }

    return false;
}

function submitApplication(payload) {
    var csrfToken = window['csrftoken'];
    $.ajax('/apply', {
        'type': 'post',
        'beforeSend': function (request)
        {
            if (csrfToken) {
                request.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        'data': payload,
        'success': applicationSuccess,
        'error': applicationError
    })
}

function applicationSuccess(res) {
    //hide everything and show thank you message.
    hideApplyDialog();
    $('#intro').text('Thanks for applying! Check your email for a confirmation.');
    $('#intro').append('<p class="follow-pedro">Follow Pedro (<a href="https://twitter.com/paxionfrut">@paxionfrut</a>)' +
        ' and I bet he will be really flattered and approve you. </p>');
    $('.hide-on-success').hide();
}

function applicationError(xhr, status, error) {
    console.log(xhr);
    showError('Agh! Something went wrong on our end. Try again later.');
    $('#apply-form-button').prop('disabled', false);

}

//alertClass should be: alert-success, alert-info, alert-error
function showError(message, alertClass) {
    var $paymentErrors = $('#payment-errors');
    $paymentErrors.text(message);
    $paymentErrors.addClass('alert');
    if (alertClass) {
        $('#payment-errors').addClass(alertClass);
    }
}

