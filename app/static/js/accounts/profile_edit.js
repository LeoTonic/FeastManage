$(document).on('ready', function() {
    $('#login').prop('disabled', true);

    setRoleDescription($('#role'));
    $('#role').on('change', function() { setRoleDescription($(this)); });
    $('#saveuser').on('click', function() { $('.form').submit(); });

    $('#deleteuser').on('click', function() {
        if (confirm('Уверены, что хотите удалить пользователя?')) $('#form_deleteuser').submit();
    });

    $('#resetpassword').on('click', function() {
        if (confirm('Уверены, что хотите сбросить пароль пользователя?')) $('#form_resetpassword').submit();
    });

    function setRoleDescription(roleitem) {
        // В СЛУЧАЕ ИЗМЕНЕНИЯ ИДЕНТИФИКАТОРОВ РОЛЕЙ - ОПИСАНИЯ НУЖНО ИЗМЕНИТЬ
        var roles = {
            "3": "Редактирование без ограничений исполнителей, фестивалей, проживания, питания, транспорта, пользователей.",
            "2": "Редактирование без ограничений исполнителей, фестивалей, проживания, питания, транспорта. Редактирование пользователей запрещено.",
            "1": "Редактирование только своих исполнителей, регистрация участников фестиваля",
        };
        $('#role-description').html(roles[roleitem.val()]);
    }
});
