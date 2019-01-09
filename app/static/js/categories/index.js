$(document).on('ready', function() {
    $('#modalInputText').on('shown.bs.modal', function() {
        var jmi = $('#modalInput');
        jmi.focus();
        jmi.keyup(function(e) {
            if (e.keyCode == 13) confirmItem();
        });
    });

    $('#addItem').on('click', function() {
        $('#formEditTextId').val(0);
        inputTextDialog('Введите текст', '', confirmItem);
    });
    function confirmItem() {
        $('#formEditTextTitle').val($('#modalInput').val());
        $('#formEditText').submit();
    }
});
