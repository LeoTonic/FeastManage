$(document).on('ready', function() {
    setRoleDescription($('#role'));
    $('#phone1').mask('(000) 000-00-00', {'translation': {0: {pattern: /[0-9*]/}}});
    $('#phone2').mask('(000) 000-00-00', {'translation': {0: {pattern: /[0-9*]/}}});
    $('#fax').mask('(000) 000-00-00', {'translation': {0: {pattern: /[0-9*]/}}});
    $('#role').on('change', function() { setRoleDescription($(this)); });
    $('.saveuser').on('click', function() {
        var phone1 = $('#phone1');
        phone1.val(phone1.cleanVal());
        var phone2 = $('#phone2');
        phone2.val(phone2.cleanVal());
        var fax = $('#fax');
        fax.val(fax.cleanVal());
        $('.form').submit();
    });

    function setRoleDescription(roleitem) {
        // В СЛУЧАЕ ИЗМЕНЕНИЯ ИДЕНТИФИКАТОРОВ РОЛЕЙ - ОПИСАНИЯ НУЖНО ИЗМЕНИТЬ
        var role_id = roleitem.val();
        switch(role_id) {
            case "3":
                $('#role-description').html("Редактирование всех исполнителей.<br>Редактирование проживания, питания, транспорта, фестивалей.<br>Редактирование пользователей");
                break;
            case "2":
                $('#role-description').html("Редактирование всех исполнителей.<br>Редактирование проживания, питания, транспорта, фестивалей.");
                break;
            default:
                $('#role-description').html("Редактирование созданных пользователем исполнителей.<br>Добавление исполнителей на фестиваль");
                break;
        }
    }
});
