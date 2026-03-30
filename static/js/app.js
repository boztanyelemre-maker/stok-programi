// ===== NARON STOK YONETIM - MAIN JS =====

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    document.querySelectorAll('.alert-dismissible').forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // Sidebar active state
    var currentPath = window.location.pathname;
    document.querySelectorAll('.menu-link').forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            // Open parent collapse if sub-link
            var parent = link.closest('.collapse');
            if (parent) {
                parent.classList.add('show');
                var trigger = document.querySelector('[href="#' + parent.id + '"]');
                if (trigger) trigger.setAttribute('aria-expanded', 'true');
            }
        }
    });

    // Dynamic formset - Add row
    var addButtons = document.querySelectorAll('.add-formset-row');
    addButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var formsetId = this.dataset.formset;
            var container = document.getElementById(formsetId);
            var totalForms = document.getElementById('id_' + formsetId + '-TOTAL_FORMS');
            var formIdx = parseInt(totalForms.value);

            var emptyRow = container.querySelector('.formset-row:last-child');
            if (emptyRow) {
                var newRow = emptyRow.cloneNode(true);
                // Update form indices
                newRow.innerHTML = newRow.innerHTML.replace(
                    new RegExp('(-\\d+-)|(___prefix___)','g'),
                    '-' + formIdx + '-'
                );
                // Clear values
                newRow.querySelectorAll('input:not([type=hidden])').forEach(function(inp) {
                    inp.value = '';
                });
                newRow.querySelectorAll('select').forEach(function(sel) {
                    sel.selectedIndex = 0;
                });
                container.appendChild(newRow);
                totalForms.value = formIdx + 1;
            }
        });
    });

    // Cascade dropdowns: Main Category -> Sub Category
    var mainCatSelect = document.getElementById('id_main_category');
    if (mainCatSelect) {
        mainCatSelect.addEventListener('change', function() {
            var subCatSelect = document.getElementById('id_sub_category');
            if (!subCatSelect) return;
            var mainId = this.value;
            subCatSelect.innerHTML = '<option value="">---------</option>';
            if (mainId) {
                fetch('/urunler/api/alt-kategoriler/?main_category_id=' + mainId)
                    .then(function(r) { return r.json(); })
                    .then(function(data) {
                        data.forEach(function(item) {
                            var opt = document.createElement('option');
                            opt.value = item.id;
                            opt.textContent = item.name;
                            subCatSelect.appendChild(opt);
                        });
                    });
            }
        });
    }

    // Cascade dropdowns: Project -> Warehouse
    var projectSelect = document.getElementById('id_project');
    if (projectSelect) {
        projectSelect.addEventListener('change', function() {
            var whSelect = document.getElementById('id_warehouse');
            if (!whSelect) return;
            var projectId = this.value;
            whSelect.innerHTML = '<option value="">---------</option>';
            if (projectId) {
                fetch('/stok/api/depolar/?project_id=' + projectId)
                    .then(function(r) { return r.json(); })
                    .then(function(data) {
                        data.forEach(function(item) {
                            var opt = document.createElement('option');
                            opt.value = item.id;
                            opt.textContent = item.name;
                            whSelect.appendChild(opt);
                        });
                    });
            }
        });
    }

    // Delete confirmation
    document.querySelectorAll('.delete-confirm').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Bu kaydi silmek istediginize emin misiniz?')) {
                e.preventDefault();
            }
        });
    });
});
