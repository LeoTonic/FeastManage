function confirmDialog(title, content, callback) {
    var modalBox = $('#modalOkCancel');
    if (modalBox) {
        modalBox.find('#modalTitle').html(title);
        modalBox.find('#modalContent').html(content);
        modalBox.find('#modalConfirm').on('click', callback);
        modalBox.modal();
    }
}

function inputTextDialog(title, content, callback) {
    var modalBox = $('#modalInputText');
    if (modalBox) {
        modalBox.find('#modalTitle').html(title);
        modalBox.find('#modalInput').val(content);
        modalBox.find('#modalConfirm').on('click', function() {
            if ($('#modalInput').val()) callback();
        });
        modalBox.modal();
    }
}