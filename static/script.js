document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("editModal");
    const editInput = document.getElementById("editInput");
    const editForm = document.getElementById("editForm");
    const cancelBtn = document.querySelector(".cancel-btn");

    document.querySelectorAll(".edit-btn").forEach(btn => {
        btn.addEventListener("click", e => {
            e.preventDefault();
            const index = btn.dataset.index;
            const task = btn.dataset.task;

            editInput.value = task;
            editForm.action = `/edit/${index}`;
            modal.classList.add("active");
        });
    });

    cancelBtn.addEventListener("click", () => {
        modal.classList.remove("active");
    });

    modal.addEventListener("click", e => {
        if (e.target === modal) {
            modal.classList.remove("active");
        }
    });
});