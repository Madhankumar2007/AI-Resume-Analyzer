const resumeInput = document.getElementById("resume");
const jobDescription = document.getElementById("jobDescription");
const analyzeBtn = document.getElementById("analyzeBtn");
const output = document.getElementById("output");

analyzeBtn.addEventListener("click", async function () {

    const resume = resumeInput.files[0];
    const job = jobDescription.value.trim();

    if (!resume) {
        alert("Please upload your resume!");
        return;
    }

    if (resume.type !== "application/pdf") {
        alert("Please upload a PDF file!");
        return;
    }

    if (resume.size > 5 * 1024 * 1024) {
        alert("Maximum file size is 5 MB!");
        return;
    }

    if (!job) {
        alert("Please enter the job description!");
        return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", job);

    output.innerText = "Analyzing your resume using AI and ATS...";
    analyzeBtn.disabled = true;

    try {

        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Resume processing failed");
        }

        displayResults(result);

    } catch (error) {

        output.innerText = error.message;

    } finally {

        analyzeBtn.disabled = false;

    }

});


function displayResults(result) {

    const match = result.match_result || {};
    const ats = result.ats_analysis || {};

    const percentage = Number(match.match_percentage) || 0;
    const semanticScore = Number(result.semantic_similarity) || 0;
    const atsScore = Number(ats.completeness_score) || 0;

    const matchedSkills = match.matched_skills || [];
    const missingSkills = match.missing_skills || [];
    const resumeSkills = result.skills || {};
    const recommendations = result.recommendations || [];

    const detectedSections = ats.detected_sections || [];
    const missingSections = ats.missing_sections || [];
    const matchedKeywords = ats.matched_keywords || [];
    const missingKeywords = ats.missing_keywords || [];
    const atsSuggestions = ats.suggestions || [];

    const matchedHTML = matchedSkills.map(skill =>
        `<span class="skill-tag matched">${escapeHTML(skill)}</span>`
    ).join("");

    const missingHTML = missingSkills.map(skill =>
        `<span class="skill-tag missing">${escapeHTML(skill)}</span>`
    ).join("");

    let resumeSkillsHTML = "";

    for (const category in resumeSkills) {

        const skills = resumeSkills[category]
            .map(skill => escapeHTML(skill))
            .join(", ");

        resumeSkillsHTML += `
            <h4>${escapeHTML(category)}</h4>
            <p>${skills}</p>
        `;
    }

    const recommendationHTML = recommendations.length
        ? recommendations.map(item => `
            <div class="recommendation-card">
                <h3>${escapeHTML(item.skill)}</h3>
                <p>${escapeHTML(item.description)}</p>
                <p><strong>Difficulty:</strong> ${escapeHTML(item.level)}</p>
                <h4>Recommended Topics</h4>
                <div class="skill-tags">
                    ${(item.topics || []).map(topic =>
                        `<span class="skill-tag">${escapeHTML(topic)}</span>`
                    ).join("")}
                </div>
            </div>
        `).join("")
        : "<p>No skill recommendations available.</p>";

    const detectedHTML = detectedSections.length
        ? detectedSections.map(section =>
            `<span class="skill-tag matched">${escapeHTML(section)}</span>`
        ).join("")
        : "<p>No sections detected.</p>";

    const missingSectionsHTML = missingSections.length
        ? missingSections.map(section =>
            `<span class="skill-tag missing">${escapeHTML(section)}</span>`
        ).join("")
        : "<p>No missing sections detected.</p>";

    const matchedKeywordsHTML = matchedKeywords.length
        ? matchedKeywords.map(keyword =>
            `<span class="skill-tag matched">${escapeHTML(keyword)}</span>`
        ).join("")
        : "<p>No matching keywords detected.</p>";

    const missingKeywordsHTML = missingKeywords.length
        ? missingKeywords.map(keyword =>
            `<span class="skill-tag missing">${escapeHTML(keyword)}</span>`
        ).join("")
        : "<p>No missing keywords detected.</p>";

    const atsSuggestionsHTML = atsSuggestions.length
        ? atsSuggestions.map(suggestion =>
            `<li>${escapeHTML(suggestion)}</li>`
        ).join("")
        : "<li>No additional suggestions available.</li>";

    output.innerHTML = `

        <div class="result-card">

            <h2>Resume Analysis Dashboard</h2>

            <!-- Keyword Match -->

            <div class="score-section">

                <div class="progress-circle"
                     style="--progress: ${percentage}%">

                    <div class="progress-inner">
                        <h2>${percentage}%</h2>
                        <span>Keyword Match</span>
                    </div>

                </div>

                <h3>Resume Skill Compatibility</h3>

            </div>

            <!-- Semantic Similarity -->

            <div class="semantic-score-card">

                <h3>AI Semantic Similarity</h3>

                <div class="semantic-score">
                    ${semanticScore.toFixed(2)}%
                </div>

                <p>
                    Sentence-BERT compares the overall meaning
                    of your resume and the job description.
                </p>

            </div>

            <!-- ATS Analysis -->

            <div class="ats-card">

                <h2>ATS Resume Analysis</h2>

                <div class="ats-score">
                    ${atsScore.toFixed(2)}%
                </div>

                <p>Resume Section Completeness</p>

                <div class="ats-progress">
                    <div class="ats-progress-fill"
                         style="width: ${Math.min(100, Math.max(0, atsScore))}%">
                    </div>
                </div>

                <div class="ats-section">

                    <h3>Detected Resume Sections</h3>

                    <div class="skill-tags">
                        ${detectedHTML}
                    </div>

                </div>

                <div class="ats-section">

                    <h3>Missing Resume Sections</h3>

                    <div class="skill-tags">
                        ${missingSectionsHTML}
                    </div>

                </div>

                <div class="ats-section">

                    <h3>Matched Job Keywords</h3>

                    <div class="skill-tags">
                        ${matchedKeywordsHTML}
                    </div>

                </div>

                <div class="ats-section">

                    <h3>Missing Job Keywords</h3>

                    <div class="skill-tags">
                        ${missingKeywordsHTML}
                    </div>

                </div>

                <div class="ats-section">

                    <h3>ATS Improvement Suggestions</h3>

                    <ul>
                        ${atsSuggestionsHTML}
                    </ul>

                </div>

            </div>

            <!-- Statistics -->

            <div class="dashboard-stats">

                <div class="stat-box">
                    <h3>${Number(result.total_skills) || 0}</h3>
                    <p>Total Resume Skills</p>
                </div>

                <div class="stat-box">
                    <h3>${matchedSkills.length}</h3>
                    <p>Matched Skills</p>
                </div>

                <div class="stat-box">
                    <h3>${missingSkills.length}</h3>
                    <p>Missing Skills</p>
                </div>

            </div>

            <!-- Matched Skills -->

            <div class="skill-section">

                <h3>Matched Skills</h3>

                <div class="skill-tags">
                    ${matchedHTML || "No matched skills found."}
                </div>

            </div>

            <!-- Missing Skills -->

            <div class="skill-section">

                <h3>Missing Skills</h3>

                <div class="skill-tags">
                    ${missingHTML || "No missing skills found."}
                </div>

            </div>

            <!-- Recommendations -->

            <div class="skill-section">

                <h2>Resume Improvement Recommendations</h2>

                ${recommendationHTML}

            </div>

            <!-- Resume Skills -->

            <div class="resume-skills">

                <h3>Skills Found in Your Resume</h3>

                ${resumeSkillsHTML || "<p>No skills detected.</p>"}

            </div>

            <!-- Extracted Text -->

            <div class="resume-skills">

                <h3>Extracted Resume Text</h3>

                <pre style="white-space: pre-wrap; overflow-wrap: anywhere;">${escapeHTML(result.extracted_text || "")}</pre>

            </div>

            <!-- Download Report -->

            <button id="downloadReportBtn">
                Download PDF Report
            </button>

        </div>

    `;

    document.getElementById("downloadReportBtn")
        .addEventListener("click", downloadReport);

}


async function downloadReport() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/download-report"
        );

        if (!response.ok) {
            throw new Error("Unable to download PDF report");
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;
        link.download = "Resume_Analysis_Report.pdf";

        document.body.appendChild(link);
        link.click();
        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {

        alert(error.message);

    }

}


function escapeHTML(text) {

    const element = document.createElement("div");

    element.textContent = String(text);

    return element.innerHTML;

}