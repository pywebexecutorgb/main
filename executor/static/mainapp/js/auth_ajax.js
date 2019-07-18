window.onload = function () {
    let loginForm = $('.login-form');

    $('.dropdown-toggle').on('click', function (event) {
        $.ajax({
            url: loginForm.attr('action'),
            success: function (data) {
                $('.login-fields').html(data.result);
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
                $('.login-fields').html(data.result);
                if ($(data.result).find('.invalid').length === 0) {
                    $('.header-menu').load(" .header-menu");
                }
            },
        });
        event.preventDefault();
    });

    let signupForm = $('.signup-form');
    let formFields = $('.signup-fields');

    $('.dropdown-signup').on('click', function (event) {
        $.ajax({
            url: signupForm.attr('action'),
            success: function (data) {
                formFields.html(data.result);
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
                formFields.html(data.result);
                if ($(data.result).find('.invalid').length === 0) {
                    formFields.html('Please check your email for complete the sign up');
                    $('.signup-btn').hide();
                }
            },
        });
        event.preventDefault();
    });

};