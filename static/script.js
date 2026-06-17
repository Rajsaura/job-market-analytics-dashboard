console.log("NEW SCRIPT LOADED");

let rolesChart = null;

// =======================
// TREND CHART
// =======================

async function loadData() {

    const response = await fetch("/api/trends");
    const json = await response.json();

    const labels = json.data.map(item => item.week);

    const datasets = json.skills.map(skill => ({
        label: skill,
        data: json.data.map(item => item[skill]),
        tension: 0.3
    }));

    const ctx = document.getElementById("trendChart");

    new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

}

// =======================
// OVERVIEW
// =======================

async function loadOverview() {

    const response = await fetch("/api/overview");
    const data = await response.json();

    document.getElementById("totalJobs").textContent =
        data.total_jobs.toLocaleString();

    document.getElementById("dataFrom").textContent =
        data.data_from;

    document.getElementById("datato").textContent =
        data.data_to;

}

// =======================
// GROWTH BADGE
// =======================

function getGrowth(skill) {

    const growth = {

        pyspark:"+16.42%",
        python:"+12.1%",
        numpy:"+9.19%",
        sql:"+8.81%",
        powerbi:"+4.43%",
        azure:"+3.01%",
        aws:"+2.75%",
        gcp:"-5.67%",
        pytorch:"-5.84%",
        restapi:"-7.93%"

    };

    return growth[skill] || "";

}

// =======================
// MOMENTUM PANEL
// =======================

async function loadMomentum() {

    const response = await fetch("/api/momentum");
    const data = await response.json();

    const container = document.getElementById("momentum");

    container.innerHTML = "";

    data.forEach(skill => {

        const row = document.createElement("div");

        row.className = "skill-row";

        row.innerHTML = `
            <span>${skill.skill}</span>

            <span class="${skill.growth >= 0 ? "positive" : "negative"}">

                ${skill.growth >= 0 ? "+" : ""}${skill.growth}%

            </span>
        `;

        row.onclick = () => {

            document
                .querySelectorAll(".skill-row")
                .forEach(r => r.classList.remove("selected-skill"));

            row.classList.add("selected-skill");

            loadSkill(skill.skill);

        };

        container.appendChild(row);

    });

}

// =======================
// SKILL DETAILS
// =======================

async function loadSkill(skillName) {

    const response = await fetch(`/api/skill/${skillName}`);
    const data = await response.json();

    document.getElementById("skillInsight").innerHTML = `

        <h2 class="skill-title">

            ${data.skill}

            <span class="growth-pill">

                ${getGrowth(skillName)}

            </span>

        </h2>

        <div class="hero-card">

            <div class="hero-number">

                ${data.total_jobs.toLocaleString()}

            </div>

            <div class="hero-text">

                Jobs This Week

            </div>

            <div class="hero-subtitle">

                Updated from latest market trends

            </div>

        </div>

        <h3>Top Roles</h3>

        <div class="chart-container">

            <canvas id="rolesChart"></canvas>

        </div>

        <h3>Top Skill Combinations</h3>

        <table class="insight-table">

            <thead>

                <tr>

                    <th>Skill</th>

                    <th>Count</th>

                </tr>

            </thead>

            <tbody>

                ${data.paired_skills.map(skill => `

                    <tr>

                        <td>${skill.skill}</td>

                        <td>${skill.count.toLocaleString()}</td>

                    </tr>

                `).join("")}

            </tbody>

        </table>

    `;

    // ======================
    // TOP ROLES CHART
    // ======================

    const topRoles = data.top_roles.slice(0,5);

    const labels = topRoles.map(role => role.role);

    const values = topRoles.map(role => role.count);

    const ctx = document.getElementById("rolesChart");

    if (rolesChart) {

        rolesChart.destroy();

    }

    rolesChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels,

            datasets: [

                {

                    data: values,

                    backgroundColor: "#4f8df7",

                    borderRadius: 10,

                    maxBarThickness: 45

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                x: {

                    ticks: {

                        color: "#d4def0"

                    },

                    grid: {

                        display: false

                    }

                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        color: "#9fb3d4"

                    },

                    grid: {

                        color: "rgba(255,255,255,.05)"

                    }

                }

            }

        }

    });

}

// =======================
// START
// =======================

loadMomentum();
loadOverview();
loadData();