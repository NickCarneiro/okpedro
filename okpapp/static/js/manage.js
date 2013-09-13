$(function() {
    $('#create-date-button').on('click', pairDate);
    $('#charge-button').on('click', chargeApplication);
});

function pairDate(e) {
    // get the two applications
    var checkedBoxes = $('#application-table :checked');
    if (checkedBoxes.length != 2) {
        showError('Check two and only two applications to pair a date');
        return;
    }
    var applicationOne = $(checkedBoxes[0]).data('application-id');
    var applicationTwo = $(checkedBoxes[1]).data('application-id');
    var payload = {
        'applicationOne': applicationOne,
        'applicationTwo': applicationTwo
    };
    var csrfToken = getCookie('csrftoken');
    $.ajax('/createDate', {
        'data': payload,
        'type': 'post',
        'success': function(res) {
            console.log(res);
            reloadDates();
        },
        'error': function(xhr, status, error) {
            console.log(xhr);
            showError(xhr.responseText);
        },
        'beforeSend': function (request)
        {
            if (csrfToken) {
                request.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
    })
}

function reloadDates() {
    location.reload()
}

function showError(message) {
    alert(message);
}

function chargeApplication(e) {
    $('#charge-button').prop('disabled', true);
    var checkedApplications = $('#application-table :checked');
    if (checkedApplications.length != 1) {
        alert('Check one application to charge.');
        return;
    }
    var applicationId = $(checkedApplications[0]).data('application-id');
    var payload = {
        'applicationId': applicationId
    };
    var csrfToken = getCookie('csrftoken');
    $.ajax('/charge', {
        'data': payload,
        'type': 'post',
        'beforeSend': function (request) {
            if (csrfToken) {
                request.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        'success': function(res) {
            reloadDates();
        },
        'error': function(xhr, message, status) {
            showError(xhr.responseText);
            $('#charge-button').prop('disabled', false);
        }
    })

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
