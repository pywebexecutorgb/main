window.onload = function () {

    // logic for login form

    $('.header-menu').on('click', '.dropdown-toggle', function (event) {
    // $('.dropdown-toggle').on('click', function (event) {
        $.ajax({
            url: $('.login-form').attr('action'),
            success: function (data) {
                $('.login-fields').html(data.result);
                $('.login-form').removeClass('was-validated');
            },
        });
        event.preventDefault();
    });

    $('.header-menu').submit('.login-form', function (event) {
    // $('.login-form').submit(function (event) {
        let loginForm = $('.login-form');
        $('.invalid').remove();
        loginForm.removeClass('was-validated');
        $.ajax({
            data: loginForm.serialize(),
            type: loginForm.attr('method'),
            url: loginForm.attr('action'),
            success: function (data) {
                $('.login-fields').html(data.result);
                if ($(data.result).find('.invalid').length === 0) {
                    $('.dropdown').load(" .dropdown>*", "");
                    $('.modals').load(" .modals>*", "");
                } else {
                    loginForm.addClass('was-validated');
                }
            },
        });
        event.preventDefault();
    });

    // logic for logout

    $('.header-menu').on('click', '.dropdown-logout', function (event) {
        $.ajax({
            url: $('.dropdown-logout').attr('href'),
            success: function () {
                $('.dropdown').load(" .dropdown>*", "");
                $('.modals').load(" .modals>*", "");
            },
        });
        event.preventDefault();
    });

    // logic for sign up form

    $('.header-menu').on('click', '.dropdown-signup', function (event) {
    // $('.dropdown-signup').on('click', function (event) {
        let signupForm = $('.signup-form');
        let signupFields = $('.signup-fields');
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

    $('.modals').submit('.signup-form', function (event) {
    // $('.signup-form').submit(function (event) {
        let signupForm = $('.signup-form');
        let signupFields = $('.signup-fields');
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
                    $('.signup-btn').hide();
                    $('.modal-body-text').show();
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

    $('.header-menu').on('click', '.dropdown-forgot', function (event) {
    // $('.dropdown-forgot').on('click', function (event) {
        let forgotForm = $('.forgot-form');
        let forgotFields = $('.forgot-fields');
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

    $('.modals').submit('.forgot-form', function (event) {
    // $('.forgot-form').submit(function (event) {
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
    // $('.dropdown-user-profile').on('click', function (event) {
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
    // $('.update-user-form').submit(function (event) {
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

    // logic for change password form

    $('.header-menu').on('click', '.dropdown-change-password', function (event) {
    // $('.dropdown-change-password').on('click', function (event) {
        $('#changePasswordModalScrollable').modal('show');
        $('.change-password-fields').show();
        $('.modal-body-title').show();
        $('.change-password-btn').show();
        $('.modal-body-text').hide();
        $.ajax({
            url: $('.dropdown-change-password').attr('href'),
            success: function (data) {
                $('.change-password-fields').html(data.result);
                $('.change-password-form').removeClass('was-validated');
            },
        });
        event.preventDefault();
    });

    $('.modals').submit('.change-password-form', function (event) {
    // $('.change-password-form').submit(function (event) {
        let changePasswordForm = $('.change-password-form');
        let changePasswordFields = $('.change-password-fields');
        $('.invalid').remove();
        changePasswordForm.removeClass('was-validated');
        $.ajax({
            data: changePasswordForm.serialize(),
            type: changePasswordForm.attr('method'),
            url: changePasswordForm.attr('action'),
            success: function (data) {
                changePasswordFields.html(data.result);
                if ($(data.result).find('.invalid').length === 0) {
                    $('.modal-body-title').hide();
                    $('.modal-body-text').show();
                    changePasswordFields.hide();
                    $('.change-password-btn').hide();
                } else {
                    changePasswordForm.addClass('was-validated');
                }
            },
        });
        event.preventDefault();
    });

    // logic for display verification message

    let pathArray = window.location.pathname.split('/');

    if (pathArray[2] === 'verify') {
        $('#verificationModalScrollableTitle').modal('show');
    }

};