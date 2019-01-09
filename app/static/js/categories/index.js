$(document).on('ready', function() {
    $('#additem').on('click', function() {
        inputTextDialog('Введите текст', '', confirmNewItem);
        function confirmNewItem() {
            $('#formInputId').val(0);
            $('#formInputTitle').val($('#modalInput').val())
            $('#formInputText').submit();
        }
    });
});
