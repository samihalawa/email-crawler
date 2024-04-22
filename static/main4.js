$(document).ready(function() {
    // Utilizamos el protocolo 'https' en lugar de 'http' para evitar peticiones no seguras
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    
    $('#searchForm').submit(function(event) {
        event.preventDefault();
        var searchQuery = $('#searchTerm').val();
        $('#results').empty();
        socket.emit('start_search', {search_query: searchQuery});
    });

    $('#showResultsBtn').click(function() {
        $('#myModal').css('display', 'block');
        loadEmails();
    });

    $('.close').click(function() {
        $('#myModal').css('display', 'none');
    });

    $(window).click(function(event) {
        if (event.target == $('#myModal')[0]) {
            $('#myModal').css('display', 'none');
        }
    });
function loadEmails() {
    $.get('/get_emails', function(data) {
        var emails = data.split('\n');
        var modalBody = $('#modalBody');
        modalBody.empty();
        var uniqueDomains = {}; // Objeto para almacenar los dominios únicos y sus correos electrónicos correspondientes
        for (var i = 0; i < emails.length; i++) {
            var emailInfo = emails[i].split(',');
            var email = emailInfo[1].trim();
            var domain = email.split('@')[1]; // Obtener el dominio del correo electrónico
            // Verificar si el correo electrónico tiene un formato válido y no está en la lista de dominios repetidos
            if (isValidEmail(email) && !(domain in uniqueDomains)) {
                var page_title = emailInfo[2].trim();
                var url = emailInfo[3].trim();
                var resultElement = $('<div>').addClass('p-4 bg-white shadow-md mb-4');
                resultElement.append($('<p>').addClass('text-lg font-bold').text('邮箱: ' + email));
                resultElement.append($('<p>').addClass('text-sm italic').text('页面标题: ' + page_title));
                resultElement.append($('<p>').addClass('text-xs').text('网址: ' + url));
                modalBody.append(resultElement);
                // Agregar el dominio al objeto de dominios únicos
                uniqueDomains[domain] = true;
            }
        }
    });
}

// Función auxiliar para verificar si un string es un email válido
function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}


    
    socket.on('new_email', function(data) {
        var resultElement = $('<div>').addClass('p-4 bg-white shadow-md mb-4');
        resultElement.append($('<p>').addClass('text-lg font-bold').text('邮箱: ' + data.email));
        resultElement.append($('<p>').addClass('text-sm italic').text('页面标题: ' + data.page_title));
        resultElement.append($('<p>').addClass('text-xs').text('网址: ' + data.url));
        $('#results').append(resultElement);
    });

    // Añadir un selector de cantidad de emails al formulario con valor predeterminado de 10
    var emailQuantitySlider = $('#emailQuantitySlider');
    var emailQuantityDisplay = $('#emailQuantityDisplay');
    emailQuantitySlider.on('input', function() {
        emailQuantityDisplay.text($(this).val());
    });
    emailQuantityDisplay.text(emailQuantitySlider.val());
});


