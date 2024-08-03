$(document).ready(function () {

    let searchParams = new URLSearchParams(window.location.search)
    // Отображение модального окна при добавлении существующей кафедры
    if (searchParams.get('msg') == "exists") {
        // Формируем заголовок окна        
        var modalTitle = $('#errModal .modal-title');
        modalTitle.empty();
        modalTitle.append('<b>' + "Ошибка" + '</b>');
        // Формируем сообщение окна
        var modalBody = $('#errModal .modal-body');
        modalBody.empty();
        modalBody.append('<p>' + "Такая кафедра уже существует!" + '</p>');
        $("#errModal").modal("show")         
    }    

    // Отображение модального окна при удалении кафедры
    let param = searchParams.get('msg');
    let prefix = "not_remove_"
    if (param != undefined && param.indexOf(prefix) != -1) {
        // Формируем заголовок окна        
        var modalTitle = $('#removeModal .modal-title');
        modalTitle.empty();
        modalTitle.append('<b>' + "Удаление кафедры" + '</b>');
        // Формируем сообщение окна
        var modalBody = $('#removeModal .modal-body');
        modalBody.empty();
        modalBody.append('<p>' + "В этой кафедре есть группы. Удалить?" + '</p>');
        // Сохраняем id удаляемой кафедры   
        $('#removeModal #removeBtn').attr('data-id', param.replace(prefix,'')); 
        $("#removeModal").modal("show")         
    }       

    $('#infoTable tbody tr').click(function () {
        // Получаем значения из выбранной строки таблицы
        var id = $(this).find('td:eq(0)').text();
        var name = $(this).find('td:eq(1)').text();

        // Отображаем значения в полях редактирования
        $('#id').val(id);
        $('#name').val(name);
    });

    $('#remove').click(function (event) {
        id = $('#id').val();        

        $.ajax({
            type: 'POST',
            url: '/remove_department',
            data: { 'departmentId': id },
            success: function (response) {
                // Перезагрузка страницы
                window.location.replace('/departments?msg=' + response.msg);                 
            },
            error: function (xhr, status, error) {
                console.log(error);   
            }
        });
    });

    $("#removeBtn").click(function() {
        // Извлекаем из модального окна id кафедры для её удаления
        id = parseInt($(this).data('id'));

        $.ajax({
            type: 'POST',
            url: '/do_remove_department',
            data: { 'departmentId': id },
            success: function (response) {
                // Перезагрузка страницы
                window.location.replace('/departments');                 
            },
            error: function (xhr, status, error) {
                console.log(error);   
            }
        });        
    });

    $('#alter').click(function (event) {
        id = $('#id').val(),
        department_name = $('#name').val(),

        $.ajax({
            type: 'POST',
            url: '/alter_department',
            data: { 'id': id, 'name': department_name },
            success: function (response) {                
                // Перезагрузка страницы
                window.location.replace('/departments?msg=' + response.msg); 
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
});