$(document).on('ready', function() {
    $('#login').prop('disabled', true);
    $('input').addClass('form-control');
    $('select').addClass('form-control');

    setRoleDescription($('#role'));
    $('#role').on('change', function() { setRoleDescription($(this)); });
    $('#saveuser').on('click', function() { $('.form').submit(); });

    $('#deleteuser').on('click', function() {
        confirmDialog('Удаление', 'Уверены, что хотите удалить пользователя?', deleteUser);
    });

    $('#resetpassword').on('click', function() {
        confirmDialog('Сброс пароля', 'Уверены, что хотите сбросить пароль пользователя?', resetPassword);
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

    function deleteUser() {
        $('#form_deleteuser').submit();
    }
    function resetPassword() {
        $('#form_resetpassword').submit();
    }
});
