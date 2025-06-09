// Exam Statistics Calculator
// Manages statistics display for exam score tables

// Cookie utilities
function setCookie(name, value, days = 30) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Load settings from cookies
const COOKIE_NAME = 'exam_stats_settings';
const SETTING_IDS = ['show_maximums', 'show_stddevs', 'show_medians', 'show_averages', 'show_distincts'];

function load_settings() {
    const settingsJson = getCookie(COOKIE_NAME);
    if (settingsJson == null) {
        save_settings();
        load_settings();
        return;
    }

    try {
        const settings = JSON.parse(settingsJson);
        // Apply settings to form elements
        Object.keys(settings).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                element.checked = settings[key];
            }
        });
    } catch (e) {
        console.error('Error loading settings (invalid json):', e);

        save_settings();
        load_settings();
    }
}

// Save settings to cookies
function save_settings() {
    const settings = {};
    
    SETTING_IDS.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            settings[id] = element.checked;
        }
    });
    
    setCookie(COOKIE_NAME, JSON.stringify(settings));
    console.log('Settings saved:', settings);
}

// Get current settings from form
function get_current_settings() {
    const settings = {};
    
    SETTING_IDS.forEach(id => {
        const element = document.getElementById(id);
        settings[id] = element ? element.checked : false;
    });

    const settingsJson = JSON.parse(getCookie(COOKIE_NAME));
    

    SETTING_IDS.forEach(id => {
        settings[id] = settingsJson[id] ? settingsJson[id] : false;
    }); 
    
    return settings;
}

// Statistical calculation functions
function calculate_max(values) {
    return Math.max(...values);
}

function calculate_min(values) {
    return Math.min(...values);
}

function calculate_sum(values) {
    return values.reduce((sum, val) => sum + val, 0);
}

function calculate_average(values) {
    return values.length > 0 ? calculate_sum(values) / values.length : 0;
}

function calculate_median(values) {
    if (values.length === 0) return 0;
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 === 0 
        ? (sorted[mid - 1] + sorted[mid]) / 2 
        : sorted[mid];
}

function calculate_stddev(values) {
    if (values.length <= 1) return 0;
    const avg = calculate_average(values);
    const squareDiffs = values.map(val => Math.pow(val - avg, 2));
    const avgSquareDiff = calculate_average(squareDiffs);
    return Math.sqrt(avgSquareDiff);
}

function calculate_distinct_count(values) {
    return new Set(values).size;
}

// Extract numeric values from table column
function extract_column_values(table, columnIndex, excludeStatRows = true) {
    const values = [];
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        // Skip statistics rows
        if (excludeStatRows && row.classList.contains('stat-row')) {
            return;
        }
        
        const cells = row.querySelectorAll('td, th');
        if (cells[columnIndex]) {
            const text = cells[columnIndex].textContent.trim();
            const num = parseFloat(text);
            if (!isNaN(num)) {
                values.push(num);
            }
        }
    });
    
    return values;
}

// Get column headers
function get_column_headers(table) {
    const headers = [];
    const headerRow = table.querySelector('thead tr, tbody tr:first-child');
    if (headerRow) {
        const cells = headerRow.querySelectorAll('th, td');
        cells.forEach(cell => {
            headers.push(cell.textContent.trim());
        });
    }
    return headers;
}

