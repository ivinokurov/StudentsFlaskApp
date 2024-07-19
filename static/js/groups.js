$(document).ready(function () {

    let searchParams = new URLSearchParams(window.location.search)
    // Отображение модального окна при добавлении существующей группы
    if (searchParams.get('msg') == "exists") {
        // Формируем заголовок окна        
        var modalTitle = $('#errModal .modal-title');
        modalTitle.empty();
        modalTitle.append('<b>' + "Ошибка" + '</b>');
        // Формируем сообщение окна
        var modalBody = $('#errModal .modal-body');
        modalBody.empty();
        modalBody.append('<p>' + "Такая группа уже существует!" + '</p>');
        $("#errModal").modal("show")         
    }    

    // Отображение модального окна при удалении группы
    let param = searchParams.get('msg');
    let prefix = "not_remove_"
    if (param != undefined && param.indexOf(prefix) != -1) {
        // Формируем заголовок окна        
        var modalTitle = $('#removeModal .modal-title');
        modalTitle.empty();
        modalTitle.append('<b>' + "Удаление группы" + '</b>');
        // Формируем сообщение окна
        var modalBody = $('#removeModal .modal-body');
        modalBody.empty();
        modalBody.append('<p>' + "В этой группе есть студенты. Удалить?" + '</p>');
        // Сохраняем id удаляемой группы   
        $('#removeModal #removeBtn').attr('data-id', param.replace(prefix,'')); 
        $("#removeModal").modal("show")         
    }     

    $('#deptFilter').on('change', function() {
        var selectedValue = $(this).find("option:selected").text().trim().toLowerCase();
        if (selectedValue == "Все кафедры".toLowerCase()) {
            $('#infoTable tbody tr').show();
            return;
        }         
        $('#infoTable tbody tr').each(function() {
            var rowValue = $(this).find('td:eq(2)').text().toLowerCase();
            $(this).toggle(rowValue.indexOf(selectedValue) > -1);
        });
    });    

    $('#infoTable tbody tr').click(function () {
        // Получаем значения из выбранной строки таблицы
        var id = $(this).find('td:eq(0)').text();
        var name = $(this).find('td:eq(1)').text();
        var department = $(this).find('td:eq(2)').text();

        // Отображаем значения в полях редактирования
        $('#id').val(id);
        $('#name').val(name);
        $("#departments").val($("#departments option:contains('" + department + "')").val()).change();
    });

    $('#remove').click(function (event) {
        id = $('#id').val();        

        $.ajax({
            type: 'POST',
            url: '/removegroup',
            data: { 'groupId': id },
            success: function (response) {
                // Перезагрузка страницы
                window.location.replace('/groups?msg=' + response.msg);                 
            },
            error: function (xhr, status, error) {
                console.log(error);   
            }
        });
    });

    $("#removeBtn").click(function() {
        // Извлекаем из модального окна id группы для её удаления
        id = parseInt($(this).data('id'));

        $.ajax({
            type: 'POST',
            url: '/do_remove_group',
            data: { 'groupId': id },
            success: function (response) {
                // Перезагрузка страницы
                window.location.replace('/groups');                 
            },
            error: function (xhr, status, error) {
                console.log(error);   
            }
        });        
    });

    $('#alter').click(function (event) {
        id = $('#id').val(),
        group_name = $('#name').val(),
        deptId = $("#departments").val(),

        $.ajax({
            type: 'POST',
            url: '/altergroup',
            data: { 'id': id, 'name': group_name, 'deptId': deptId },
            success: function (response) {                
                // Перезагрузка страницы
                window.location.replace('/groups?msg=' + response.msg); 
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
});