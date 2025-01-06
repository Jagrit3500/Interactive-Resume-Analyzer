const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const fileNameDisplay = document.getElementById("file-name");
const jobDescriptionInput = document.getElementById("jobDescription");
const analyzeBtn = document.getElementById("analyzeBtn");
const loadingIndicator = document.getElementById("loading");
const resultSection = document.getElementById("result");
const matchScoreElement = document.getElementById("matchScore");
const suggestionsList = document.getElementById("suggestionsList");

dropzone.addEventListener("click", () => {
  fileInput.click();
});

dropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropzone.style.backgroundColor = "#f1f1f1";
});

dropzone.addEventListener("dragleave", () => {
  dropzone.style.backgroundColor = "white";
});

dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  const file = event.dataTransfer.files[0];
  handleFileUpload(file);
});

fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  handleFileUpload(file);
});

function handleFileUpload(file) {
  if (file) {
    fileNameDisplay.textContent = `Selected file: ${file.name}`;
  }
}

async function analyzeResume() {
  const resumeFile = fileInput.files[0];
  const jobDescription = jobDescriptionInput.value.trim();

  if (!resumeFile || !jobDescription) {
    alert("Please upload a resume and enter a job description.");
    return;
  }

  loadingIndicator.style.display = "block";
  resultSection.style.display = "none";

  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("jobDescription", jobDescription);

  try {
    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (response.ok) {
      matchScoreElement.textContent = `Match Score: ${data.matchScore}%`;
      suggestionsList.innerHTML = "";
      data.suggestions.forEach(suggestion => {
        const li = document.createElement("li");
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
      });

      resultSection.style.display = "block";
    } else {
      alert("Error analyzing the resume. Please try again.");
    }
  } catch (error) {
    console.error("Error during analysis:", error);
    alert("An error occurred. Please try again.");
  } finally {
    loadingIndicator.style.display = "none";
  }
}
