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

    $('#deleteCategory').on('click', function() {
        confirmDialog('Удаление', 'Уверены, что хотите удалить выбранную категорию?', confirmDeleteCategory);
    });


    $('#addItem').on('click', function() {
        $('#formEditItemId').val(0);
        inputTextDialog('Введите текст', '', confirmListItem);
        $('#modalInput').keyup(function(e) {
            if (e.keyCode == 13) confirmListItem();
        });
    });

    function confirmCategoryItem() {
        $('#formEditCategoryTitle').val($('#modalInput').val());
        $('#formEditCategory').submit();
    }

    function confirmListItem() {
        $('#formEditItemTitle').val($('#modalInput').val());
        $('#formEditItem').submit();
    }

    function confirmDeleteCategory() {
        $('#formDeleteCategory').submit();
    }

});
