window.onload = function () {

    // logic for login form

    let loginForm = $('.login-form');
    let loginFields = $('.login-fields');

    $('.header-menu').on('click', '.dropdown-toggle', function (event) {
        $.ajax({
            url: loginForm.attr('action'),
            success: function (data) {
                loginFields.html(data.result);
                loginForm.removeClass('was-validated');
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
                if ($(data.result).find('.invalid').length === 0) {
                    $('.dropdown').load(" .dropdown>*", "");
                    $('.modals').load(" .modals", "");
                } else {
                    loginForm.addClass('was-validated');
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
                if ($(data.result).find('.invalid').length === 0) {
                    signupFields.hide();
                    $('.modal-body-text').show();
                    $('.signup-btn').hide();
                } else {
                    signupForm.addClass('was-validated');
                }
            },
        });
        event.preventDefault();
    });

    // logic for forgot password form

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
                if ($(data.result).find('.invalid').length === 0) {
                    $('.modal-body-title').hide();
                    $('.modal-body-text').show();
                    forgotFields.hide();
                    $('.forgot-btn').hide();
                } else {
                    forgotForm.addClass('was-validated');
                }
            },
        });
        event.preventDefault();
    });

    // logic for update user form

    $('.header-menu').on('click', '.dropdown-user-profile', function (event) {
        $('#updateUserModalScrollable').modal('show');
        $.ajax({
            url: $('.dropdown-user-profile').attr('href'),
            success: function (data) {
                $('.update-user-fields').html(data.result);
                $('.update-user-form').removeClass('was-validated');
            },
        });
        event.preventDefault();
    });

    $('.modals').submit('.update-user-form', function (event) {
        let updateUserForm = $('.update-user-form');
        let updateUserFields = $('.update-user-fields');
        $('.invalid').remove();
        updateUserForm.removeClass('was-validated');
        $.ajax({
            data: new FormData(updateUserForm.get(0)),
            type: updateUserForm.attr('method'),
            url: updateUserForm.attr('action'),
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                updateUserFields.html(data.result);
                if ($(data.result).find('.invalid').length === 0) {
                    $('#updateUserModalScrollable').modal('hide');
                    $('.dropdown-user-profile').load(" .dropdown-user-profile>*", "");
                } else {
                    updateUserForm.addClass('was-validated');
                }
            },
        });
        event.preventDefault();
    });

    let pathArray = window.location.pathname.split('/');

    if (pathArray[2] === 'verify') {
        $('#verificationModalScrollableTitle').modal('show');
    }

};