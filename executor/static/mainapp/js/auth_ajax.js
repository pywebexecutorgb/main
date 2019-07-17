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

};