// Create a statistics row
function create_stat_row(table, statType, statName, statFunction, countRows=0) {
    const headers = get_column_headers(table);
    const row = document.createElement('tr');
    row.classList.add('stat-row', `stat-${statType}`);
    // row.style.backgroundColor = '#f8f9fa';
    row.style.fontWeight = 'bold';
    // row.style.borderTop = '2px solid #dee2e6';
    
    // First cell with stat name

    const emptyCell = document.createElement('td');
    row.appendChild(emptyCell);

    const nameCell = document.createElement('td');
    nameCell.textContent = statType == 'distincts' ? statName + ` (${countRows})` : statName;
    nameCell.style.fontWeight = 'bold';
    // nameCell.style.color = '#495057';
    row.appendChild(nameCell);
    
    // For maximums, we need to calculate other columns first to sum them for the sum column
    let calculatedValues = [];
    
    // Calculate stats for each column (skip first column which is usually names)
    for (let i = 2; i < headers.length; i++) {
        const cell = document.createElement('td');
        const values = extract_column_values(table, i);
        
        if (values.length > 0) {
            let result;
            
            // Special handling for maximums with sum column (assuming sum is column index 1)
            if (statType === 'maximums' && i === 1 && headers[i].toLowerCase().includes('sum')) {
                // Sum will be calculated after we get all other maximums
                result = 0; // Placeholder
            } else {
                result = statFunction(values);
                if (statType === 'maximums') {
                    calculatedValues.push(result);
                }
            }
            
            // Format the result
            if (statType === 'distincts') {
                cell.textContent = result.toString();
            } else {
                cell.textContent = Number.isInteger(result) ? result.toString() : result.toFixed(2);
            }
        } else {
            cell.textContent = '-';
        }
        
        row.appendChild(cell);
    }
    
    // Special handling: Update sum column for maximums row
    if (statType === 'maximums' && calculatedValues.length > 0) {
        const sumColumnIndex = 2;
        if (sumColumnIndex > 0) { // Found sum column (and it's not the first column)
            const sumCell = row.children[sumColumnIndex]; // +1 because first cell is the stat name
            const sumOfMaximums = calculatedValues.reduce((sum, val) => sum + val, 0) - calculatedValues[0];
            sumCell.textContent = Number.isInteger(sumOfMaximums) ? sumOfMaximums.toString() : sumOfMaximums.toFixed(2);
        }
    }
    
    return row;
}

// Remove existing statistics rows from table
function remove_stat_rows(table) {
    const statRows = table.querySelectorAll('.stat-row');
    statRows.forEach(row => row.remove());
}

// Add statistics rows to table based on settings
function add_stat_rows(table, settings) {
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    
    var statConfigs = [];
    if (getCookie('lang') == 'en') {

        statConfigs = [
            { key: 'show_maximums', name: 'Maximum', type: 'maximums', func: calculate_max },
            { key: 'show_averages', name: 'Average', type: 'averages', func: calculate_average },
            { key: 'show_medians', name: 'Median', type: 'medians', func: calculate_median },
            { key: 'show_stddevs', name: 'Standard deviation', type: 'stddevs', func: calculate_stddev },
            { key: 'show_distincts', name: 'Distinct', type: 'distincts', func: calculate_distinct_count }
        ];
    } else {
        statConfigs = [
            { key: 'show_maximums', name: 'أعلى درجة', type: 'maximums', func: calculate_max },
            { key: 'show_averages', name: 'المتوسط', type: 'averages', func: calculate_average },
            { key: 'show_medians', name: 'الوسيط', type: 'medians', func: calculate_median },
            { key: 'show_stddevs', name: 'الانحراف المعياري', type: 'stddevs', func: calculate_stddev },
            { key: 'show_distincts', name: 'بدون تكرار', type: 'distincts', func: calculate_distinct_count }
        ];
    }
        
    // Add enabled statistics in order
    const rowsCount = tbody.childElementCount;

    statConfigs.forEach(config => {
        if (settings[config.key]) {
            const statRow = create_stat_row(table, config.type, config.name, config.func, rowsCount);
            tbody.insertBefore(statRow, tbody.firstChild);
        }
    });
}

// Main function to refresh all tables
function refresh_tables() {
    const settings = get_current_settings();
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
        // Remove existing stat rows
        remove_stat_rows(table);
        
        // Add new stat rows based on current settings
        add_stat_rows(table, settings);
    });
    
    console.log('Tables refreshed with settings:', settings);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Load saved settings
    load_settings();
    
    // Refresh tables with loaded settings
    refresh_tables();
    
    // Add event listeners to form elements
    const settingIds = ['show_maximums', 'show_stddevs', 'show_medians', 'show_averages', 'show_distincts'];
    settingIds.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('change', function() {
                save_settings();
                refresh_tables();
            });
        }
    });
    
    console.log('Exam statistics system initialized');
});

// Export functions for manual use
window.examStats = {
    refresh_tables,
    save_settings,
    load_settings,
    get_current_settings
};

