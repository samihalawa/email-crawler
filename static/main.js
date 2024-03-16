$(document).ready(function() {
    // We use the 'https' protocol instead of 'http' to avoid insecure requests
    var socketProtocol = (window.location.protocol.includes('https') ? 'wss' : 'ws') + '://';
    var socket = io.connect(socketProtocol + document.domain + ':' + location.port, {secure: window.location.protocol.includes('https')});
    
  $('#searchForm').submit(function(event) {
    event.preventDefault();
    var searchQuery = $('#searchTerm').val();
    var numResults = $('#emailQuantitySlider').val(); // Captura el valor seleccionado en el slider
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

    var displayedDomains = {}; // Object to keep track of displayed domains

    function loadEmails() {
        $.get('/get_emails', function(data) {
            var emails = data.split('\n');
            var modalBody = $('#modalBody');
            modalBody.empty();
            displayedDomains = {}; // Reset displayed domains
            for (var i = 0; i < emails.length; i++) {
                var emailInfo = emails[i].split(',');
                var email = emailInfo[1].trim();
                var domain = email.split('@')[1]; // Get the domain from the email
                // Check if the email is in valid format and not in the list of displayed domains
                if (isValidEmail(email) && !(domain in displayedDomains)) {
                    var page_title = emailInfo[2].trim();
                    var url = emailInfo[3].trim();
                    var resultElement = $('<div>').addClass('relative p-4 bg-white shadow-md mb-4');
                    resultElement.append($('<p>').addClass('text-lg font-bold').text('Email:'+email));
                    resultElement.append($('<p>').addClass('text-sm italic').text(page_title));
                    resultElement.append($('<p>').addClass('text-xs').text(url));
                    var copyButton = $('<button>').addClass('absolute top-0 right-0 mt-1 mr-1 p-1 bg-gray-200 rounded text-gray-600 hover:bg-gray-300 hover:text-gray-800 focus:outline-none');
                    copyButton.html('<span>Send Mail</span><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2m-4 0V3H5a2 2 0 00-2 2v12a2 2 0 002 2h2v4l7-5-7-5v4z" /></svg>');
                    copyButton.click(function() {
                        var emailText = $(this).siblings('p.text-lg.font-bold').text().replace('Email: ', '');
                        navigator.clipboard.writeText(emailText).then(function() {
                            alert('Email copied to clipboard: ' + emailText);
                        }, function() {
                            alert('Failed to copy email to clipboard.');
                        });
                    });
                    resultElement.append(copyButton);
                    modalBody.append(resultElement);
                    // Add the domain to the list of displayed domains
                    displayedDomains[domain] = true;
                }
            }
        });
    }

    // Helper function to check if a string is a valid email
    function isValidEmail(email) {
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    socket.on('new_email', function(data) {
        var email = data.email.trim();
        var domain = email.split('@')[1]; // Get the domain from the email
        // Check if the email is in valid format and not in the list of displayed domains
        if (isValidEmail(email) && !(domain in displayedDomains)) {
            var resultElement = $('<div>').addClass('relative p-4 bg-white shadow-md mb-4');
            resultElement.append($('<p>').addClass('text-lg font-bold').text('Email: '+email));
            resultElement.append($('<p>').addClass('text-sm italic').text(data.page_title));
            resultElement.append($('<p>').addClass('text-xs').text(data.url));
            var copyButton = $('<button>').addClass('absolute top-0 right-0 mt-1 mr-1 p-1 bg-gray-200 rounded text-gray-600 hover:bg-gray-300 hover:text-gray-800 focus:outline-none');
            copyButton.html('<span>Send Mail</span> <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2m-4 0V3H5a2 2 0 00-2 2v12a2 2 0 002 2h2v4l7-5-7-5v4z" /></svg>');
            copyButton.click(function() {
                var emailText = $(this).siblings('p.text-lg.font-bold').text().replace('Email: ', '');
                navigator.clipboard.writeText(emailText).then(function() {
                    alert('Email copied to clipboard: ' + emailText);
                }, function() {
                    alert('Failed to copy email to clipboard.');
                });
            });
            resultElement.append(copyButton);
            $('#resultsemail').append(resultElement);
            // Add the domain to the list of displayed domains
            displayedDomains[domain] = true;
        }
    });

    // Add an email quantity selector to the form with default value of 10
    var emailQuantitySlider = $('#emailQuantitySlider');
    var emailQuantityDisplay = $('#emailQuantityDisplay');
    emailQuantitySlider.on('input', function() {
        emailQuantityDisplay.text($(this).val());
    });
    emailQuantityDisplay.text(emailQuantitySlider.val());
});
