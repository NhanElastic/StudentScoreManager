let currentItemId = null;
let currentItemType = null;
let isAdding = false;

const API_BASE = "http://localhost:8000";

async function fetchAPI(endpoint, method = "GET", data = null) {
    console.log(`Making ${method} request to ${endpoint}`);
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method,
            headers: { "Content-Type": "application/json" },
            body: data ? JSON.stringify(data) : null,
        });
        console.log("Response status:", response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Error response:", errorText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Full error:", error);
        throw error;
    }
}

// Student API functions
async function getStudents() {
    return await fetchAPI("/api/students/list");
}

async function createStudent(student) {
    return await fetchAPI("/api/students/add", "POST", {
        name: student.name,
        class_name: student.class,
        dob: student.dob,
    });
}

async function updateStudent(id, updates) {
    return await fetchAPI(`/api/students/${id}`, "PUT", updates);
}

async function deleteStudent(id) {
    return await fetchAPI(`/api/students/${id}`, "DELETE");
}

document.addEventListener("DOMContentLoaded", async () => {
    try {
        await Promise.all([
            refreshTable("student"),
            refreshTable("subject"),
            refreshTable("score"),
        ]);
        console.log("flagged");

        // Set up search event listeners
        document
            .getElementById("studentSearch")
            .addEventListener("keyup", filterStudents);
        document
            .getElementById("subjectSearch")
            .addEventListener("keyup", filterSubjects);
        document
            .getElementById("scoreSearch")
            .addEventListener("keyup", filterScores);
    } catch (error) {
        console.error("Initialization error:", error);
        showWarning("Failed to load initial data");
    }
});

// Switch between tabs
function switchTab(tabName) {
    document
        .querySelectorAll(".tab")
        .forEach((tab) => tab.classList.remove("active"));
    document
        .querySelectorAll(".tab-content")
        .forEach((content) => content.classList.remove("active"));

    document
        .querySelector(`.tab[onclick="switchTab('${tabName}')"]`)
        .classList.add("active");
    document.getElementById(`${tabName}-tab`).classList.add("active");
}

// Show add form
function showAddForm(type) {
    if (isAdding) return;
    isAdding = true;
    currentItemType = type;

    let newRow = "";
    const tableId = `${type}Table`;

    if (type === "student") {
        newRow = `
            <tr class="edit-mode">
                <td><i class="fas fa-check" onclick="addItem(this)"></i></td>
                <td><input type="text" placeholder="Student ID"></td>
                <td><input type="text" placeholder="Name"></td>
                <td><input type="text" placeholder="Class"></td>
                <td><input type="date"></td>
                <td class="actions-cell"></td>
            </tr>`;
    } else if (type === "subject") {
        newRow = `
            <tr class="edit-mode">
                <td><i class="fas fa-check" onclick="addItem(this)"></i></td>
                <td><input type="text" placeholder="Subject ID"></td>
                <td><input type="text" placeholder="Name"></td>
                <td><input type="number" placeholder="Lessons"></td>
                <td class="actions-cell"></td>
            </tr>`;
    } else if (type === "score") {
        newRow = `
            <tr class="edit-mode">
                <td><i class="fas fa-check" onclick="addItem(this)"></i></td>
                <td><input type="text" placeholder="Score ID"></td>
                <td>
                    <select>
                        <option value="">Select Student</option>
                        ${students
                            .map(
                                (s) =>
                                    `<option value="${s.id}">${s.name} (ID: ${s.id})</option>`
                            )
                            .join("")}
                    </select>
                </td>
                <td>
                    <select>
                        <option value="">Select Subject</option>
                        ${subjects
                            .map(
                                (s) =>
                                    `<option value="${s.id}">${s.name} (ID: ${s.id})</option>`
                            )
                            .join("")}
                    </select>
                </td>
                <td><input type="number" step="0.1" min="0" max="10" placeholder="Score"></td>
                <td><input type="date"></td>
                <td class="actions-cell"></td>
            </tr>`;
    }

    const row = document.querySelector(`#${tableId} .add-row`);
    row.insertAdjacentHTML("beforebegin", newRow);
    row.style.display = "none";
}

