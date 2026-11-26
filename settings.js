const byId = id => document.getElementById(id);

let csrfToken = "";
async function api(url, options = {}) {
  const headers = {...(options.headers || {})};
  if ((options.method || "GET").toUpperCase() !== "GET") {
    if (!csrfToken) csrfToken = (await fetch("/api/auth/csrf").then(r => r.json())).csrf_token || "";
    if (csrfToken) headers["X-StayMate-CSRF"] = csrfToken;
  }
  options = {...options, headers};
  const response = await fetch(url, options);
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).detail || "Die lokale API antwortet nicht.");
  return response.json();
}

async function loadStatus() {
  try {
    const status = await api("/api/status");
    byId("model-status").textContent = status.model_enabled ? (status.model_configured ? "Codex aktiv" : "Codex nicht gefunden") : "Codex angehalten";
    byId("model-detail").textContent = status.model_configured ? `${status.model_calls_today} von ${status.model_call_limit} Modellaufrufen heute; maximal ${status.model_max_concurrent} gleichzeitig.` : "Codex-CLI installieren und anmelden.";
    byId("model-stop-status").textContent = status.model_enabled ? "Neue Modellaufrufe sind aktiv." : "Der Not-Aus ist aktiv; neue Modellaufrufe sind gesperrt.";
    byId("model-stop-button").hidden = !status.model_enabled;
    byId("model-resume-button").hidden = status.model_enabled;
    byId("portfolio-status").textContent = `${status.properties} Objekte aktiv`;
    byId("skill-status").textContent = `${status.skills} interne Schritte aktiv`;
    byId("memory-count").textContent = `${status.tickets_total} Tickets gespeichert`;
  } catch {
    byId("model-status").textContent = "StayMate-Backend nicht erreichbar";
    byId("portfolio-status").textContent = "Nicht verfügbar";
    byId("skill-status").textContent = "Nicht verfügbar";
    byId("memory-count").textContent = "Nicht verfügbar";
  }
}

async function loadMemory() {
  const box = byId("memory-list");
  try {
    const [pending, approved] = await Promise.all([
      api("/api/memory?status_filter=pending"),
      api("/api/memory?status_filter=approved"),
    ]);
    const entries = [...(pending.items || []), ...(approved.items || [])];
    box.replaceChildren();
    if (!entries.length) { box.textContent = "Noch keine Memory-Einträge."; return; }
    for (const item of entries) {
      const row = document.createElement("article"); row.className = "memory-item";
      const content = document.createElement("p"); content.textContent = item.content;
      const meta = document.createElement("small"); meta.className = "muted";
      meta.textContent = `${item.scope} · ${item.source} · ${item.status}`;
      row.append(content, meta);
      if (item.status === "pending") {
        const button = document.createElement("button"); button.type = "button"; button.textContent = "Freigeben";
        button.addEventListener("click", async () => {
          button.disabled = true;
          try { await api(`/api/memory/${item.id}/approve`, {method:"POST"}); await loadMemory(); }
          catch (error) { button.disabled = false; meta.textContent = error.message; }
        });
        row.append(document.createElement("br"), button);
      }
      box.append(row);
    }
  } catch (error) { box.textContent = error.message; }
}

byId("memory-form").addEventListener("submit", async event => {
  event.preventDefault(); byId("memory-status-message").textContent = "";
  try {
    await api("/api/memory", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      content:byId("memory-content").value,
      scope:byId("memory-scope").value,
      source:byId("memory-source").value,
    })});
    byId("memory-content").value = "";
    byId("memory-status-message").textContent = "Notiz gespeichert und wartet auf Freigabe.";
    await loadMemory();
  } catch (error) { byId("memory-status-message").textContent = error.message; }
});

byId("backup-button").addEventListener("click", async () => {
  const button = byId("backup-button"); button.disabled = true;
  try {
    const result = await api("/api/admin/backup", {method:"POST"});
    byId("backup-status").textContent = `Backup erstellt: ${result.backup}`;
  } catch (error) { byId("backup-status").textContent = error.message; }
  finally { button.disabled = false; }
});

byId("model-stop-button").addEventListener("click", async () => {
  try { await api("/api/admin/model/stop", {method:"POST"}); await loadStatus(); }
  catch (error) { byId("model-stop-status").textContent = error.message; }
});
byId("model-resume-button").addEventListener("click", async () => {
  try { await api("/api/admin/model/resume", {method:"POST"}); await loadStatus(); }
  catch (error) { byId("model-stop-status").textContent = error.message; }
});

async function loadProperties() {
  try {
    const items = await api("/api/properties");
    for (const item of items) {
      const option = document.createElement("option"); option.value = item.id; option.textContent = item.name;
      byId("memory-scope").append(option);
    }
  } catch { /* Status cards already describe a disconnected backend. */ }
}

async function loadIntegrations() {
  const box = byId("integration-list");
  try {
    const data = await api("/api/integrations");
    box.replaceChildren();
    for (const provider of data.integrations || []) {
      const card = document.createElement("article"); card.className = "integration-item";
      const heading = document.createElement("h3"); heading.textContent = provider.provider;
      const status = document.createElement("strong"); status.textContent = provider.connected ? "Verbunden" : "Nicht verbunden · Partnerzugang erforderlich";
      const note = document.createElement("p"); note.className = "muted";
      note.textContent = provider.adapter_available ? "Adapter verfügbar." : "Für diesen Anbieter ist in dieser Version noch kein aktiver Adapter eingerichtet.";
      const list = document.createElement("ul");
      for (const requirement of provider.requirements || []) { const item = document.createElement("li"); item.textContent = requirement; list.append(item); }
      card.append(heading, status, note, list); box.append(card);
    }
  } catch (error) { box.textContent = error.message; }
}

async function startDashboard() {
  try {
    const auth = await fetch("/api/auth/me").then(r => r.json());
    if (auth.admin_required && auth.user?.role !== "host") {
      byId("admin-login").hidden = false;
      return;
    }
    if (auth.required && auth.user?.role !== "host") { location.replace("/?sign-in=1"); return; }
  } catch { location.replace("/"); return; }
  byId("dashboard-content").hidden = false;
  loadStatus(); loadMemory(); loadProperties(); loadIntegrations();
}
byId("admin-login-form").addEventListener("submit", async event => {
  event.preventDefault();
  const button = event.currentTarget.querySelector("button[type=submit]");
  button.disabled = true;
  byId("admin-login-status").textContent = "";
  try {
    await api("/api/auth/login", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({email:byId("admin-email").value.trim(), password:byId("admin-password").value})});
    location.reload();
  } catch (error) {
    byId("admin-login-status").textContent = error.message;
  } finally {
    button.disabled = false;
  }
});
startDashboard();
