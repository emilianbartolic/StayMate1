let properties = [];
const propertyScenes = {
  "design-maisonette": { image:"assets/properties/design-maisonette.jpg", caption:"Maisonette mit Wendeltreppe und offener Küche", alt:"Modernes Maisonette-Interieur mit Wendeltreppe und offener Küche", credit:"Foto: Alex Tyson / Unsplash", url:"https://unsplash.com/photos/a-living-room-filled-with-furniture-and-a-spiral-staircase-5ESQy7RsjWE" },
  "city-loft": { image:"assets/properties/city-loft.jpg", caption:"Helles, modernes Stadtapartment", alt:"Helles modernes Apartment mit großzügigem Wohnbereich", credit:"Foto: Nha Chill / Unsplash", url:"https://unsplash.com/photos/a-bright-and-airy-living-room-with-modern-decor-ZuHIek5xn_I" },
  "lake-house": { image:"assets/properties/lake-house.jpg", caption:"Ferienhaus direkt am See", alt:"Holzhaus am Seeufer mit Wald im Hintergrund", credit:"Foto: Danny Giebe / Unsplash", url:"https://unsplash.com/photos/brown-wooden-house-near-lake-surrounded-by-trees-during-daytime-2ASwewGVSPE" }
};
let activePropertyId = "design-maisonette";
const el = (id) => document.getElementById(id);
let csrfValue = "";
let canManageTickets = false;
async function csrfHeader() {
  if (!csrfValue) { const response = await fetch("/api/auth/csrf"); if (response.ok) csrfValue = (await response.json()).csrf_token || ""; }
  return csrfValue ? {"X-StayMate-CSRF": csrfValue} : {};
}
let tickets = [];
let conversationId = localStorage.getItem("staymate-conversation-id");
if (!conversationId) { conversationId = crypto.randomUUID(); localStorage.setItem("staymate-conversation-id", conversationId); }
const escapeHtml = (value) => value.replace(/[&<>'"]/g, character => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", "'":"&#39;", '"':"&quot;" })[character]);
function addMessage(text, role, note = "") { const article = document.createElement("article"); article.className = `message ${role}`; article.innerHTML = `<div class="avatar">${role === "agent" ? "S" : "G"}</div><div class="bubble"><p>${escapeHtml(text)}</p>${note ? `<small class="${note.includes("direkt") ? "escalation-note" : ""}">${escapeHtml(note)}</small>` : ""}</div>`; el("messages").append(article); el("messages").scrollTop = el("messages").scrollHeight; return article; }
function setDecision(escalated, sources = [], error = false) { const box = el("decision"); const generalAnswer = !error && !escalated && sources.length === 0; box.className = `decision ${error ? "error" : escalated ? "escalate" : "safe"}`; box.innerHTML = error ? '<span class="decision-icon">!</span><div><strong>Codex nicht erreichbar</strong><p>Es wurde keine Antwort erstellt.</p></div>' : escalated ? '<span class="decision-icon">!</span><div><strong>Host muss bestätigen</strong><p>Die Frage liegt in der lokalen Warteschlange.</p></div>' : generalAnswer ? '<span class="decision-icon">i</span><div><strong>Allgemeine Antwort</strong><p>Hier wurden keine Unterkunftsangaben bestätigt.</p></div>' : '<span class="decision-icon">✓</span><div><strong>Infos gefunden</strong><p>Codex hat bestätigte Angaben zu dieser Unterkunft verwendet.</p></div>'; el("sources").innerHTML = sources.length ? sources.map(s => `<li>${escapeHtml(s)}</li>`).join("") : "<li>Keine bestätigte Information für diese Frage</li>"; }
function setJourney(step, message) { const progress = el("journey-progress"); progress.setAttribute("aria-valuenow", step); progress.style.setProperty("--progress", `${((step - 1) / 2) * 100}%`); el("journey-count").textContent = `${step} von 3`; el("journey-message").textContent = message; document.querySelectorAll("[data-journey-step]").forEach(item => { const itemStep = Number(item.dataset.journeyStep); item.classList.toggle("active", itemStep === step); item.classList.toggle("done", itemStep < step); }); }
function showTrace(text, working = false) { const trace = el("agent-trace"); if (!trace) return; trace.classList.toggle("working", working); trace.lastElementChild.textContent = text; }
function updateAdvisor() { if (!tickets.length) return; const early = tickets.filter(ticket => /früher|early|später|late/i.test(ticket.question)).length; const unknown = tickets.length - early; if (early) { el("advisor-title").textContent = "Muster: Check-in-Zeiten"; el("advisor-text").textContent = `${early} Anfrage(n) betreffen einen frühen oder späten Check-in. Ergänze eine klare Host-Regel in der Wissensbasis.`; } else if (unknown) { el("advisor-title").textContent = "Muster: Wissenslücke"; el("advisor-text").textContent = `${unknown} Anliegen konnten nicht sicher beantwortet werden. Prüfe sie und ergänze bestätigte Antworten als FAQ.`; } }
function renderTickets() {
  const open=tickets.filter(ticket=>ticket.status==="open");
  const done=tickets.filter(ticket=>ticket.status==="answered");
  el("ticket-count").textContent=open.length;el("open-count").textContent=open.length;el("answered-count").textContent=done.length;updateAdvisor();
  el("tickets").innerHTML=tickets.length?tickets.map(ticket=>{
    const source=ticket.source_url?'<p><a href="'+escapeHtml(ticket.source_url)+'" target="_blank" rel="noopener noreferrer">Objekt beim Anbieter öffnen</a></p>':'';
    const answerBox=ticket.status==="open"?'<label class="host-reply-label">Antwort des Gastgebers (vom Buchungsportal übernehmen)<textarea data-host-reply="'+ticket.id+'" rows="3" maxlength="2000" placeholder="Antwort hier eintragen …"></textarea></label><button class="resolve" data-host-send="'+ticket.id+'">Antwort im Gast-Chat anzeigen</button>':'<p class="host-saved-reply"><strong>Antwort an Gast:</strong> '+escapeHtml(ticket.host_reply||"Antwort gespeichert.")+'</p>';
    return '<article class="ticket"><div class="ticket-top"><strong>'+ (ticket.status==="open"?"Host-Antwort benötigt":"✓ Antwort erfasst")+' · '+escapeHtml(ticket.priority||"normal")+'</strong><small>'+escapeHtml(ticket.property_name||"Unterkunft")+'</small></div><p>„'+escapeHtml(ticket.question)+'"</p><small>'+escapeHtml(ticket.category||"")+'</small>'+source+answerBox+'</article>';
  }).join(""):'<div class="empty-state"><span>✓</span><h3>Keine offenen Anfragen</h3><p>Fragen, die Codex nicht sicher aus bestätigten Fakten beantworten kann, erscheinen hier.</p></div>';
  el("tickets").querySelectorAll("[data-host-send]").forEach(button=>button.addEventListener("click",()=>{
    const ticketId=button.dataset.hostSend,field=el("tickets").querySelector('[data-host-reply="'+ticketId+'"]'),reply=field?.value.trim();
    if(!reply)return;
    button.disabled=true;
    csrfHeader().then(csrf=>fetch('/api/tickets/'+encodeURIComponent(ticketId)+'/reply',{method:'POST',headers:{'Content-Type':'application/json',...csrf},body:JSON.stringify({reply})})).then(async response=>{if(!response.ok)throw new Error();await loadTickets();await loadConversationReplies(activePropertyId);}).catch(()=>{button.disabled=false;field?.focus();});
  }));
}
async function loadTickets(){try{const response=await fetch('/api/tickets');if(!response.ok)throw new Error();const data=await response.json();tickets=data.items||[];renderTickets();}catch{el("tickets").innerHTML='<div class="empty-state"><h3>Host-Warteschlange nicht erreichbar</h3><p>Der lokale Speicher ist gerade nicht erreichbar.</p></div>';}}
async function loadConversationReplies(propertyId){try{const response=await fetch('/api/conversations/'+encodeURIComponent(conversationId)+'/replies');if(!response.ok)return;const data=await response.json();(data.items||[]).filter(item=>item.property_id===propertyId).forEach(item=>addMessage(item.reply,"agent","Antwort des Gastgebers"));}catch{}}
async function getAgentAnswer(question,imageFile) {
  try{
    const body=new FormData();body.append("question",question||"Bitte beschreibe dieses Bild im Zusammenhang mit der Unterkunft.");body.append("property_id",activePropertyId);body.append("conversation_id",conversationId);if(imageFile)body.append("image",imageFile);
    const csrf=await csrfHeader();const response=await fetch("/api/chat",{method:"POST",headers:csrf,body});
    if(response.status===401){location.href="/?sign-in=1";return;}
    if(!response.ok){const error=await response.json().catch(()=>({}));throw new Error(error.detail||"StayMate konnte Codex nicht erreichen.");}
    const result=await response.json();
    if(result.model_used!==true)throw new Error("Codex hat keine Antwort erstellt.");
    setDecision(result.decision==="escalate",result.sources);
    if(result.decision==="escalate"&&canManageTickets)await loadTickets();
    return {answer:result.answer,decision:result.decision};
  }catch(error){
    if(canManageTickets)await loadTickets();
    setDecision(false,[],true);
    return {answer:"Codex ist gerade nicht erreichbar. Ich habe keine automatische Antwort erstellt. Bitte versuche es erneut, wenn Codex verbunden ist.",decision:"error",note:"Eine externe Plattform wurde nicht benachrichtigt."};
  }
}
function updateProperty(propertyId) {
  const property=properties.find(item=>item.id===propertyId)||properties[0];if(!property)return;
  const scene=propertyScenes[property.id]||{image:property.image||"assets/properties/design-maisonette.jpg",caption:property.demo_only?property.name:"Bilder und Termine beim Anbieter",alt:property.image_alt||("Bild zu "+property.name),credit:property.demo_only?(property.image_label||"KI-Beispielbild · kein echtes Objekt"):property.image_credit||"Bildquelle beim Anbieter",url:property.source_url||"",imagePosition:property.image_position};
  activePropertyId=property.id;el("property-select").value=property.id;el("property-meta").textContent=property.location;
  el("checkin-time").textContent=property.demo_only?property.check_in||"Nicht hinterlegt · Demo":property.check_in||"Beim Anbieter erfragen";el("checkout-time").textContent=property.demo_only?property.check_out||"Nicht hinterlegt · Demo":property.check_out||"Beim Anbieter erfragen";
  el("sources").innerHTML='<li>'+escapeHtml(property.name)+'</li>';
  el("messages").innerHTML='<article class="message agent"><div class="avatar">S</div><div class="bubble"><p>'+(property.demo_only?'Du siehst jetzt die fiktive Wohnidee „'+escapeHtml(property.name)+'“. Was möchtest du dazu wissen?':'Du chattest jetzt zu '+escapeHtml(property.name)+'. Was möchtest du wissen?')+'</p><small>'+(property.demo_only?'Das KI-Beispielbild und die Wohnungsdaten sind nur ein Muster. Echte Unterkünfte findest du über die Stadtsuche.':'Codex beantwortet Fragen aus den bestätigten Angaben; offene Punkte kommen in die Host-Warteschlange.')+'</small></div></article>';
  setJourney(1,"Womit kann ich dir helfen?");
  const photoFrame=el("property-photo").closest(".property-visual");photoFrame?.classList.remove("scene-crop-left","scene-crop-right");if(scene.imagePosition)photoFrame?.classList.add(scene.imagePosition.endsWith("right")?"scene-crop-right":"scene-crop-left");
  el("property-photo").src=scene.image;el("property-photo").alt=scene.alt;el("property-caption").textContent=scene.caption;el("photo-credit").textContent=scene.credit;el("photo-credit").href=scene.url||"#";
  el("photo-disclaimer").textContent=property.demo_only?"Musterbild · keine echte Unterkunft":property.source_url?"Bild und Angaben beim Anbieter prüfen":"Beispielbild, nicht das konkrete Mietobjekt";
  el("selection-note").textContent=property.demo_only?"Dies ist nur eine fiktive Wohnidee, keine echte Unterkunft. Nutze die Stadtsuche für reale Angebote.":"Der Objekt-Chat ist für Fragen nach deiner Auswahl. Er bestätigt keine Buchung; externe Buchungen schließt du beim Anbieter ab.";
  el("privacy-note").textContent=property.demo_only?"Deine Nachricht und ein hochgeladenes Bild werden an Codex übermittelt. Angaben zu Anreise und Parken sind fiktive Demo-Werte; die Wohnidee hat keinen Host.":"Deine Nachricht und ein hochgeladenes Bild werden zur Antwort an Codex übermittelt. Offene Punkte kommen in eine lokale Host-Warteschlange; Airbnb oder Booking.com werden nicht automatisch benachrichtigt.";
  el("photo-credit").hidden=!scene.url;
  const sourceLink=el("property-source");if(sourceLink){sourceLink.href=property.demo_only?property.search_url||"#":property.source_url||"#";sourceLink.hidden=!property.source_url&&!property.demo_only;sourceLink.textContent=property.demo_only?property.search_label||"Echte Unterkünfte suchen":property.source_url?"Angebot beim Anbieter öffnen":"";}
  el("property-status").textContent=property.demo_only?"Wohnidee · Demo, kein Inserat":localStorage.getItem("staymate-current-object")===property.id?"Auswahl vorgemerkt · noch nicht gebucht":"Unterkunft aktiv";
  showTrace(property.name+" · Codex bereit");
  loadConversationReplies(property.id);
}
const propertySelect=el("property-select");
propertySelect.addEventListener("change",event=>updateProperty(event.target.value));
async function loadProperties(){
  try{
    const response=await fetch("/api/properties");if(!response.ok)throw new Error();
    properties=await response.json();
    const offered=properties.filter(property=>!property.demo_only),concepts=properties.filter(property=>property.demo_only);
    propertySelect.innerHTML='<optgroup label="StayMate-Objekte und Inserate">'+offered.map(property=>'<option value="'+escapeHtml(property.id)+'">'+escapeHtml(property.name)+'</option>').join("")+'</optgroup><optgroup label="Wohnideen · fiktive Demo-Konzepte">'+concepts.map(property=>'<option value="'+escapeHtml(property.id)+'">'+escapeHtml(property.name)+'</option>').join("")+'</optgroup>';
    const requested=new URLSearchParams(location.search).get("property_id");
    const saved=localStorage.getItem("staymate-current-object");
    const start=properties.some(item=>item.id===requested)?requested:properties.some(item=>item.id===saved)?saved:"design-maisonette";
    updateProperty(start);
  }catch{
    el("property-status").textContent="Portfolio nicht erreichbar";
    addMessage("StayMate konnte das Objekt-Portfolio nicht laden. Bitte prüfe die lokale Verbindung.","agent");
    el("send-button").disabled=true;
  }
}
loadProperties();
fetch("/api/auth/me").then(response=>response.json()).then(state=>{
  canManageTickets=state.user?.role==="host";
  el("dashboard-toggle").hidden=!canManageTickets;
  if(canManageTickets)loadTickets();
}).catch(()=>{});
let selectedImage = null;
el("image-upload").addEventListener("change", event => { selectedImage = event.target.files?.[0] || null; el("image-selection").textContent = selectedImage ? `Bild angehängt: ${selectedImage.name}` : ""; });
el("chat-form").addEventListener("submit", async (event) => { event.preventDefault(); const input = el("question"); const question = input.value.trim(); if (!question && !selectedImage) return; const image = selectedImage; addMessage(question || "Was ist auf diesem Bild zu sehen?", "guest"); input.value = ""; setJourney(2, "Gute Frage — ich suche die passenden Infos für dich."); el("send-button").disabled = true; const pending = addMessage("Einen kleinen Moment …", "agent", "Ich prüfe die Infos zu deiner Unterkunft."); const result = await getAgentAnswer(question, image); pending.remove(); addMessage(result.answer, "agent"); setJourney(3, result.decision === "error" ? "Codex ist nicht erreichbar; es wurde keine Antwort erstellt." : result.decision === "escalate" ? "Der Gastgeber muss noch bestätigen." : "Geschafft! Deine Antwort ist da."); selectedImage = null; el("image-upload").value = ""; el("image-selection").textContent = ""; el("send-button").disabled = false; });
document.querySelectorAll(".suggestions button").forEach(button => button.addEventListener("click", () => { el("question").value = button.dataset.question; el("chat-form").requestSubmit(); }));
el("reset").addEventListener("click", () => { updateProperty(activePropertyId); setDecision(false, []); });
el("dashboard-toggle").addEventListener("click", () => { el("dashboard").classList.add("open"); el("dashboard").setAttribute("aria-hidden", "false"); });
el("dashboard-close").addEventListener("click", () => { el("dashboard").classList.remove("open"); el("dashboard").setAttribute("aria-hidden", "true"); });
