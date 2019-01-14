var selectedItems = [];

$(document).on('ready', function() {
    $('#modalInputText').on('shown.bs.modal', function() {
        $('#modalInput').focus();
    });

    $.each(selectedItems, function(index, value) {
        $('#'.concat(value)).addClass('item--selected');
    });

    $('.edititem').on('click', function() {
        var rowItem = $(this);
        var id = rowItem.attr('id');
        var result = toggleItem(id);
        rowItem.toggleClass('item--selected', result);
        if (selectedItems.length > 0 && $('#deleteItems').is(":hidden")) {
            $('#deleteItems').show(250);
        } else if (selectedItems.length == 0 && $('#deleteItems').is(":visible")) {
            $('#deleteItems').hide(250);
        }
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

    $('.usertool').on('click', function(e) {
        e.stopPropagation();
        var jq = $(this);
        var id = jq.attr('id').substr(4);
        var title = jq.attr('title');
        $('#formEditItemId').val(id);
        inputTextDialog('Введите текст', title, confirmListItem);
        $('#modalInput').keyup(function(e) {
            if (e.keyCode == 13) confirmListItem();
        });
    });

    $('.edititem').hover(
        function(){
            var id = $(this).attr('id');
            $('#edit'.concat(id)).show(50);
        },
        function(){
            var id = $(this).attr('id');
            $('#edit'.concat(id)).hide(50);
        }
    );

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

    function toggleItem(id) {
        var itemIndex = selectedItems.indexOf(id);
        if (itemIndex == -1) {
            selectedItems.push(id);
            return true;
        }
        selectedItems.splice(itemIndex, 1);
        return false;
    }
});
