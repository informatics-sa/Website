/**
 * Sortable Tables - Add sorting functionality to HTML tables
 * 
 * Usage:
 * - Add 'sortable' attribute to <table> element: <table sortable>
 * - Add 'sort-value' attribute to <th> elements: sort-value="num" or sort-value="string"
 * - Optionally add initial sort state: sort-state="asc" or sort-state="desc"
 */

(function() {
    'use strict';

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSortableTables);
    } else {
        initSortableTables();
    }

    function initSortableTables() {
        const tables = document.querySelectorAll('table[sortable]');
        tables.forEach(table => setupSortableTable(table));
    }

    function setupSortableTable(table) {
        const thead = table.querySelector('thead');
        if (!thead) return;

        const headers = thead.querySelectorAll('th[sort-value]');
        
        headers.forEach((header, index) => {
            // Add styling to indicate sortable column
            header.style.cursor = 'pointer';
            header.style.userSelect = 'none';
            header.style.position = 'relative';
            header.style.paddingRight = '20px';

            // Create sort indicator
            const indicator = document.createElement('span');
            indicator.className = 'sort-indicator';
            indicator.style.position = 'absolute';
            indicator.style.right = '5px';
            indicator.style.top = '50%';
            indicator.style.transform = 'translateY(-50%)';
            indicator.style.fontSize = '0.8em';
            indicator.style.opacity = '0.5';
            
            // Set initial state
            const initialState = header.getAttribute('sort-state') || 'none';
            header.setAttribute('data-sort-state', initialState);
            updateIndicator(indicator, initialState);
            
            header.appendChild(indicator);

            // Add click handler
            header.addEventListener('click', () => {
                handleSort(table, header, index+1);
            });

            // Apply initial sort if specified
            if (initialState !== 'none') {
                sortTable(table, index+1, header.getAttribute('sort-value'), initialState);
            }
        });
    }

    function handleSort(table, header, columnIndex) {
        const currentState = header.getAttribute('data-sort-state') || 'none';
        let newState;

        // Cycle through states: none -> asc -> desc -> none
        if (currentState === 'none') {
            newState = 'asc';
        } else if (currentState === 'asc') {
            newState = 'desc';
        } else {
            newState = 'none';
        }

        // Reset all other headers to 'none'
        const allHeaders = table.querySelectorAll('th[sort-value]');
        allHeaders.forEach(h => {
            if (h !== header) {
                h.setAttribute('data-sort-state', 'none');
                const ind = h.querySelector('.sort-indicator');
                if (ind) updateIndicator(ind, 'none');
            }
        });

        // Update current header
        header.setAttribute('data-sort-state', newState);
        const indicator = header.querySelector('.sort-indicator');
        updateIndicator(indicator, newState);

        // Perform sort
        if (newState === 'none') {
            // Restore original order
            restoreOriginalOrder(table);
        } else {
            const sortType = header.getAttribute('sort-value');
            sortTable(table, columnIndex, sortType, newState);
        }
    }

    function updateIndicator(indicator, state) {
        if (state === 'asc') {
            indicator.textContent = '▲';
            indicator.style.opacity = '1';
        } else if (state === 'desc') {
            indicator.textContent = '▼';
            indicator.style.opacity = '1';
        } else {
            indicator.textContent = '⇅';
            indicator.style.opacity = '0.5';
        }
    }

    function sortTable(table, columnIndex, sortType, direction) {
        const tbody = table.querySelector('tbody');
        if (!tbody) return;

        // Store original order if not already stored
        if (!tbody.hasAttribute('data-original-order')) {
            const rows = Array.from(tbody.querySelectorAll('tr'));
            rows.forEach((row, index) => {
                row.setAttribute('data-original-index', index);
            });
            tbody.setAttribute('data-original-order', 'true');
        }

        const rows = Array.from(tbody.querySelectorAll('tr'));
        console.log(rows.map(v => v.cells[columnIndex].innerText));
        console.log('Sorting', rows.length, 'rows by column', columnIndex, 'type:', sortType, 'direction:', direction);
        
        rows.sort((a, b) => {
            const aCell = a.cells[columnIndex];
            const bCell = b.cells[columnIndex];
            
            if (!aCell || !bCell) return 0;

            let aValue = aCell.textContent.trim();
            let bValue = bCell.textContent.trim();

            let comparison = 0;

            if (sortType === 'num') {
                // Parse as numbers
                const aNum = parseFloat(aValue.replace(/[^0-9.-]/g, '')) || 0;
                const bNum = parseFloat(bValue.replace(/[^0-9.-]/g, '')) || 0;
                comparison = aNum - bNum;
            } else {
                // String comparison (case-insensitive)
                comparison = aValue.toLowerCase().localeCompare(bValue.toLowerCase());
            }

            return direction === 'asc' ? comparison : -comparison;
        });

        // Re-append rows in sorted order
        rows.forEach(row => tbody.appendChild(row));
    }

    function restoreOriginalOrder(table) {
        const tbody = table.querySelector('tbody');
        if (!tbody) return;

        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.sort((a, b) => {
            const aIndex = parseInt(a.getAttribute('data-original-index') || '0');
            const bIndex = parseInt(b.getAttribute('data-original-index') || '0');
            return aIndex - bIndex;
        });

        rows.forEach(row => tbody.appendChild(row));
    }

    // Export for manual initialization if needed
    window.initSortableTables = initSortableTables;
})();