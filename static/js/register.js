
$(document).ready(function () {

    let searchParams = new URLSearchParams(window.location.search)
    // Отображение модального окна при добавлении пользователя с существующим в БД логином
    if (searchParams.get('msg') == "exists") {
        // Формируем заголовок окна
        var modalTitle = $('#errModal .modal-title');
        modalTitle.empty();
        modalTitle.append('<b>' + "Ошибка добавления нового пользователя" + '</b>');
        // Формируем сообщение окна
        var modalBody = $('#errModal .modal-body');
        modalBody.empty();
        modalBody.append('<p>' + "Пользователь с таким логином уже существует!" + '</p>');
        $("#errModal").modal("show")         
    } 

    $('button[name="removeUser"]').click(function(event ){
        var id = $(event.target).attr('id');

        $.ajax({
            type: 'POST',
            url: '/removeuser',
            data: { 'id': id },
            success: function (response) {                
                // Перезагрузка страницы
                    window.location.replace('/register');                                        
            },
            error: function (xhr, status, error) {
                console.log(error);   
            },
        });        
    });    

    $('#register').click(function (event) {
        username = $('#username').val(),
        password = $('#password').val(),
        role = $('#role').val(),

        $.ajax({
            type: 'POST',
            url: '/register',
            data: { 'username': username, 'password': password, 'role': role },
            success: function (response) {                
                // Перезагрузка страницы
                if (response.msg == "exists")
                    window.location.replace('/register?msg=' + response.msg); 
                else 
                    window.location.replace('/register');                                             
            },
            error: function (xhr, status, error) {
                console.log(error);               
            }
        });
    });    
});