$(document).ready(function() {
    var socketProtocol = (window.location.protocol.includes('https') ? 'wss' : 'ws') + '://';
    var socket = io.connect(socketProtocol + document.domain + ':' + location.port, {secure: window.location.protocol.includes('https')});
    
    $('#searchForm').submit(function(event) {
        event.preventDefault();
        var searchQuery = $('#searchTerm').val();
        var numResults = $('#emailQuantitySlider').val();
        $('#resultsemail').empty();
        socket.emit('start_search', {search_query: searchQuery, num_results: numResults});
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

    var displayedDomains = {};

    function loadEmails() {
        $.get('/get_emails', function(data) {
            var emails = data.split('\n');
            var modalBody = $('#modalBody');
            modalBody.empty();
            displayedDomains = {};
            emails.forEach(function(emailInfoStr) {
                var emailInfo = emailInfoStr.split(',');
                var email = emailInfo[1].trim();
                if (isValidEmail(email)) {
                    var domain = email.split('@')[1];
                    if (!(domain in displayedDomains)) {
                        var page_title = emailInfo[2].trim();
                        var url = emailInfo[3].trim();
                        var resultElement = $('<div>').addClass('relative p-4 bg-white shadow-md mb-4');
                        resultElement.append($('<p>').addClass('text-lg font-bold').text('Email: ' + email));
                        resultElement.append($('<p>').addClass('text-sm italic').text(page_title));
                        resultElement.append($('<p>').addClass('text-xs').text(url));
                        modalBody.append(resultElement);
                        displayedDomains[domain] = true;
                    }
                }
            });
        });
    }

    function isValidEmail(email) {
        var domain = email.substring(email.lastIndexOf("@") + 1);
        var domainParts = domain.split('.');
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        var tooManyNumbers = (email.replace(/[^0-9]/g,"").length > email.length * 0.5); // More than 50% of the email are digits
        var validDomainLength = domain.length >= 3 && domainParts.every(part => part.length >= 3);
        var validEmailLength = email.length >= 5;
        return emailRegex.test(email) && validDomainLength && !tooManyNumbers && validEmailLength;
    }

    socket.on('new_email', function(data) {
        var email = data.email.trim();
        if (isValidEmail(email)) {
            var domain = email.split('@')[1];
            if (!(domain in displayedDomains)) {
                var resultElement = $('<div>').addClass('relative p-4 bg-white shadow-md mb-4');
                resultElement.append($('<p>').addClass('text-lg font-bold').text('Email: ' + email));
                resultElement.append($('<p>').addClass('text-sm italic').text(data.page_title));
                resultElement.append($('<p>').addClass('text-xs').text(data.url));
                $('#resultsemail').append(resultElement);
                displayedDomains[domain] = true;
            }
        }
    });

    var emailQuantitySlider = $('#emailQuantitySlider');
    var emailQuantityDisplay = $('#emailQuantityDisplay');
    emailQuantitySlider.on('input', function() {
        emailQuantityDisplay.text($(this).val());
    });
    emailQuantityDisplay.text(emailQuantitySlider.val());
});