async function addItem(button) {
    const row = button.closest("tr");
    const inputs = row.querySelectorAll("input, select");

    try {
        if (currentItemType === "student") {
            const [id, name, className, dob] = Array.from(inputs).map(
                (i) => i.value
            );
            await createStudent({
                id: parseInt(id),
                name,
                class: className,
                dob,
            });
        }

        await refreshTable(currentItemType);
        row.remove();
        document.querySelector(
            `#${currentItemType}Table .add-row`
        ).style.display = "";
        isAdding = false;
    } catch (error) {
        console.error("Add failed:", error);
    }
}

// Show actions menu
function showActionsMenu(button, id, type, event) {
    event.stopPropagation();

    const menu = button.nextElementSibling;
    const allMenus = document.querySelectorAll(".menu-content");
    allMenus.forEach((m) => (m.style.display = "none"));
    menu.style.display = "block";
    currentItemId = id;
    currentItemType = type;
}

async function deleteItem(type, id) {
    try {
        const confirmed = confirm(
            `Are you sure you want to delete this ${type}?`
        );
        if (!confirmed) return;

        switch (type) {
            case "student":
                await deleteStudent(id);
                break;
            case "subject":
                await deleteSubject(id);
                break;
            case "score":
                await deleteScore(id);
                break;
        }

        await refreshTable(type);
    } catch (error) {
        console.error(`Error deleting ${type}:`, error);
    }
}

// Confirm delete
function confirmDelete(confirm) {
    if (confirm) {
        if (currentItemType === "student") {
            students = students.filter((s) => s.id !== currentItemId);
            scores = scores.filter((s) => s.studentId !== currentItemId);
        } else if (currentItemType === "subject") {
            subjects = subjects.filter((s) => s.id !== currentItemId);
            scores = scores.filter((s) => s.subjectId !== currentItemId);
        } else if (currentItemType === "score") {
            scores = scores.filter((s) => s.id !== currentItemId);
        }

        refreshTable(currentItemType);
    }

    document.getElementById("deleteModal").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}

async function editItem(row, type, event) {
    event.stopPropagation();

    const cells = row.cells;
    let original = {};

    if (type === "student") {
        original = {
            id: cells[1].textContent,
            name: cells[2].textContent,
            class: cells[3].textContent,
            dob: cells[4].textContent,
        };

        cells[1].innerHTML = `<input value="${original.id}">`;
        cells[2].innerHTML = `<input value="${original.name}">`;
        cells[3].innerHTML = `<input value="${original.class}">`;
        cells[4].innerHTML = `<input type="date" value="${original.dob}">`;

        row.classList.add("edit-mode");
        currentItemType = type;

        const inputs = row.querySelectorAll("input");
        inputs.forEach((input) => {
            input.addEventListener("blur", async (e) => {
                e.stopPropagation();
                try {
                    const updates = {
                        name: inputs[1].value,
                        class_name: inputs[2].value,
                        dob: inputs[3].value,
                    };

                    await updateStudent(original.id, updates);
                    await refreshTable(type);
                } catch (error) {
                    console.error("Update failed:", error);
                    restoreOriginal(row, original, type);
                }
            });
        });
    }
}

