let currentItemType = null;
let isAdding = false;

const API_BASE = "http://localhost:8000/api";
const SUBROUTES = {
    student: "students",
    subject: "subjects",
    score: "scores",
};

async function fetchAPI(endpoint, method = "GET", data = null) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method,
            headers: { "Content-Type": "application/json" },
            body: data ? JSON.stringify(data) : null,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(
                `HTTP error! status: ${response.status} - ${errorText}`
            );
        }

        return await response.json();
    } catch (error) {
        console.error("API error:", error);
        throw error;
    }
}

const studentAPI = {
    getAll: () => fetchAPI(`/${SUBROUTES.student}/list`),
    create: (student) => fetchAPI(`/${SUBROUTES.student}/add`, "POST", student),
    update: (updates) =>
        fetchAPI(`/${SUBROUTES.student}/update`, "PUT", updates),
    delete: (id) => fetchAPI(`/${SUBROUTES.student}/remove/${id}`, "DELETE"),
};

async function refreshTable(type) {
    let data = [];
    const tableBody = document.querySelector(`#${type}Table tbody`);
    tableBody.innerHTML = "";

    switch (type) {
        case "student":
            students = await studentAPI.getAll();
            data = students;
            break;
        case "subject":
            subjects = await fetchAPI(`/${SUBROUTES.subject}/list`);
            data = subjects;
            break;
        case "score":
            scores = await fetchAPI(`/${SUBROUTES.score}/list`);
            data = scores;
            break;
    }

    data.forEach((item) => {
        const row = createTableRow(item, type);
        tableBody.appendChild(row);
    });

    const addRow = document.createElement("tr");
    addRow.className = "add-row";
    addRow.innerHTML = `<td colspan="100%"><button onclick="showAddForm('${type}')">+ Add ${type}</button></td>`;
    tableBody.appendChild(addRow);
}

function createTableRow(item, type) {
    const row = document.createElement("tr");
    row.setAttribute("data-id", item.id);
    let content = "";

    switch (type) {
        case "student":
            content = `
                <td>${item.student_id}</td>
                <td>${item.name}</td>
                <td>${item.class_}</td>
                <td>${item.birthdate}</td>`;
            break;
        case "subject":
            content = `
                <td>${item.subject_id}</td>
                <td>${item.name}</td>
                <td>${item.lessons}</td>`;
            break;
        case "score":
            const student = student.find((s) => s.id === item.studentId);
            const subject = subject.find((s) => s.id === item.subjectId);
            content = `
                <td>${item.score_id}</td>
                <td>${student ? student.name : "Unknown"}</td>
                <td>${subject ? subject.name : "Unknown"}</td>
                <td>${item.score}</td>
                <td>${item.date}</td>`;
            break;
    }

    content += `
    <td class="actions-cell">
        <button class="icon-button" aria-label="Actions" onclick="showActionsMenu(this, ${item.id}, '${type}', event)">
            <svg class="kebab-icon" viewBox="0 0 24 24" width="20" height="20">
                <circle cx="12" cy="6" r="1.5"/>
                <circle cx="12" cy="12" r="1.5"/>
                <circle cx="12" cy="18" r="1.5"/>
            </svg>
        </button>
        <div class="menu-content">
            <button onclick="editItem(${item.id}, '${type}')">Edit</button>
            <button onclick="deleteItem(${item.id}, '${type}')">Delete</button>
        </div>
    </td>`;

    row.innerHTML = content;
    return row;
}

function showAddForm(type) {
    if (isAdding) return;
    isAdding = true;
    currentItemType = type;

    const row = document.querySelector(`#${type}Table .add-row`);
    row.insertAdjacentHTML("beforebegin", getAddRowHTML(type));
    row.style.display = "none";
}

function getAddRowHTML(type) {
    const inputs = {
        student: `
            <td><input type="text" placeholder="Student ID"></td>
            <td><input type="text" placeholder="Name"></td>
            <td><input type="text" placeholder="Class"></td>
            <td><input type="date"></td>`,
        subject: `
            <td><input type="text" placeholder="Subject ID"></td>
            <td><input type="text" placeholder="Name"></td>
            <td><input type="number" placeholder="Lessons"></td>`,
        score: `
            <td><input type="text" placeholder="Score ID"></td>
            <td>${generateStudentSelect()}</td>
            <td>${generateSubjectSelect()}</td>
            <td><input type="number" step="0.1" min="0" max="10" placeholder="Score"></td>
            <td><input type="date"></td>`,
    };

    return `<tr class="edit-mode">${inputs[type]}<td class="actions-cell"><i class="fas fa-check" onclick="addItem(this)"></i></td></tr>`;
}

function generateStudentSelect() {
    return `<select><option value="">Select Student</option>${students
        .map((s) => `<option value="${s.id}">${s.name} (ID: ${s.id})</option>`)
        .join("")}</select>`;
}

