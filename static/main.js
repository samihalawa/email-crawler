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
            for (var i = emails.length - 1; i >= 0; i--) {
                var emailInfo = emails[i].split(',');
                var email = emailInfo[1].trim();
                var page_title = emailInfo[2].trim();
                var url = emailInfo[3].trim();
                var resultElement = $('<div>').addClass('p-4 bg-white shadow-md mb-4');
                resultElement.append($('<p>').addClass('text-lg font-bold').text('邮箱: ' + email));
                resultElement.append($('<p>').addClass('text-sm italic').text('页面标题: ' + page_title));
                resultElement.append($('<p>').addClass('text-xs').text('网址: ' + url));
                modalBody.append(resultElement);
            }
        });
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