function saveItem(row, original, type) {
    const inputs = row.querySelectorAll("input, select");

    if (type === "student") {
        const [id, name, className, dob] = Array.from(inputs).map(
            (i) => i.value
        );
        if (!id || !name || !className || !dob) {
            showWarning("All fields are required");
            restoreOriginal(row, original, type);
            return;
        }

        const student = students.find((s) => s.id == currentItemId);
        if (student) {
            student.id = parseInt(id);
            student.name = name;
            student.class = className;
            student.dob = dob;

            scores
                .filter((s) => s.studentId == currentItemId)
                .forEach((s) => {
                    s.studentId = parseInt(id);
                    s.studentName = name;
                });
        }
    } else if (type === "subject") {
        const [id, name, lessons] = Array.from(inputs).map((i) => i.value);
        if (!id || !name || !lessons) {
            showWarning("All fields are required");
            restoreOriginal(row, original, type);
            return;
        }

        const subject = subjects.find((s) => s.id == currentItemId);
        if (subject) {
            subject.id = parseInt(id);
            subject.name = name;
            subject.lessons = parseInt(lessons);

            scores
                .filter((s) => s.subjectId == currentItemId)
                .forEach((s) => {
                    s.subjectId = parseInt(id);
                    s.subjectName = name;
                });
        }
    } else if (type === "score") {
        const [id, studentSelect, subjectSelect, score, date] = Array.from(
            inputs
        ).map((i) => i.value);
        if (!id || !studentSelect || !subjectSelect || !score || !date) {
            showWarning("All fields are required");
            restoreOriginal(row, original, type);
            return;
        }

        const scoreItem = scores.find((s) => s.id == currentItemId);
        if (scoreItem) {
            const student = students.find((s) => s.id == studentSelect);
            const subject = subjects.find((s) => s.id == subjectSelect);

            scoreItem.id = parseInt(id);
            scoreItem.studentId = studentSelect;
            scoreItem.studentName = student.name;
            scoreItem.subjectId = subjectSelect;
            scoreItem.subjectName = subject.name;
            scoreItem.score = parseFloat(score);
            scoreItem.date = date;
        }
    }

    row.classList.remove("edit-mode");
    refreshTable(type);
}

// Refresh table
function refreshTable(type) {
    const tableId = `${type}Table`;
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = `
        <tr class="add-row" onclick="showAddForm('${type}')">
            <td><i class="fas fa-plus"></i></td>
            <td colspan="${
                type === "subject" ? 4 : type === "score" ? 6 : 5
            }">Click to add new ${type}</td>
        </tr>
    `;

    if (type === "student") {
        students.forEach((student) => {
            const row = `
                <tr>
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.class}</td>
                    <td>${student.dob}</td>
                    <td class="actions-cell">
                        <div class="actions-menu">
                            <div class="menu-trigger" onclick="showActionsMenu(this, ${student.id}, '${type}', event)">
                                <i class="fas fa-ellipsis-v"></i>
                            </div>
                            <div class="menu-content">
                                <button onclick="editItem(this.closest('tr'), '${type}', event)">
                                    <i class="fas fa-edit"></i> Edit
                                </button>
                                <button onclick="deleteItem()">
                                    <i class="fas fa-trash"></i> Delete
                                </button>
                            </div>
                        </div>
                    </td>
                </tr>
            `;
            tbody.insertAdjacentHTML("afterbegin", row);
        });
    } else if (type === "subject") {
        subjects.forEach((subject) => {
            const row = `
                <tr>
                    <td>${subject.id}</td>
                    <td>${subject.name}</td>
                    <td>${subject.lessons}</td>
                    <td class="actions-cell">
                        <div class="actions-menu">
                            <div class="menu-trigger" onclick="showActionsMenu(this, ${subject.id}, '${type}', event)">
                                <i class="fas fa-ellipsis-v"></i>
                            </div>
                            <div class="menu-content">
                                <button onclick="editItem(this.closest('tr'), '${type}', event)">
                                    <i class="fas fa-edit"></i> Edit
                                </button>
                                <button onclick="deleteItem()">
                                    <i class="fas fa-trash"></i> Delete
                                </button>
                            </div>
                        </div>
                    </td>
                </tr>
            `;
            tbody.insertAdjacentHTML("afterbegin", row);
        });
    } else if (type === "score") {
        scores.forEach((score) => {
            const row = `
                <tr data-student-id="${score.studentId}" data-subject-id="${score.subjectId}">
                    <td>${score.id}</td>
                    <td>${score.studentName} (ID: ${score.studentId})</td>
                    <td>${score.subjectName} (ID: ${score.subjectId})</td>
                    <td>${score.score}</td>
                    <td>${score.date}</td>
                    <td class="actions-cell">
                        <div class="actions-menu">
                            <div class="menu-trigger" onclick="showActionsMenu(this, ${score.id}, '${type}', event)">
                                <i class="fas fa-ellipsis-v"></i>
                            </div>
                            <div class="menu-content">
                                <button onclick="editItem(this.closest('tr'), '${type}', event)">
                                    <i class="fas fa-edit"></i> Edit
                                </button>
                                <button onclick="deleteItem()">
                                    <i class="fas fa-trash"></i> Delete
                                </button>
                            </div>
                        </div>
                    </td>
                </tr>
            `;
            tbody.insertAdjacentHTML("afterbegin", row);
        });
    }
}

