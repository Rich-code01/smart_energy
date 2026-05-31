// ---------------- DAILY ----------------
fetch("/api/daily")
    .then(r => r.json())
    .then(d => {

        document.getElementById("kpi").innerHTML =
            `Today: ${d.today} | Yesterday: ${d.yesterday}`;

        new Chart(document.getElementById("dailyChart"), {
            type: "bar",
            data: {
                labels: ["Today", "Yesterday"],
                datasets: [{ data: [d.today, d.yesterday] }]
            }
        });
    });


// ---------------- WEEKLY ----------------
fetch("/api/weekly")
    .then(r => r.json())
    .then(data => {

        new Chart(document.getElementById("weeklyChart"), {
            type: "line",
            data: {
                labels: data.map(x => x[0]),
                datasets: [{ data: data.map(x => x[1]) }]
            }
        });
    });


// ---------------- REGION ----------------
fetch("/api/region")
    .then(r => r.json())
    .then(data => {

        new Chart(document.getElementById("regionChart"), {
            type: "pie",
            data: {
                labels: data.map(x => "R" + x[0]),
                datasets: [{ data: data.map(x => x[1]) }]
            }
        });
    });


// ---------------- REAL TIME ----------------
function loadRealtime() {
    fetch("/api/realtime")
        .then(r => r.json())
        .then(data => {

            let html = "<table><tr><th>Meter</th><th>Power</th><th>Energy</th></tr>";

            data.forEach(r => {
                html += `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`;
            });

            html += "</table>";

            document.getElementById("realtime").innerHTML = html;
        });
}

loadRealtime();
setInterval(loadRealtime, 5000);


// ---------------- PERFORMANCE ----------------
fetch("/api/performance")
    .then(r => r.json())
    .then(d => {

        new Chart(document.getElementById("perfChart"), {
            type: "bar",
            data: {
                labels: ["Raw", "3H", "Day", "Week"],
                datasets: [{
                    data: [
                        d.query.raw,
                        d.query["3h"],
                        d.query.day,
                        d.query.week
                    ]
                }]
            }
        });
    });