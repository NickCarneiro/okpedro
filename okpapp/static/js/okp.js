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
        Stripe.createToken({
            number: $('#apply-card-number').val(),
            cvc: $('#apply-card-cvc').val(),
            exp_month: $('#apply-card-expiry-month').val(),
            exp_year: $('#apply-card-expiry-year').val()
            }, stripeResponseHandler);

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

var stripeResponseHandler = function(status, response) {
    console.log(status);
    console.log(response);
    if (response.error) {
        var message;
        // Show the errors on the form
        if (status == 400) {
            message = 'Something was wrong with your payment info. Double check it.'
        } else {
            message = response.error.message;
        }
        showError(message);
        $('#apply-form-button').prop('disabled', false);
    } else {
        // token contains id, last4, and card type
        var token = response.id;
        // Insert the token into the form so it gets submitted to the server
        console.log(token);
        submitApplication({
            'emailAddress': $('#apply-email').val(),
            'facebookUrl': $('#apply-facebook-url').val(),
            'specialRequests': $('#apply-requests').val(),
            'stripeToken': token
        })
    }
};

function submitApplication(payload) {
    var csrfToken = getCookie('csrftoken');
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

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
