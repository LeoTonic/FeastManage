var selectedUsers = [];

$(document).on('ready', function() {
    $.each(selectedUsers, function(index, value) {
        $('#'.concat(value)).addClass('user--selected');
    });

    $('.edituser').on('click', function() {
        var rowItem = $(this);
        var id = rowItem.attr('id');
        var result = toggleUser(id);
        rowItem.toggleClass('user--selected', result);
        if (selectedUsers.length > 0 && $('#deleteusers').is(":hidden")) {
            $('#deleteusers').show(250);
        } else if (selectedUsers.length == 0 && $('#deleteusers').is(":visible")) {
            $('#deleteusers').hide(250);
        }
    });

    $('.usertool').on('click', function() {
        var id = $(this).attr('id').substr(4);
        location.href = Flask.url_for('accounts.edituser', { "user_id": id });
    });

    $('#deleteusers').on('click', function() {
        if (confirm('Уверены, что хотите удалить выбранных пользователей?')) {
            var suForm = $('#form_deleteusers');
            $.each(selectedUsers, function(index, value) {
                $("<input type='hidden'/>").attr('name', 'users[]').val(value).appendTo(suForm);
            });
            $('#form_deleteusers').submit();
        }
    });

    $('.edituser').hover(
        function(){
            var id = $(this).attr('id');
            $('#edit'.concat(id)).show(250);
        },
        function(){
            var id = $(this).attr('id');
            $('#edit'.concat(id)).hide(250);
        }
    );

    function toggleUser(id) {
        var itemIndex = selectedUsers.indexOf(id);
        if (itemIndex == -1) {
            selectedUsers.push(id);
            return true;
        }
        selectedUsers.splice(itemIndex, 1);
        return false;
    }
});
