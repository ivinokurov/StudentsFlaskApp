$(document).ready(function() {
    $('#themeToggle').change(function() {
        $.ajax({
            url: '/toggle_theme', 
            method: 'POST',
            // Отправляем состояние чекбокса
            data: { dark_theme: $(this).is(':checked') },  
            success: function(response) {
                location.reload();              
            },
            error: function(xhr, status, error) {
                console.error('Ошибка:', error);
            }
        });
    });
});