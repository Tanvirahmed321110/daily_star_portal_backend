// Toast Notification Function
function showToast(type, title, message) {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icon = type === 'success' ? '✔' : '❌';

    toast.innerHTML = `
                <div class="toast-icon">${icon}</div>
                <div class="toast-content">
                    <div class="toast-title">${title}</div>
                    <div class="toast-message">${message}</div>
                </div>
                <button class="toast-close">&times;</button>
            `;

    container.appendChild(toast);

    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
        toast.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    });

    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
}

// Validate form before submit
function validateForm() {
    const rows = document.querySelectorAll('.product-table tbody tr');
    let hasError = false;
    let errorMessage = '';

    if (rows.length === 0) {
        showToast('error', 'Validation Error', 'Please add at least one product item');
        return false;
    }

    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const productSelect = row.querySelector('.product-category');
        const productName = row.querySelector('.product-name');
        const quantity = row.querySelector('.quantity');
        const reqDate = row.querySelector('.required-date');

        // validation with OR
        if (!productSelect.value && !productName.value.trim()) {
            hasError = true;
            if (!productSelect.value) {
                errorMessage = `Row ${i + 1}: Please select a product`;
            } else if (!productName.value.trim()) {
                errorMessage = `Row ${i + 1}: Please enter product name`;
            }
            break;
        }

        if (!quantity.value || quantity.value < 1) {
            hasError = true;
            errorMessage = `Row ${i + 1}: Please enter valid quantity (minimum 1)`;
            break;
        }

        if (!reqDate.value) {
            hasError = true;
            errorMessage = `Row ${i + 1}: Please select required date`;
            break;
        }
    }

    if (hasError) {
        showToast('error', 'Validation Failed', errorMessage);
        return false;
    }

    return true;
}


// Get selected priority
function getSelectedPriority() {
    const activeBtn = document.querySelector('.priority-btn.active');
    if (activeBtn) {
        return activeBtn.innerText.trim();
    }
    return '🟢 Low';
}

// Get all product data
function getProductData() {
    const rows = document.querySelectorAll('.product-table tbody tr');
    const products = [];

    rows.forEach((row, index) => {
        products.push({
            sl: index + 1,
            product: row.querySelector('.product-category').value,
            productName: row.querySelector('.product-name').value,
            quantity: row.querySelector('.quantity').value,
            requiredDate: row.querySelector('.required-date').value,
            remarks: row.querySelector('.remarks').value || 'N/A'
        });
    });

    return products;
}

// Submit form handler
document.getElementById('requisitionForm').addEventListener('submit', function (e) {
    e.preventDefault();

    if (!validateForm()) {
        return;
    }

    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.innerHTML;

    // Show loading state
    submitBtn.innerHTML = 'Submitting... ⏳';
    submitBtn.disabled = true;

    // Get form data
    const reqNumber = document.querySelector('.sl-badge').innerText;
    const reqDate = document.getElementById('reqDate').value;
    const priority = getSelectedPriority();
    const userName = document.querySelector('.user-field .value').innerText;
    const products = getProductData();

    // Simulate API call (replace with actual backend call)
    setTimeout(() => {
        // Success scenario
        showToast(
            'success',
            'Requisition Submitted!',
            `REQ-${reqNumber} has been successfully submitted. Thank you`
        );

        // Log to console for debugging
        console.log('=== Requisition Submitted ===');
        console.log('Requisition No:', reqNumber);
        console.log('Date:', reqDate);
        console.log('Priority:', priority);
        console.log('Submitted By:', userName);
        console.log('Products:', products);
        console.log('Total Items:', products.length);
        console.log('Total Quantity:', products.reduce((sum, p) => sum + parseInt(p.quantity), 0));



        // Reset button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 1500);

});


// Priority button handler
document.querySelectorAll('.priority-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        this.closest('.priority-group').querySelectorAll('.priority-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
    });
});

// Add product row handler
document.querySelector('.add-row-btn').addEventListener('click', function () {
    const tbody = document.querySelector('.product-table tbody');
    const rows = tbody.querySelectorAll('tr');
    const n = rows.length + 1;
    const newRow = rows[0].cloneNode(true);

    // Update row number
    newRow.querySelector('td').textContent = String(n).padStart(2, '0');

    // Reset all inputs in new row
    newRow.querySelectorAll('select').forEach(select => select.selectedIndex = 0);
    newRow.querySelectorAll('input').forEach(input => {
        if (input.type === 'number') {
            input.value = 1;
        } else if (input.type !== 'date') {
            input.value = '';
        }
    });

    tbody.appendChild(newRow);
    showToast('success', 'Row Added', `Product row ${n} has been added successfully`);
});

// Auto-update product name when category changes
document.addEventListener('change', function (e) {
    if (e.target.classList.contains('product-category')) {
        const row = e.target.closest('tr');
        const productNameInput = row.querySelector('.product-name');
        if (e.target.value) {
            productNameInput.value = e.target.value;
        }
    }
});