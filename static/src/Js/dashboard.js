
// =============== For Status Filter
document.addEventListener('DOMContentLoaded', function () {

    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const emptyFilter = document.getElementById('emptyFilter');


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

    // Empty sms here
    if (emptyFilter) {
        emptyFilter.style.display = visibleCount === 0 ? '' : 'none';
    }}

    if (searchInput) searchInput.addEventListener('input', filterTable);
    if (statusFilter) statusFilter.addEventListener('change', filterTable);
});