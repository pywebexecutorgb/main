window.onload = function () {
    let loginForm = $('.login-form');
    let loginFields = $('.login-fields');

    $('.dropdown-toggle').on('click', function (event) {
        $.ajax({
            url: loginForm.attr('action'),
            success: function (data) {
                loginFields.html(data.result);
            },
        });
        event.preventDefault();
    });

    loginForm.submit(function (event) {
        $.ajax({
            data: loginForm.serialize(),
            type: loginForm.attr('method'),
            url: loginForm.attr('action'),
            success: function (data) {
                loginFields.html(data.result);
                if ($(data.result).find('.invalid').length === 0) {
                    $('.header-menu').load(" .header-menu");
                }
            },
        });
        event.preventDefault();
    });

    let signupForm = $('.signup-form');
    let signupFields = $('.signup-fields');

    $('.dropdown-signup').on('click', function (event) {
        $('#signupModalScrollable').modal('show');
        $.ajax({
            url: signupForm.attr('action'),
            success: function (data) {
                signupFields.html(data.result);
            },
        });
        event.preventDefault();
    });

    signupForm.submit(function (event) {
        $.ajax({
            data: signupForm.serialize(),
            type: signupForm.attr('method'),
            url: signupForm.attr('action'),
            success: function (data) {
                signupFields.html(data.result);
                if ($(data.result).find('.invalid').length === 0) {
                    signupFields.hide();
                    $('.modal-body-text').show();
                    $('.signup-btn').hide();
                }
            },
        });
        event.preventDefault();
    });

    let forgotForm = $('.forgot-form');
    let forgotFields = $('.forgot-fields');

    $('.dropdown-forgot').on('click', function (event) {
        $('#forgotModalScrollable').modal('show');
        $('.modal-body-text').hide();
        // $('#forgotModalScrollable').show();
        $.ajax({
            url: forgotForm.attr('action'),
            success: function (data) {
                forgotFields.html(data.result);
            },
        });
        event.preventDefault();
    });

    forgotForm.submit(function (event) {
        $.ajax({
            data: forgotForm.serialize(),
            type: forgotForm.attr('method'),
            url: forgotForm.attr('action'),
            success: function (data) {
                forgotFields.html(data.result);
                if ($(data.result).find('.invalid').length === 0) {
                    $('.modal-body-title').hide();
                    $('.modal-body-text').show();
                    forgotFields.hide();
                    $('.forgot-btn').hide();
                }
            },
        });
        event.preventDefault();
    });

};