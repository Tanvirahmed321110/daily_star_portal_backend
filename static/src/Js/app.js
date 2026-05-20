

const addRowBtn = document.querySelector('.add-row-btn')
const tbody = document.querySelector('#js-product-table-body')
// console.log(addRowBtn,tbody)

// =========================
// Add New Row
// =========================
addRowBtn.addEventListener('click', function () {

    const rows = tbody.querySelectorAll('tr')
    const sl = rows.length + 1

    // first row er select option copy
    const products = tbody.querySelector('.product-category')

    const newRow = document.createElement('tr')
    newRow.innerHTML = `
        <td class="sl-no"
            style="color:var(--muted);font-family:'DM Mono',monospace;font-size:12px;">
            ${String(sl).padStart(2, '0')}
        </td>

        <td>
            <select class="product-category" name="product_id" onchange="onCategoryChange(this)">
                ${products.innerHTML}
            </select>
        </td>

        <td>
            <input type="text"
                   name="description"
                   class="product-name"
                   placeholder="Product Name"/>
        </td>

        <td>
            <input type="number"
                   name="required_qty"
                   class="quantity"
                   value="1"
                   min="1"/>
        </td>

        <td>
            <input type="date"
                   name="required_on"
                   required="required"
                   class="required-date"/>
        </td>

        <td>
            <input type="text"
                   class="remarks"
                   name="remarks"
                   placeholder="Additional notes..."/>
        </td>
    `

    tbody.appendChild(newRow)

})


// When Select Product Then Product Name auto set
function onCategoryChange(selectEl) {

    const tr = selectEl.closest('tr')

    const nameInput = tr.querySelector('.product-name')

    const productName =
        selectEl.options[selectEl.selectedIndex].text

    nameInput.value = productName
}



function validateRequisitionForm() {

    const rows = document.querySelectorAll('#js-product-table-body tr')

    for (let row of rows) {

        const product = row.querySelector('.product-category')?.value.trim()
        const desc = row.querySelector('.product-name')?.value.trim()

        // empty
        if (!product && !desc) {
            return false
        }
    }

    return true
}

const form = document.querySelector('#requisitionForm')
form.addEventListener('submit', function (e) {

    const ok = validateRequisitionForm()

    if (!ok) {
        e.preventDefault()
        alert("Please fill at least Product or Product Name in one row.")
    }
})


// Active class add and value set
const priorityBtns = document.querySelectorAll('.priority-btn')
if (priorityBtns) {
    priorityBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            // remove all active class
            priorityBtns.forEach(b => b.classList.remove('active'))
            this.classList.add('active')
            document.getElementById('priority-input').value = this.dataset.value
        })
    })
}
