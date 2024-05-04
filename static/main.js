
document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect(window.location.origin);
    var form = document.getElementById('searchForm');
    form.onsubmit = function(e) {
        e.preventDefault();
        var searchTerm = document.getElementById('searchTerm').value;
        var quantity = document.getElementById('emailQuantitySlider').value;
        var dataTypes = [];
        document.querySelectorAll("input[name='dataType']:checked").forEach((elem) => {
            dataTypes.push(elem.value);
        });
        socket.emit('start_search', { search_query: searchTerm, num_results: quantity, data_type: dataTypes.join('_') });
    };
    socket.on('new_contact', function(data) {
        console.log('New contact found: ' + data.contact);
    });
});