function generateSubjectSelect() {
    return `<select><option value="">Select Subject</option>${subjects
        .map((s) => `<option value="${s.id}">${s.name} (ID: ${s.id})</option>`)
        .join("")}</select>`;
}

async function addItem(button) {
    const row = button.closest("tr");
    const inputs = row.querySelectorAll("input, select");

    try {
        if (currentItemType === "student") {
            const [id, name, className, dob] = Array.from(inputs).map(
                (i) => i.value
            );
            await studentAPI.create({
                student_id: parseInt(id),
                name,
                class_: className,
                birthdate: dob,
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
        showWarning(
            `Failed to add ${currentItemType}: ${error.message}`,
            "error"
        );
    }
}

function showActionsMenu(button, id, type, event) {
    event.stopPropagation();

    document.querySelectorAll(".actions-cell.active").forEach((cell) => {
        if (cell !== button.closest(".actions-cell")) {
            cell.classList.remove("active");
        }
    });

    const cell = button.closest(".actions-cell");
    cell.classList.toggle("active");

    const clickOutsideHandler = (e) => {
        if (!cell.contains(e.target)) {
            cell.classList.remove("active");
            document.removeEventListener("click", clickOutsideHandler);
        }
    };

    document.addEventListener("click", clickOutsideHandler);
}

async function deleteItem(id, type) {
    console.log(id, type);

    try {
        if (currentItemType === "student") {
            console.log(id);
            await studentAPI.delete(id);
        } else if (currentItemType === "subject") {
            await fetchAPI(
                `/${SUBROUTES.subject}/remove`,
                {
                    id: id,
                },
                "DELETE"
            );
        } else if (currentItemType === "score") {
            await fetchAPI(
                `/${SUBROUTES.score}/remove`,
                {
                    id: id,
                },
                "DELETE"
            );
        }

        await refreshTable(currentItemType);
        showWarning(`${currentItemType} deleted successfully`, "success");
    } catch (error) {
        console.error("Delete failed:", error);
        showWarning(
            `Failed to delete ${currentItemType}: ${error.message}`,
            "error"
        );
        return;
    }
}

function showWarning(message, type = "warning", duration = 5000) {
    const container = document.getElementById("notification-container");
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;

    notification.innerHTML = `
        <span>${message}</span>
        <button class="notification-close" aria-label="Close">&times;</button>
    `;

    container.appendChild(notification);

    let timeoutId = setTimeout(() => {
        removeNotification(notification);
    }, duration);

    notification
        .querySelector(".notification-close")
        .addEventListener("click", () => {
            clearTimeout(timeoutId);
            removeNotification(notification);
        });

    function removeNotification(element) {
        element.style.animation = "slideIn 0.3s ease-out reverse forwards";
        setTimeout(() => {
            element.remove();
        }, 300);
    }
}

function editItem(id, type) {
    if (isAdding) return;
    currentItemId = id;
    currentItemType = type;

    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (!row) {
        showWarning("Could not find item to edit", "error");
        return;
    }

    const originalContent = row.innerHTML;
    row.classList.add("edit-mode");

    let editForm = "";
    if (type === "student") {
        const student = students.find((s) => s.id === id);
        if (!student) {
            showWarning("Student data not found", "error");
            return;
        }

        editForm = `
            <td><input type="text" value="${
                student.student_id
            }" placeholder="Student ID"></td>
            <td><input type="text" value="${
                student.name
            }" placeholder="Name"></td>
            <td><input type="text" value="${
                student.class_
            }" placeholder="Class"></td>
            <td><input type="date" value="${student.birthdate}"></td>
            <td class="actions-cell">
                <button class="save-btn" onclick="saveItem(${id}, '${type}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M20 6L9 17l-5-5"/>
                    </svg>
                </button>
                <button class="cancel-btn" onclick="cancelEdit(this, '${originalContent.replace(
                    /'/g,
                    "\\'"
                )}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                </button>
            </td>
        `;
    } else if (type === "subject") {
        const subject = subjects.find((s) => s.id === id);
        if (!subject) {
            showWarning("Subject data not found", "error");
            return;
        }

        editForm = `
            <td><input type="text" value="${
                subject.subject_id
            }" placeholder="Subject ID"></td>
            <td><input type="text" value="${
                subject.name
            }" placeholder="Name"></td>
            <td><input type="number" value="${
                subject.lessons
            }" placeholder="Lessons"></td>
            <td class="actions-cell">
                <button class="save-btn" onclick="saveItem(${id}, '${type}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M20 6L9 17l-5-5"/>
                    </svg>
                </button>
                <button class="cancel-btn" onclick="cancelEdit(this, '${originalContent.replace(
                    /'/g,
                    "\\'"
                )}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                </button>
            </td>
        `;
    } else if (type === "score") {
        const score = scores.find((s) => s.id === id);
        if (!score) {
            showWarning("Score data not found", "error");
            return;
        }

        const studentOptions = students
            .map(
                (s) =>
                    `<option value="${s.id}" ${
                        s.id === score.studentId ? "selected" : ""
                    }>${s.name}</option>`
            )
            .join("");

        const subjectOptions = subjects
            .map(
                (s) =>
                    `<option value="${s.id}" ${
                        s.id === score.subjectId ? "selected" : ""
                    }>${s.name}</option>`
            )
            .join("");

        editForm = `
            <td><input type="text" value="${
                score.score_id
            }" placeholder="Score ID"></td>
            <td>
                <select class="student-select">
                    <option value="">Select Student</option>
                    ${studentOptions}
                </select>
            </td>
            <td>
                <select class="subject-select">
                    <option value="">Select Subject</option>
                    ${subjectOptions}
                </select>
            </td>
            <td><input type="number" step="0.1" min="0" max="10" value="${
                score.score
            }" placeholder="Score"></td>
            <td><input type="date" value="${score.date}"></td>
            <td class="actions-cell">
                <button class="save-btn" onclick="saveItem(${id}, '${type}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M20 6L9 17l-5-5"/>
                    </svg>
                </button>
                <button class="cancel-btn" onclick="cancelEdit(this, '${originalContent.replace(
                    /'/g,
                    "\\'"
                )}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                </button>
            </td>
        `;
    }

    row.innerHTML = editForm;
}

async function saveItem(id, type) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (!row) {
        showWarning("Could not find item to save", "error");
        return;
    }

    try {
        if (type === "student") {
            const inputs = row.querySelectorAll("input");
            const [student_id, name, class_, birthdate] = Array.from(
                inputs
            ).map((i) => i.value);

            await studentAPI.update({
                id: id,
                student_id: parseInt(student_id),
                name,
                class_,
                birthdate,
            });
        } else if (type === "subject") {
            const inputs = row.querySelectorAll("input");
            const [subject_id, name, lessons] = Array.from(inputs).map(
                (i) => i.value
            );

            await fetchAPI(`/${SUBROUTES.subject}/update`, "PUT", {
                id: id,
                subject_id: subject_id,
                name,
                lessons: parseInt(lessons),
            });
        } else if (type === "score") {
            const inputs = row.querySelectorAll("input, select");
            const [score_id, studentId, subjectId, score, date] = Array.from(
                inputs
            ).map((i) => i.value);

            await fetchAPI(`/${SUBROUTES.score}/update`, "PUT", {
                id: id,
                score_id: score_id,
                studentId: parseInt(studentId),
                subjectId: parseInt(subjectId),
                score: parseFloat(score),
                date,
            });
        }

        await refreshTable(type);
        showWarning(`${type} updated successfully`, "success");
    } catch (error) {
        console.error("Update failed:", error);
        showWarning(`Failed to update ${type}: ${error.message}`, "error");
    }
}

function cancelEdit(button, originalContent) {
    if (!button) return;

    const row = button.closest("tr");
    if (!row) return;

    try {
        row.innerHTML = originalContent;
        row.classList.remove("edit-mode");
    } catch (error) {
        console.error("Error canceling edit:", error);
        showWarning("Failed to cancel edit", "error");
    }
}

function filterTable(inputId, tableSelector) {
    const searchTerm = document.getElementById(inputId).value.toLowerCase();
    const rows = document.querySelectorAll(`${tableSelector} tr:not(.add-row)`);

    rows.forEach((row) => {
        const cells = Array.from(row.cells).slice(1, -1);
        const rowText = cells
            .map((cell) => cell.textContent.toLowerCase())
            .join(" ");
        row.style.display = rowText.includes(searchTerm) ? "" : "none";
    });
}

function filterStudents() {
    filterTable("studentSearch", "#studentTable tbody");
}

function filterSubjects() {
    filterTable("subjectSearch", "#subjectTable tbody");
}

function filterScores() {
    filterTable("scoreSearch", "#scoreTable tbody");
}

function switchTab(tabName) {
    document.querySelectorAll(".tab-content").forEach((tab) => {
        tab.classList.remove("active");
    });
    document.querySelectorAll(".tab").forEach((tab) => {
        tab.classList.remove("active");
    });

    document.getElementById(`${tabName}-tab`).classList.add("active");
    document
        .querySelector(`.tab[onclick="switchTab('${tabName}')"]`)
        .classList.add("active");

    refreshTable(tabName);
}

document.addEventListener("DOMContentLoaded", async () => {
    try {
        await Promise.all([
            refreshTable("student"),
            refreshTable("subject"),
            refreshTable("score"),
        ]);

        ["student", "subject", "score"].forEach((type) => {
            document
                .getElementById(`${type}Search`)
                .addEventListener("keyup", () => {
                    if (type === "student") filterStudents();
                    if (type === "subject") filterSubjects();
                    if (type === "score") filterScores();
                });
        });
    } catch (error) {
        console.error("Initialization error:", error);
        showWarning("Failed to load initial data");
    }
});
