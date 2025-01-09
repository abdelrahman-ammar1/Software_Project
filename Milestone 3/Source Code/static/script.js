document.addEventListener("DOMContentLoaded", () => {
    // Example: Confirm delete action
    document.querySelectorAll('button[name="action"][value="delete"]').forEach(button => {
        button.addEventListener("click", event => {
            if (!confirm("Are you sure you want to delete this item?")) {
                event.preventDefault();
            }
        });
    });
});
