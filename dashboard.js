async function getJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function loadData() {
  const [stats, incidents] = await Promise.all([
    getJSON("/api/stats"),
    getJSON("/api/incidents?limit=50")
  ]);

  document.getElementById("events").textContent = stats.events;
  document.getElementById("incidents").textContent = stats.incidents;
  document.getElementById("open").textContent = stats.open_incidents;
  document.getElementById("danger").textContent =
    (stats.severity.HIGH || 0) + (stats.severity.CRITICAL || 0);

  document.getElementById("severity").textContent =
    JSON.stringify(stats.severity, null, 2);
  document.getElementById("detections").textContent =
    JSON.stringify(stats.detections, null, 2);

  const tbody = document.getElementById("incidentsTable");
  tbody.innerHTML = incidents.map(i => `
    <tr>
      <td>${i.id}</td>
      <td>${i.severity}</td>
      <td>${i.rule_id}</td>
      <td>${i.mitre_technique || "-"}</td>
      <td>${i.risk_score}</td>
      <td>${i.status}</td>
      <td>${new Date(i.created_at).toLocaleString()}</td>
    </tr>
  `).join("");
}

async function checkHealth() {
  try {
    const h = await getJSON("/health");
    document.getElementById("health").textContent = h.status.toUpperCase();
  } catch {
    document.getElementById("health").textContent = "OFFLINE";
  }
}

loadData();
checkHealth();
setInterval(loadData, 10000);
