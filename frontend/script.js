let currentItemId = null;
let currentItemType = null;
let isAdding = false;

const API_BASE = "http://localhost:8000/api";
const SUBROUTES = {
  student: 'students',
  subject: 'subjects',
  score: 'scores'
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
      throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}

// API helpers
const studentAPI = {
  getAll: () => fetchAPI(`/${SUBROUTES.student}/list`),
  create: (student) => fetchAPI(`/${SUBROUTES.student}/add`, "POST", student),
  update: (id, updates) => fetchAPI(`/${SUBROUTES.student}/${id}`, "PUT", updates),
  delete: (id) => fetchAPI(`/${SUBROUTES.student}/${id}`, "DELETE"),
};

// Event setup

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await Promise.all(["student", "subject", "score"].map(refreshTable));

    document.getElementById("studentSearch").addEventListener("keyup", filterStudents);
    document.getElementById("subjectSearch").addEventListener("keyup", filterSubjects);
    document.getElementById("scoreSearch").addEventListener("keyup", filterScores);
  } catch (error) {
    console.error("Initialization error:", error);
    showWarning("Failed to load initial data");
  }
});

function switchTab(tabName) {
  document.querySelectorAll(".tab, .tab-content").forEach(el => el.classList.remove("active"));
  document.querySelector(`.tab[onclick="switchTab('${tabName}')"]`).classList.add("active");
  document.getElementById(`${tabName}-tab`).classList.add("active");
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
  const baseRow = `
    <tr class="edit-mode">
      <td><i class="fas fa-check" onclick="addItem(this)"></i></td>
  `;

  switch (type) {
    case "student":
      return `${baseRow}
        <td><input type="text" placeholder="Student ID"></td>
        <td><input type="text" placeholder="Name"></td>
        <td><input type="text" placeholder="Class"></td>
        <td><input type="date"></td>
        <td class="actions-cell"></td>
      </tr>`;
    case "subject":
      return `${baseRow}
        <td><input type="text" placeholder="Subject ID"></td>
        <td><input type="text" placeholder="Name"></td>
        <td><input type="number" placeholder="Lessons"></td>
        <td class="actions-cell"></td>
      </tr>`;
    case "score":
      return `${baseRow}
        <td><input type="text" placeholder="Score ID"></td>
        <td>${generateStudentSelect()}</td>
        <td>${generateSubjectSelect()}</td>
        <td><input type="number" step="0.1" min="0" max="10" placeholder="Score"></td>
        <td><input type="date"></td>
        <td class="actions-cell"></td>
      </tr>`;
  }
}

function generateStudentSelect() {
  return `<select><option value="">Select Student</option>${students.map(s => `<option value="${s.id}">${s.name} (ID: ${s.id})</option>`).join("")}</select>`;
}

function generateSubjectSelect() {
  return `<select><option value="">Select Subject</option>${subjects.map(s => `<option value="${s.id}">${s.name} (ID: ${s.id})</option>`).join("")}</select>`;
}

async function addItem(button) {
  const row = button.closest("tr");
  const inputs = row.querySelectorAll("input, select");

  try {
    if (currentItemType === "student") {
      const [id, name, className, dob] = Array.from(inputs).map(i => i.value);
      await studentAPI.create({ student_id: parseInt(id), name, class_: className, birthdate: dob });
    }

    await refreshTable(currentItemType);
    row.remove();
    document.querySelector(`#${currentItemType}Table .add-row`).style.display = "";
    isAdding = false;
  } catch (error) {
    console.error("Add failed:", error);
  }
}

function showActionsMenu(button, id, type, event) {
  event.stopPropagation();
  document.querySelectorAll(".menu-content").forEach(m => m.style.display = "none");
  button.nextElementSibling.style.display = "block";
  currentItemId = id;
  currentItemType = type;
}

function confirmDelete(confirm) {
  if (confirm) {
    if (currentItemType === "student") {
      students = students.filter(s => s.id !== currentItemId);
      scores = scores.filter(s => s.studentId !== currentItemId);
    } else if (currentItemType === "subject") {
      subjects = subjects.filter(s => s.id !== currentItemId);
      scores = scores.filter(s => s.subjectId !== currentItemId);
    } else if (currentItemType === "score") {
      scores = scores.filter(s => s.id !== currentItemId);
    }
    refreshTable(currentItemType);
  }
  document.getElementById("deleteModal").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

function filterTableRows(inputId, tableSelector) {
  const searchTerm = document.getElementById(inputId).value.toLowerCase();
  document.querySelectorAll(`${tableSelector} tbody tr:not(.add-row)`).forEach(row => {
    const rowText = Array.from(row.cells).slice(1, -1).map(c => c.textContent.toLowerCase()).join(" ");
    row.style.display = rowText.includes(searchTerm) ? "" : "none";
  });
}

function filterStudents() { filterTableRows("studentSearch", "#studentTable"); }
function filterSubjects() { filterTableRows("subjectSearch", "#subjectTable"); }
function filterScores() { filterTableRows("scoreSearch", "#scoreTable"); }

// TODO: complete similar cleanup for editItem, saveItem, deleteItem, refreshTable...
function filterTable(searchInputId, tableBodySelector) {
    const searchTerm = document.getElementById(searchInputId).value.toLowerCase();
    const rows = document.querySelectorAll(`${tableBodySelector} tr:not(.add-row)`);

    rows.forEach((row) => {
        const cells = Array.from(row.cells).slice(1, -1);
        const rowText = cells.map(cell => cell.textContent.toLowerCase()).join(" ");
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
                    switch (type) {
                        case "student":
                            filterStudents();
                            break;
                        case "subject":
                            filterSubjects();
                            break;
                        case "score":
                            filterScores();
                            break;
                    }
                });
        });

    } catch (error) {
        console.error("Initialization error:", error);
        showWarning("Failed to load initial data");
    }
});
