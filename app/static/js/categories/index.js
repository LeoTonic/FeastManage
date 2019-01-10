$(document).on('ready', function() {
    $('#modalInputText').on('shown.bs.modal', function() {
        $('#modalInput').focus();
    });

    $('#addCategory').on('click', function() {
        $('#formEditCategoryId').val(0);
        inputTextDialog('Введите текст', '', confirmCategoryItem);
        $('#modalInput').keyup(function(e) {
            if (e.keyCode == 13) confirmCategoryItem();
        });
    });
    function confirmCategoryItem() {
        $('#formEditCategoryTitle').val($('#modalInput').val());
        $('#formEditCategory').submit();
    }
});
