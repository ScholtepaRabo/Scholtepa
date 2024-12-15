// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Add sorting functionality
    document.querySelectorAll('th').forEach(header => {
        header.addEventListener('click', () => {
            const table = header.closest('table');
            const index = Array.from(header.parentElement.children).indexOf(header);
            sortTable(table, index);
        });
    });
});

function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sorted = rows.sort((a, b) => {
        const aCol = a.querySelectorAll('td')[column].textContent;
        const bCol = b.querySelectorAll('td')[column].textContent;
        return aCol.localeCompare(bCol);
    });

    tbody.innerHTML = '';
    sorted.forEach(row => tbody.appendChild(row));
}