async function filterStudents() {
    try {
        const searchTerm = document
            .getElementById("studentSearch")
            .value.toLowerCase();
        const students = await getStudents();

        const rows = document.querySelectorAll(
            "#studentTable tbody tr:not(.add-row)"
        );
        rows.forEach((row) => {
            const cells = row.cells;
            let rowText = "";

            for (let i = 1; i < cells.length - 1; i++) {
                rowText += cells[i].textContent.toLowerCase() + " ";
            }

            row.style.display = rowText.includes(searchTerm) ? "" : "none";
        });
    } catch (error) {
        console.error("Search error:", error);
    }
}

function filterSubjects() {
    const searchTerm = document
        .getElementById("subjectSearch")
        .value.toLowerCase();
    const rows = document.querySelectorAll(
        "#subjectTable tbody tr:not(.add-row)"
    );

    rows.forEach((row) => {
        const cells = row.cells;
        let rowText = "";

        for (let i = 1; i < cells.length - 1; i++) {
            rowText += cells[i].textContent.toLowerCase() + " ";
        }

        row.style.display = rowText.includes(searchTerm) ? "" : "none";
    });
}

function filterScores() {
    const searchTerm = document
        .getElementById("scoreSearch")
        .value.toLowerCase();
    const rows = document.querySelectorAll(
        "#scoreTable tbody tr:not(.add-row)"
    );

    rows.forEach((row) => {
        const cells = row.cells;
        let rowText = "";

        for (let i = 1; i < cells.length - 1; i++) {
            rowText += cells[i].textContent.toLowerCase() + " ";
        }

        row.style.display = rowText.includes(searchTerm) ? "" : "none";
    });
}

// Initial load
document.addEventListener("DOMContentLoaded", () => {
    refreshTable("student");
    refreshTable("subject");
    refreshTable("score");

    // Add event listeners for search inputs
    document
        .getElementById("studentSearch")
        .addEventListener("keyup", filterStudents);
    document
        .getElementById("subjectSearch")
        .addEventListener("keyup", filterSubjects);
    document
        .getElementById("scoreSearch")
        .addEventListener("keyup", filterScores);
});

// Utility functions
function showWarning(message) {
    const warning = document.createElement("div");
    warning.className = "confirmation-modal";
    warning.innerHTML = `
        <p class="modal-message">${message}</p>
        <div class="modal-buttons">
            <button onclick="this.parentElement.parentElement.remove()">OK</button>
        </div>
    `;
    document.body.appendChild(warning);
}

function restoreOriginal(row, original, type) {
    if (type === "student") {
        row.cells[1].textContent = original.id;
        row.cells[2].textContent = original.name;
        row.cells[3].textContent = original.class;
        row.cells[4].textContent = original.dob;
    } else if (type === "subject") {
        row.cells[1].textContent = original.id;
        row.cells[2].textContent = original.name;
        row.cells[3].textContent = original.lessons;
    } else if (type === "score") {
        const student = students.find((s) => s.id == original.studentId);
        const subject = subjects.find((s) => s.id == original.subjectId);

        row.cells[1].textContent = original.id;
        row.cells[2].textContent = `${student.name} (ID: ${student.id})`;
        row.cells[3].textContent = `${subject.name} (ID: ${subject.id})`;
        row.cells[4].textContent = original.score;
        row.cells[5].textContent = original.date;
    }

    row.classList.remove("edit-mode");
}

function showLoading(show) {
    let loader = document.getElementById("global-loader");
    if (!loader && show) {
        loader = document.createElement("div");
        loader.id = "global-loader";
        loader.className = "loading";
        loader.innerHTML = '<div class="spinner">Loading...</div>';
        document.body.appendChild(loader);
    } else if (loader && !show) {
        loader.remove();
    }
}
