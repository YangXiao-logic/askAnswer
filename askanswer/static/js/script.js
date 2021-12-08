$(document).ready(function () {

    var ENTER_KEY = 13;
    var ESC_KEY = 27;


    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });


    $(document).on('click', '.delete-btn', function () {
        var $question = $(this).parent();
        $.ajax({
            type: 'DELETE',
            url: $(this).data('href'),
            success: function () {
                $question.remove();
            }
        });
    });

    $(document).on('click', '.delete-tag', function () {
        var $tag = $(this).parent().parent().parent().parent();
        $.ajax({
            type: 'DELETE',
            url: $(this).data('href'),
            success: function () {
                $tag.remove();
            }
        });
    });

    $(document).on('click', '.delete-user', function () {
        var $user = $(this).parent().parent().parent().parent();
        $.ajax({
            type: 'DELETE',
            url: $(this).data('href'),
            success: function () {
                $user.remove();
            }
        });
    });

    function remove_edit_name_input() {
        var $edit_input = $('#edit-name-input');
        var $input = $('#item-input');

        $edit_input.parent().prev().show();
        $edit_input.parent().remove();
        $input.focus();
    }

    function edit_tag_name(e) {
        var $edit_input = $('#edit-name-input');
        var value = $edit_input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $edit_input.val('');

        if (!value) {
            return;
        }

        var url = $edit_input.parent().prev().data('href');
        var id = $edit_input.parent().prev().data('id');

        $.ajax({
            type: 'PUT',
            url: url,
            data: JSON.stringify({'name': value}),
            contentType: 'application/json;charset=UTF-8',
            success: function () {
                $('#name' + id).html(value);
                $edit_input.parent().prev().data('name', value);
                remove_edit_name_input();
            }
        })
    }

    // add new item
    $(document).on('keyup', '#edit-name-input', edit_tag_name.bind(this));


    $(document).on('click', '.edit-btn-name', function () {

        var $tag_name = $(this).parent().parent().parent().prev();
        var tagId = $tag_name.data('id');
        var tagNameBody = $('#body' + tagId).text();
        $tag_name.hide();
        $tag_name.after(' \
                <div class="row card-panel hoverable">\
                <input class="validate" id="edit-name-input" type="text" value="' + tagNameBody + '"\
                autocomplete="off" autofocus required> \
                </div> \
            ');

        var $edit_input = $('#edit-name-input');

        // Focus at the end of input text.
        // Multiply by 2 to ensure the cursor always ends up at the end;
        // Opera sometimes sees a carriage return as 2 characters.
        var strLength = $edit_input.val().length * 2;

        $edit_input.focus();
        $edit_input[0].setSelectionRange(strLength, strLength);

        // Remove edit form when ESC was pressed or focus out.
        $(document).on('keydown', function (e) {
            if (e.keyCode === ESC_KEY) {
                remove_edit_name_input();
            }
        });

        $edit_input.on('focusout', function () {
            remove_edit_name_input();
        })
    });


    function remove_edit_content_input() {
        var $edit_input = $('#edit-content-input');
        var $input = $('#item-input');

        $edit_input.parent().prev().show();
        $edit_input.parent().remove();
        $input.focus();
    }

    function edit_tag_content(e) {
        var $edit_input = $('#edit-content-input');
        var value = $edit_input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $edit_input.val('');

        if (!value) {
            return;
        }

        var url = $edit_input.parent().prev().data('href');
        var id = $edit_input.parent().prev().data('id');

        $.ajax({
            type: 'PUT',
            url: url,
            data: JSON.stringify({'content': value}),
            contentType: 'application/json;charset=UTF-8',
            success: function () {
                $('#content' + id).html(value);
                $edit_input.parent().prev().data('content', value);
                remove_edit_content_input();
            }
        })
    }

    // add new item
    $(document).on('keyup', '#edit-content-input', edit_tag_content.bind(this));


    $(document).on('click', '.edit-btn-content', function () {

        var $tag_content = $(this).parent().parent().prev().prev();
        var tagId = $tag_content.data('id');
        var tagContentBody = $('#body' + tagId).text();
        $tag_content.hide();
        $tag_content.after(' \
                <div class="row card-panel hoverable">\
                <input class="validate" id="edit-content-input" type="text" value="' + tagContentBody + '"\
                autocomplete="off" autofocus required> \
                </div> \
            ');

        var $edit_input = $('#edit-content-input');

        // Focus at the end of input text.
        // Multiply by 2 to ensure the cursor always ends up at the end;
        // Opera sometimes sees a carriage return as 2 characters.
        var strLength = $edit_input.val().length * 2;

        $edit_input.focus();
        $edit_input[0].setSelectionRange(strLength, strLength);

        // Remove edit form when ESC was pressed or focus out.
        $(document).on('keydown', function (e) {
            if (e.keyCode === ESC_KEY) {
                remove_edit_content_input();
            }
        });

        $edit_input.on('focusout', function () {
            remove_edit_content_input();
        })
    });

});

