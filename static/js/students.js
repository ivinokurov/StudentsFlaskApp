
$(document).ready(function () {

    let searchParams = new URLSearchParams(window.location.search)
    // Отображение модального окна при добавлении существующего студента
    if (searchParams.get('msg') == "exists") {
        // Формируем заголовок окна
        var modalTitle = $('#errModal .modal-title');
        modalTitle.empty();
        modalTitle.append('<b>' + "Ошибка" + '</b>');
        // Формируем сообщение окна
        var modalBody = $('#errModal .modal-body');
        modalBody.empty();
        modalBody.append('<p>' + "Такой студент уже существует!" + '</p>');
        $("#errModal").modal("show")         
    }    

    $('#groupFilter').on('change', function() {
        var selectedValue = $(this).find("option:selected").text().trim().toLowerCase();
        if (selectedValue == "Все группы".toLowerCase()) {
            $('#infoTable tbody tr').show();
            return;
        }        
        $('#infoTable tbody tr').each(function() {
            var rowValue = $(this).find('td:eq(4)').text().toLowerCase();
            $(this).toggle(rowValue.indexOf(selectedValue) > -1);
        });
    });   

    $('#infoTable tbody tr').click(function () {
        // Получаем значения из выбранной строки таблицы
        var id = $(this).find('td:eq(0)').text();
        var name = $(this).find('td:eq(1)').text().trim();
        var phone = $(this).find('td:eq(2)').text();
        var card = $(this).find('td:eq(3)').text();
        var group = $(this).find('td:eq(4)').text();

        // Отображаем значения в полях редактирования
        $('#id').val(id);
        $('#name').val(name);
        $('#phone').val(phone);
        $('#card').val(card);
        $("#groups").val($("#groups option:contains('" + group + "')").val()).change();
        if ($(this).hasClass("table-active")) {
            $('#chief').prop('checked', true);
        } else {
            $('#chief').prop('checked', false);
        }
    });

    $('#remove').click(function (event) {
        var studentId = $('#id').val(),
        chief = $("#chief").is(':checked') ? "on" : "off"            

        $.ajax({
            type: 'POST',
            url: '/remove_student',
            data: { 'id': studentId, 'chief': chief },
            success: function (response) {
                // Перезагрузка страницы
                window.location.replace('/students');
            },
            error: function (xhr, status, error) {
                // Обработка ошибки
            }
        });
    });

    $('#alter').click(function (event) {
        id = $('#id').val(),
        student_name = $('#name').val(),
        student_phone = $('#phone').val(),
        student_card = $('#card').val(),
        groupId = $("#groups").val(),
        chief = $("#chief").is(':checked') ? "on" : "off"

        $.ajax({
            type: 'POST',
            url: '/alter_student',
            data: { 'id': id, 'name': student_name, 'phone': student_phone, 'card': student_card, 'groupId': groupId, 'chief': chief },
            success: function (response) {                
                // Перезагрузка страницы
                window.location.replace('/students?msg=' + response.msg);                                                 
            },
            error: function (xhr, status, error) {
                console.log(error);               
            }
        });
    });
});