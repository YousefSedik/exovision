let currentSort = { column: -1, direction: 'asc' };
let currentPage = 1;
let entriesPerPage = 10;

function sortTable(columnIndex) {
    const table = document.getElementById('exoplanet-data-table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    // Determine sort direction
    if (currentSort.column === columnIndex) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.direction = 'asc';
        currentSort.column = columnIndex;
    }

    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();

        // Handle numeric values
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);

        if (!isNaN(aNum) && !isNaN(bNum)) {
            return currentSort.direction === 'asc' ? aNum - bNum : bNum - aNum;
        }

        // Handle text values
        return currentSort.direction === 'asc'
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });

    // Clear and repopulate tbody
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));

    // Update sort arrows
    updateSortArrows(columnIndex);
}

function updateSortArrows(activeColumn) {
    const headers = document.querySelectorAll('th .sort-arrow');
    headers.forEach((arrow, index) => {
        if (index === activeColumn) {
            arrow.textContent = currentSort.direction === 'asc' ? '↑' : '↓';
            arrow.style.opacity = '1';
        } else {
            arrow.textContent = '↕';
            arrow.style.opacity = '0.6';
        }
    });
}

function changePage(direction) {
    // Pagination logic would go here
    console.log('Change page:', direction);
}

function exportResults() {
    const table = document.getElementById('exoplanet-data-table');
    if (!table) {
        console.warn('No results table found to export');
        return;
    }

    const rows = [];

    // Extract header
    const headerCells = Array.from(table.querySelectorAll('thead th'));
    const header = headerCells.map(th => th.childNodes[0]?.textContent?.trim() || th.textContent.trim());
    rows.push(header);

    // Extract body
    const bodyRows = Array.from(table.querySelectorAll('tbody tr'));
    bodyRows.forEach(tr => {
        const cells = Array.from(tr.children).map(td => td.textContent.trim());
        rows.push(cells);
    });

    // CSV escaping
    const escapeCsv = (value) => {
        if (value == null) return '';
        const str = String(value).replace(/\r?\n|\r/g, ' ');
        if (/[",\n,]/.test(str)) {
            return '"' + str.replace(/"/g, '""') + '"';
        }
        return str;
    };

    const csv = rows.map(r => r.map(escapeCsv).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'exoplanet_predictions.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Search functionality
function initResultTable() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('#table-body tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    const exportBtn = document.getElementById('export-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportResults);
    }

    const entriesSelect = document.getElementById('entries-per-page');
    if (entriesSelect) {
        entriesSelect.addEventListener('change', function () {
            entriesPerPage = parseInt(this.value);
            // Repaginate table logic would go here
            console.log('Entries per page changed to:', entriesPerPage);
        });
    }
}

// Expose initializer for dynamic loads
if (typeof window !== 'undefined') {
    window.initResultTable = initResultTable;
}

// Auto-initialize if elements already in DOM (e.g., normal page load)
try {
    initResultTable();
} catch (e) {
    // Safe no-op if DOM not ready
}
