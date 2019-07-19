window.onload = function () {

    // logic for login form

    let loginForm = $('.login-form');
    let loginFields = $('.login-fields');

    $('.dropdown-toggle').on('click', function (event) {
        $.ajax({
            url: loginForm.attr('action'),
            success: function (data) {
                loginFields.html(data.result);
                signupForm.removeClass('was-validated');
            },
        });
        event.preventDefault();
    });

    loginForm.submit(function (event) {
        $('.invalid').remove();
        loginForm.removeClass('was-validated');
        $.ajax({
            data: loginForm.serialize(),
            type: loginForm.attr('method'),
            url: loginForm.attr('action'),
            success: function (data) {
                loginFields.html(data.result);
                loginForm.addClass('was-validated');
                if ($(data.result).find('.invalid').length === 0) {
                    $('.header-menu').load(" .header-menu");
                }
            },
        });
        event.preventDefault();
    });

    // logic for sign up form

    let signupForm = $('.signup-form');
    let signupFields = $('.signup-fields');

    $('.dropdown-signup').on('click', function (event) {
        $('.modal-body-text').hide();
        signupFields.show();
        $('.signup-btn').show();
        $('#signupModalScrollable').modal('show');
        $.ajax({
            url: signupForm.attr('action'),
            success: function (data) {
                signupFields.html(data.result);
                signupForm.removeClass('was-validated');
            },
        });
        event.preventDefault();
    });

    signupForm.submit(function (event) {
        $('.invalid').remove();
        signupForm.removeClass('was-validated');
        $.ajax({
            data: signupForm.serialize(),
            type: signupForm.attr('method'),
            url: signupForm.attr('action'),
            success: function (data) {
                signupFields.html(data.result);
                signupForm.addClass('was-validated');
                if ($(data.result).find('.invalid').length === 0) {
                    signupFields.hide();
                    $('.modal-body-text').show();
                    $('.signup-btn').hide();
                }
            },
        });
        event.preventDefault();
    });

    // logic for reset password form

    let forgotForm = $('.forgot-form');
    let forgotFields = $('.forgot-fields');

    $('.dropdown-forgot').on('click', function (event) {
        $('#forgotModalScrollable').modal('show');
        $('.modal-body-title').show();
        $('.modal-body-text').hide();
        forgotFields.show();
        $('.forgot-btn').show();
        $.ajax({
            url: forgotForm.attr('action'),
            success: function (data) {
                forgotFields.html(data.result);
                forgotFields.show();
                forgotForm.removeClass('was-validated');
            },
        });
        event.preventDefault();
    });

    forgotForm.submit(function (event) {
        $('.invalid').remove();
        forgotForm.removeClass('was-validated');
        $.ajax({
            data: forgotForm.serialize(),
            type: forgotForm.attr('method'),
            url: forgotForm.attr('action'),
            success: function (data) {
                forgotFields.html(data.result);
                forgotForm.addClass('was-validated');
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