
// =============== For Status Filter
document.addEventListener('DOMContentLoaded', function () {

    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const emptyFilter = document.getElementById('emptyFilter');

    // // ✅ Duplicate Option Remove
    const seen = new Set();
    Array.from(statusFilter.options).forEach(option => {
        if (option.value === '') return;
        if (seen.has(option.value)) {
            option.remove();
        } else {
            seen.add(option.value);
        }
    });

    // ✅ Filter Function
    function filterTable() {
        const searchVal = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const statusVal = statusFilter.value.toLowerCase().trim();
        const rows = document.querySelectorAll('#tableBody .table-row');

        let visibleCount = 0;

        rows.forEach(row => {
            const name = (row.dataset.name || '').toLowerCase();
            const status = (row.dataset.status || '').toLowerCase();

            const matchSearch = searchVal === '' || name.includes(searchVal);
            const matchStatus = statusVal === '' || status === statusVal;

            if (matchSearch &&  matchStatus) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });

    // empty sms
    if (emptyFilter) {
        emptyFilter.style.display = visibleCount === 0 ? '' : 'none';
    }}

    if (searchInput) searchInput.addEventListener('input', filterTable);
    if (statusFilter) statusFilter.addEventListener('change', filterTable);
});