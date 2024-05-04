document.addEventListener('DOMContentLoaded', function() {
    const grid = new tui.Grid({
        el: document.getElementById('grid'),
        data: {
            api: {
                readData: { url: '/api/readData', method: 'GET' }
            }
        },
        scrollX: true,
        scrollY: true,
        rowHeaders: ['checkbox'],
        pageOptions: {
            perPage: 10
        },
        columns: [
            { header: 'Search Term', name: 'search_query' },
            { header: 'Email', name: 'email' },
            { header: 'Page Title', name: 'page_title' },
            { header: 'URL', name: 'url' }
        ]
    });

    grid.on('response', function(data) {
        console.log('Data loaded successfully:', data);
    });

    grid.on('error', function(error) {
        console.error('Error loading data:', error);
    });
});
