const catalog = [
  { id:"design-maisonette", name:"Design-Maisonette", type:"Apartment", sourceType:"StayMate", location:"Gärtringen · Raum Stuttgart", regions:["gärtringen","stuttgart-umgebung"], guests:4, image:"assets/properties/design-maisonette.jpg", alt:"Symbolbild, kein Originalfoto der Unterkunft", area:null, rooms:null, features:["Zwei kostenlose Stellplätze","WLAN & eigener Arbeitsplatz","Zwei Ebenen mit Wendeltreppe","Kingsize-Bett und Schlafcouch"], difference:"Zwei Ebenen und eigene Stellplätze; liegt in Gärtringen statt in Stuttgart-Mitte.", layout:["Wohnen","Schlafen & Bad über Wendeltreppe"], description:"Maisonette auf zwei Ebenen für bis zu vier Gäste, mit Arbeitsplatz und Parkplatz." },
  { id:"city-loft", name:"City Loft", type:"Apartment", sourceType:"StayMate", location:"Stuttgart-Mitte", regions:["stuttgart","stuttgart-mitte"], guests:2, image:"assets/properties/city-loft.jpg", alt:"Symbolbild, kein Originalfoto der Unterkunft", area:null, rooms:null, features:["Zentral in Stuttgart-Mitte","S-Bahn in fünf Minuten","Schnelles WLAN","Kein eigener Stellplatz; Parkhaus in zwei Gehminuten"], difference:"Zentrale Wahl für zwei Gäste, mit S-Bahn und Parkhaus nah. Kein eigener Parkplatz und kein separater Arbeitsplatz.", layout:null, description:"Zentrales Loft für bis zu zwei Gäste mit Doppelbett und schnellem WLAN." },
  { id:"lake-house", name:"Haus am See", type:"Ferienhaus", sourceType:"StayMate", location:"Bodensee · ruhige Lage", regions:["bodensee"], guests:6, image:"assets/properties/lake-house.jpg", alt:"Symbolbild, kein Originalfoto der Unterkunft", area:null, rooms:4, features:["Drei Schlafzimmer","See in fünf Minuten zu Fuß","Drei kostenlose Stellplätze","WLAN & Arbeitsplatz mit Gartenblick"], difference:"Drei Schlafzimmer und Platz für bis zu sechs; ruhig am See statt in einer Stadtmitte.", layout:["Wohnen & Küche","Schlafzimmer 1","Schlafzimmer 2","Schlafzimmer 3"], description:"Ruhiges Haus am Bodensee für bis zu sechs Gäste mit drei Schlafzimmern." },
  { id:"airbnb-gaertringen-70", name:"Apartment mit Terrasse · 70 m²", type:"Apartment", sourceType:"Airbnb", sourceUrl:"https://www.airbnb.de/rooms/33947915", sourceLabel:"Auf Airbnb ansehen", checked:"24.11.2026", location:"Gärtringen · Raum Stuttgart", regions:["gärtringen","stuttgart-umgebung"], guests:4, area:70, rooms:2, image:"https://cf.bstatic.com/xdata/images/hotel/max1024x768/421713080.jpg?k=acfac9ba4523616cace707831c587c2808ea7fd9b11a7ad98fad0c1a8b53d470&o=",alt:"Wohnzimmer des 70-m²-Apartments in Gärtringen mit Zugang zur Terrasse",imageLabel:"Inseratsfoto",features:["1 Schlafzimmer · 3 Betten","Private Terrasse & eigener Eingang","Zwei Parkplätze","Voll ausgestattete Küche · 24-Stunden-Code-Check-in"], difference:"70 m² mit privater Terrasse und zwei Stellplätzen; kompakter als das 110-m²-Apartment.", layout:["Wohnen & Küche","Schlafzimmer","Bad","Terrasse"], description:"Erdgeschoss-Apartment für bis zu vier Personen; öffentliches Inserat bei Airbnb." },
  { id:"booking-gaertringen-110", name:"Apartment mit Balkon · 110 m²", type:"Apartment", sourceType:"Booking.com", sourceUrl:"https://www.booking.com/hotel/de/3-zimmer-apartment-110-qm-max-5-personen-balkon-parkplatz-internet-250-mbit.de.html", sourceLabel:"Auf Booking.com ansehen", checked:"24.11.2026", location:"Gärtringen · Raum Stuttgart", regions:["gärtringen","stuttgart-umgebung"], guests:5, area:110, rooms:3, image:"assets/properties/external-apartment-visualizations.png",imagePosition:"visualization-left",alt:"KI-Visualisierung eines großzügigen Apartments mit Balkon",imageLabel:"Visualisierung · kein Inseratsfoto",features:["2 Schlafzimmer · bis zu 5 Gäste","Balkon","Kostenloser Privatparkplatz","WLAN · Küche · Haustiere auf Anfrage"], difference:"Größte Stadtregion-Option: 110 m², zwei Schlafzimmer und Balkon für bis zu fünf Gäste.", layout:["Wohnen","Küche","Schlafzimmer 1","Schlafzimmer 2","Balkon"], description:"Drei-Zimmer-Apartment mit Balkon und kostenlosem Privatparkplatz; öffentliches Booking.com-Inserat." },
  { id:"stuttgart-hinterhaus", name:"Gemütliches Hinterhaus", type:"Ferienhaus", sourceType:"Ferienwohnungen.de", sourceUrl:"https://www.ferienwohnungen.de/vacation-home/70219532", sourceLabel:"Angebot und Termine ansehen", checked:"24.11.2026", location:"Stuttgart · Weilimdorf", regions:["stuttgart","weilimdorf"], guests:4, area:35, rooms:2, image:"https://img.holidu.com/images/c2135189-8b9f-4c57-82d3-ee9c99e5a770/l.jpg",alt:"Innenraumfoto des gemütlichen Hinterhauses in Stuttgart-Weilimdorf",imageLabel:"Inseratsfoto",features:["1 Schlafzimmer · Betten für bis zu 4","Klimaanlage & WLAN","Küche · Waschmaschine · Trockner","ÖPNV-Anbindung · Parken an der Straße"], difference:"Kleines 35-m²-Hinterhaus direkt in Stuttgart; Klimaanlage und WLAN, aber kein Privatparkplatz.", layout:["Wohnbereich & Küche","Schlafzimmer im Obergeschoss"], description:"35-m²-Ferienhaus in Weilimdorf für bis zu vier Personen; Reisetermine und Preis zeigt die Angebotsseite." },
  { id:"konstanz-ana", name:"Ferienwohnung Ana", type:"Apartment", sourceType:"Bodensee.travel · Direktvermieter", sourceUrl:"https://www.bodensee.travel/ferienwohnung-konstanz-ana/", sourceLabel:"Beim Vermieter ansehen", checked:"24.11.2026", location:"Konstanz · Musikerviertel", regions:["bodensee","konstanz"], guests:6, area:80, rooms:4, image:"assets/properties/external-apartment-visualizations.png",imagePosition:"visualization-right",alt:"KI-Visualisierung einer Altbauwohnung in Konstanz mit zwei Balkonen",imageLabel:"Visualisierung · kein Inseratsfoto",features:["3 Schlafzimmer","100 m bis zum Bodensee · Seeblick","Zwei Balkone","Eigener Parkplatz · WLAN"], difference:"Drei Schlafzimmer und zwei Balkone nur 100 m vom See; ruhige Stadtlage in Konstanz.", layout:["Wohnzimmer & Küche","Schlafzimmer 1","Schlafzimmer 2","Schlafzimmer 3","Bad"], description:"Privat vermietete 80-m²-Wohnung in Konstanz für bis zu sechs Personen." },
  { id:"villa-koepfler-family", name:"Wohnung Family · Villa Köpfler", type:"Ferienwohnung", sourceType:"Villa Köpfler · Direktvermieter", sourceUrl:"https://www.villabodensee.eu/villa-koepfler/wohnung-family", sourceLabel:"Beim Vermieter ansehen", checked:"24.11.2026", location:"Gaienhofen · Bodensee", regions:["bodensee","gaienhofen"], guests:8, area:220, rooms:5, guestNote:"Für 6 Erwachsene und 2 Kinder", image:"https://www.villabodensee.eu/fileadmin/_processed_/9/0/csm_WG-Family-OG-Kueche_bc56aa4ece.webp",alt:"Küche und Essbereich der Wohnung Family in der Villa Köpfler",imageLabel:"Foto des Anbieters",features:["4 Schlafzimmer · 220 m² auf 3 Ebenen","Dachterrasse mit Seeblick","Sauna · gemeinschaftlicher Naturpool","Zwei Außenstellplätze"], difference:"Größte Gruppenoption: 220 m², vier Schlafzimmer, Sauna und Dachterrasse; passend für bis zu sechs Erwachsene plus zwei Kinder.", layout:["Wohnbereich & Küche","Schlafzimmer 1","Schlafzimmer 2","Schlafzimmer 3","Schlafzimmer 4","Dachterrasse"], description:"Große Ferienwohnung der Villa Köpfler; der Belegungskalender und Anfrageweg liegen beim Vermieter." },
  { id:"seebalkon-radolfzell", name:"Seebalkon · wählbare Wohnungsgröße", type:"Ferienwohnung", sourceType:"Seebalkon · Direktvermieter", sourceUrl:"https://www.seebalkon.de/buchen/", sourceLabel:"Preise und Termine ansehen", checked:"24.11.2026", location:"Radolfzell · Halbinsel Mettnau", regions:["bodensee","radolfzell"], guests:6, area:110, rooms:4, sizeOptions:[{maxGuests:2,area:70,rooms:2},{maxGuests:4,area:90,rooms:3},{maxGuests:6,area:110,rooms:4}], image:"https://www.bodenseeurlaub.de/media/jfewo/images/981/thumb/balkon1579025644-a3e32b53.jpg",alt:"Balkon der Ferienwohnung Seebalkon mit Blick zum Bodensee",imageLabel:"Inseratsfoto",features:["Je nach Gruppengröße 70, 90 oder 110 m²","Bis zu 3 Schlafzimmer","Seeblick-Balkon & Liegewiese","Zwei Parkplätze · WLAN"], difference:"Ein Objekt, dessen buchbare Größe mit der Gruppe wächst: 70 m² für 1–2, 90 m² für 3–4 und 110 m² für 5–6 Gäste.", layout:["Wohnküche & Wohnzimmer","Schlafzimmer 1","Weitere Schlafzimmer je nach Belegung","Seeblick-Balkon"], description:"Ferienwohnung, die laut Vermieter je nach Gästezahl in drei Größen gebucht wird." },
  { id:"stuttgart-four-room", name:"Großzügig wohnen · 95 m²", type:"Apartment", sourceType:"Airbnb", sourceUrl:"https://www.airbnb.de/rooms/1422649983145720762", sourceLabel:"Auf Airbnb ansehen", checked:"24.11.2026", location:"Stuttgart · Bad Cannstatt", regions:["stuttgart","stuttgart-bad-cannstatt"], guests:4, area:95, rooms:4, image:"https://a0.muscache.com/im/pictures/miso/Hosting-1422649983145720762/original/844df4cf-c8c8-4ffc-bfad-981335f72a9e.jpeg?im_w=720",alt:"Wohnbereich des 95-m²-Apartments in Stuttgart",imageLabel:"Airbnb-Inseratsfoto",features:["2 Schlafzimmer · 2 Doppelbetten","Arbeitszimmer & WLAN","Garten zur Mitbenutzung","Parkplätze vor dem Haus"], difference:"Vier Zimmer mit separatem Arbeitszimmer und Gartenzugang; ruhiger als ein City-Loft und direkt in Stuttgart.",layout:["Wohn- und Esszimmer","Schlafzimmer 1","Schlafzimmer 2","Arbeitszimmer","Küche & Bad"],description:"95-m²-Apartment für bis zu vier Gäste mit zwei Schlafzimmern; Kalender und Buchung laufen über Airbnb." },
  { id:"konstanz-unteres-paradies", name:"Unteres Paradies · 46 m²", type:"Apartment", sourceType:"Konstanz-Ferienwohnung · Direktvermieter", sourceUrl:"https://www.konstanz-ferienwohnung.de/",sourceLabel:"Beim Vermieter ansehen",checked:"24.11.2026",location:"Konstanz · Paradies",regions:["bodensee","konstanz"],guests:2,area:46,rooms:2,image:"assets/properties/konstanz-visualizations.png",imagePosition:"paradise-left",alt:"KI-Visualisierung eines kleinen Apartments mit Balkon in Konstanz",imageLabel:"Visualisierung · kein Inseratsfoto",features:["Für bis zu 2 Personen","Balkon mit Gartenmöbeln","Küche · WLAN","10 Minuten zur Altstadt · 5 Minuten zum Seerhein"],difference:"Kompakte 46 m² für zwei Personen mit eigenem Schlafbereich und Balkon; ruhige Lage im Konstanzer Stadtteil Paradies.",layout:["Wohnen & Schlafen","Küche","Bad","Balkon"],description:"Kleine Ferienwohnung im 1. Obergeschoss; mindestens sechs Nächte laut Anbieter."},
  { id:"konstanz-oberes-paradies", name:"Oberes Paradies · bis 85 m²", type:"Apartment", sourceType:"Konstanz-Ferienwohnung · Direktvermieter", sourceUrl:"https://www.konstanz-ferienwohnung.de/",sourceLabel:"Beim Vermieter ansehen",checked:"24.11.2026",location:"Konstanz · Paradies",regions:["bodensee","konstanz"],guests:4,area:85,rooms:4,image:"assets/properties/konstanz-visualizations.png",imagePosition:"paradise-right",alt:"KI-Visualisierung einer Dachwohnung mit Holzbalken und Balkon in Konstanz",imageLabel:"Visualisierung · kein Inseratsfoto",features:["Bis zu 4 Personen · 2 Schlafzimmer","Dachgeschoss mit Holzdecke","Überdachter Balkon · Eckbadewanne","WLAN · Waschmaschine"],difference:"Größere Dachgeschoss-Wohnung bis 85 m² mit zweitem Schlafzimmer; zusätzlich zum kleinen Unteren Paradies.",layout:["Wohnzimmer","Schlafzimmer 1","Schlafzimmer 2","Küche & Bad","Balkon"],description:"67–85-m²-Dachgeschoss-Wohnung für bis zu vier Personen; Belegung und Anfrage beim Direktvermieter."}
];
const conceptCatalogPromise=fetch("/api/properties").then(response=>response.ok?response.json():[]).then(properties=>{
  const existing=new Set(catalog.map(item=>item.id));
  let added=0;
  for(const property of properties.filter(item=>item.demo_only)){
    if(existing.has(property.id))continue;
    catalog.push({
      id:property.id,name:property.name,type:property.type||"Apartment",sourceType:property.source_type||"Wohnidee · fiktives Konzept",
      location:property.location,regions:property.regions||[],guests:property.guests,area:property.area,rooms:property.rooms,examplePricePerNight:property.example_price_per_night,
      image:property.image,alt:property.image_alt,imageLabel:property.image_label,features:property.features||[],
      difference:property.difference,layout:property.layout,description:property.description,demoOnly:true,
      sourceUrl:null,searchUrl:property.search_url,searchLabel:property.search_label,availabilityChecked:false
    });
    existing.add(property.id);added++;
  }
  if(added)refreshObjectChatSwitch();
  return added;
}).catch(()=>0);
catalog.forEach(item=>{
  item.regions=[...(item.regions||[]),"Deutschland","Baden-Württemberg"];
  if(/gärtringen/i.test(item.location))item.regions.push("Landkreis Böblingen");
});
const questions = [
  { key:"dates", ask:"Wann möchtest du reisen? Wenn du noch flexibel bist, kannst du das sagen. Für konkrete Verfügbarkeiten brauche ich An- und Abreise (z. B. 12.12.2026–15.12.2026).", suggestions:["Noch flexibel", "Daten später festlegen"] },
  { key:"guests", ask:"Wie viele Erwachsene und Kinder reisen mit? So kann ich passende Schlafplätze vergleichen.", suggestions:["Allein", "Zu zweit", "Mit Familie"] },
  { key:"type", ask:"Welche Unterkunft passt besser: Apartment, ganzes Ferienhaus oder beides?", suggestions:["Apartment", "Ferienhaus", "Beides ansehen"] },
  { key:"size", ask:"Welche Wohnungsgröße oder Zimmerzahl wünschst du? Wenn du offen bist, vergleiche ich verschiedene Größen.", suggestions:["2 Zimmer", "3 Zimmer", "Ab 70 m²"] }
];
const followupQuestions=[
  {key:"budget",ask:"Welches Budget pro Nacht ist für euch ungefähr passend? Ich berücksichtige es als Richtwert; aktuelle Preise prüft der Anbieter.",suggestions:["Bis 100 €", "100–200 €", "Flexibel"]},
  {key:"needs",ask:"Was ist euch wichtiger: Ruhe und Natur, eine zentrale Lage oder gute Verkehrsanbindung?",suggestions:["Natur & Ruhe", "Zentral gelegen", "Gute Anbindung"]},
  {key:"musthave",ask:"Welche Ausstattung ist euch wichtig? Zum Beispiel Balkon, Garten, Parkplatz, WLAN oder Küche.",suggestions:["Balkon oder Garten", "Parkplatz", "WLAN & Arbeiten"]},
  {key:"sleeping",ask:"Wie möchtet ihr schlafen: lieber getrennte Schlafzimmer oder ist ein Wohn-Schlafbereich in Ordnung?",suggestions:["Getrennte Zimmer", "Ein Schlafzimmer reicht", "Flexibel"]},
  {key:"accessibility",ask:"Gibt es noch etwas, worauf ich achten soll, etwa wenige Treppen, Kinderbett, Haustier oder Barrierefreiheit?",suggestions:["Wenig Treppen", "Mit Haustier", "Keine Besonderheiten"]}
];
const clarificationQuestions=[
  {key:"refine_issue",ask:"Was passt an meiner Empfehlung noch nicht ganz? Ich kann Lage, Größe, Preisrahmen oder Unterkunftsart ändern.",suggestions:["Lieber größer", "Lieber zentral", "Anderes Objekt"]},
  {key:"refine_priority",ask:"Was soll ich bei der neuen Auswahl am stärksten gewichten?",suggestions:["Mehr Zimmer", "Mehr Ruhe", "Balkon oder Garten"]}
];
const state = { step:0, followupStep:0, clarificationStep:0, phase:"gathering", profile:{place:"",dates:"",guests:"",size:"",type:"",budget:"",needs:"",musthave:"",sleeping:"",accessibility:""} };
let focusedListing=null,selectedListingId=null,recommendedListingId=null;
let latestMatches=[],visibleListingCount=12,liveProviderConfigured=null,liveAvailabilityChecked=false;
function refreshObjectChatSwitch(){const link=$("object-chat-switch");if(!link)return;const id=selectedListingId||localStorage.getItem("staymate-current-object");const item=catalog.find(x=>x.id===id);if(!item){link.hidden=true;return;}link.href="/staymate.html?property_id="+encodeURIComponent(item.id);link.textContent="Zum Objekt-Chat · "+item.name;link.hidden=false;}
const $ = id => document.getElementById(id);
const esc = value => String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const resolveImageUrl = value => {
  try { return new URL(String(value || ""), document.baseURI).href; }
  catch { return ""; }
};
const conversation = $("conversation");
let isBusy=false;

function addBubble(text, who="bot") {
  const article=document.createElement("article"); article.className=`bubble ${who}-bubble`;
  const avatar=who==="bot"?'<span class="bubble-avatar">✦</span>':'';
  article.innerHTML=`${avatar}<div><p>${esc(text)}</p></div>`; conversation.append(article); conversation.scrollTop=conversation.scrollHeight;return article;
}
function progress(step) {
  const total=10;
  let count=step+1;
  if(state.phase==="deepening")count=6+state.followupStep;
  if(state.phase==="interim"||state.phase==="clarifying"||state.phase==="selected")count=10;
  count=Math.min(count,total);
  $("progress-count").textContent="Schritt "+count+" von "+total;
  $("progress-bar").style.width=(count/total*100)+"%";
  $("progress-title").textContent=state.phase==="deepening"?"Deine Wünsche":state.phase==="interim"?"Deine Empfehlung":state.phase==="clarifying"?"Auswahl verfeinern":state.phase==="selected"?"Dein Objekt":"Deine Suche";
}
function showSuggestions(items) {
  const wrap=$("suggested"); wrap.innerHTML='<span>Du kannst auch tippen</span>'+items.map(x=>`<button type="button" data-suggest="${esc(x)}">${esc(x)}</button>`).join("");
  wrap.querySelectorAll("button").forEach(button=>button.addEventListener("click",()=>submitAnswer(button.dataset.suggest)));
}
function showSizeChoices(){const card=document.createElement("div");card.className="room-choice-grid";card.innerHTML='<button type="button" data-size="2 Zimmer"><b>2 Zimmer</b><span class="mini-floorplan two"><i>Wohnen</i><i>Schlafen</i><i>Bad</i></span><small>Wohnen + separates Schlafzimmer</small></button><button type="button" data-size="3 Zimmer"><b>3 Zimmer</b><span class="mini-floorplan three"><i>Wohnen</i><i>Schlafen 1</i><i>Schlafen 2</i><i>Bad</i></span><small>Mehr Platz für Familie oder Freunde</small></button>';conversation.append(card);conversation.scrollTop=conversation.scrollHeight;card.querySelectorAll("button").forEach(button=>button.addEventListener("click",()=>submitAnswer(button.dataset.size)));}
async function askCodex(message,stage,nextQuestion=""){
  const selected=state.phase==="selected"?catalog.find(x=>x.id===selectedListingId):null;
  const source=(stage==="recommendations"||stage==="refinement")?latestMatches:[];
  const candidates=source.slice(0,5).map(x=>{
    const availability=x.demoOnly?"fiktive Idee; nicht buchbar":x.availabilityChecked?"Anbieter meldet für angefragte Termine verfügbar":"Verfügbarkeit nicht geprüft";
    const price=x.demoOnly?`fiktiver Demo-Richtwert ca. ${x.examplePricePerNight} EUR pro Nacht`:x.priceTotal!==null&&x.priceTotal!==undefined?`Gesamt ${x.priceTotal} ${x.currency||"EUR"}${x.nights?` für ${x.nights} Nächte`:""}`:"kein Live-Preis";
    return "["+x.id+"] "+x.name+" ("+x.location+"); "+(x.guests?`bis ${x.guests} Gäste`:"Belegung unbekannt")+(x.area?", ca. "+x.area+" m² (nur Entwurf)":"")+(x.rooms?", "+x.rooms+" Zimmer (nur Entwurf)":"")+"; "+availability+"; "+price+"; "+(x.features[0]||"")+(x.demoOnly?"; FIKTIVES WOHNKONZEPT. Bild, Größe, Kapazität und Ausstattung sind nur Entwurfsideen; niemals als echte Unterkunft ausgeben.":"");
  });
  const context="Suchprofil: "+JSON.stringify(state.profile)+"\nAngebote: "+(candidates.length?candidates.join(" | "):"keine")+"\nAusgewählt: "+(selected?selected.name+" ("+selected.id+")":"noch keines");
  const headers={"Content-Type":"application/json"};if(window.staymateCsrf)headers["X-StayMate-CSRF"]=window.staymateCsrf;
  const response=await fetch("/api/search/chat",{method:"POST",headers,body:JSON.stringify({message,stage,context,next_question:nextQuestion})});
  if(response.status===401){document.getElementById("account-dialog")?.showModal();throw new Error("Bitte melde dich kurz an, damit deine Suche deinem Konto zugeordnet wird.");}
  if(!response.ok)throw new Error("Codex ist gerade nicht erreichbar.");
  const data=await response.json();
  if(data.model_used!==true||!data.reply)throw new Error("Codex hat keine Antwort erstellt.");
  return data;
}
function parseStayDates(value){
  const text=String(value||"");
  const iso=[...text.matchAll(/\b(20\d{2}-\d{2}-\d{2})\b/g)].map(m=>m[1]);
  if(iso.length>=2)return {checkin:iso[0],checkout:iso[1]};
  const local=[...text.matchAll(/\b(\d{1,2})[./](\d{1,2})[./](20\d{2})\b/g)].map(m=>`${m[3]}-${String(m[2]).padStart(2,"0")}-${String(m[1]).padStart(2,"0")}`);
  return local.length>=2?{checkin:local[0],checkout:local[1]}:null;
}
function parseGuestRequest(value){
  const text=String(value||"").toLowerCase();
  if(/\ballein\b|\bsolo\b/.test(text))return {guests:1,children:[]};
  if(/\bzu zweit\b|\b2 personen\b|\b2 gäste\b/.test(text))return {guests:2,children:[]};
  if(/kind|kinder/.test(text)){
    const children=[...text.matchAll(/(\d{1,2})\s*(?:jahre?|j\.?)(?:\s*alt)?/g)].map(m=>Number(m[1])).filter(n=>n<=17);
    const adults=Number(text.match(/(\d+)\s*(?:erwachsene?|adults?)/)?.[1]||0);
    return adults>0&&children.length?{guests:adults+children.length,children}:null;
  }
  const count=Number(text.match(/\b(\d{1,2})\s*(?:personen|gäste|erwachsene?)\b/)?.[1]||0);
  return count>0?{guests:count,children:[]}:null;
}
function maxNightlyBudget(value){
  const text=String(value||"").toLowerCase();
  if(/flexibel|egal|offen/.test(text))return null;
  const amounts=[...text.matchAll(/\d{2,5}/g)].map(m=>Number(m[0]));
  return amounts.length?Math.max(...amounts):null;
}
function setProviderNotice(message, citySearchUrl=null){
  const box=$("provider-notice");if(!box)return;
  box.replaceChildren();box.hidden=!message;if(!message)return;
  const text=document.createElement("span");text.textContent=message;box.append(text);
  if(citySearchUrl){const link=document.createElement("a");link.href=citySearchUrl;link.target="_blank";link.rel="noopener noreferrer";link.textContent="Echte Unterkünfte beim Anbieter ansehen";box.append(link);}
}
function bookingSearchUrl(){
  const params=new URLSearchParams({ss:state.profile.place||"Deutschland",no_rooms:"1"});
  const group=parseGuestRequest(state.profile.guests);if(group)params.set("group_adults",String(Math.max(1,group.guests-group.children.length)));
  const dates=parseStayDates(state.profile.dates);if(dates){params.set("checkin",dates.checkin);params.set("checkout",dates.checkout);}
  return "https://www.booking.com/searchresults.de.html?"+params.toString();
}
async function loadLiveProviderStatus(){
  try{
    const response=await fetch("/api/live-offers/status");if(!response.ok)return;
    const status=await response.json();liveProviderConfigured=status.configured===true;
    if(!liveProviderConfigured)setProviderNotice("Für alle Großstädte und Orte im Landkreis Böblingen gibt es auswählbare, fiktive Wohnideen mit eigenem Bild. Sie sind Musterkonzepte, keine echten Inserate oder Buchungsangebote.",bookingSearchUrl());
    else setProviderNotice("Die Live-Suche für deutsche Städte ist bereit. WohnBuddy lädt passende Anbieterangebote nach deinen Kriterien.");
  }catch{}
}
async function loadLiveOffers(){
  setProviderNotice("Suche passende Wohnideen und optionale Anbieterangebote …");
  const dates=parseStayDates(state.profile.dates),group=parseGuestRequest(state.profile.guests);
  const exactAvailability=Boolean(dates&&group);
  const payload={city:state.profile.place,type:state.profile.type||"",guests:group?.guests||2,children:group?.children||[],max_price:maxNightlyBudget(state.profile.budget)};
  if(exactAvailability){payload.checkin=dates.checkin;payload.checkout=dates.checkout;}
  let result;
  try{
    const response=await fetch("/api/live-offers/search",{method:"POST",headers:{"Content-Type":"application/json",...(window.staymateCsrf?{"X-StayMate-CSRF":window.staymateCsrf}:{})},body:JSON.stringify(payload)});
    result=await response.json();if(!response.ok)throw new Error(result.detail||"Live-Suche nicht erreichbar.");
  }catch(error){liveAvailabilityChecked=false;setProviderNotice(error.message,bookingSearchUrl());return;}
  liveProviderConfigured=result.configured===true;liveAvailabilityChecked=result.availability_checked===true;
  for(let i=catalog.length-1;i>=0;i--)if(catalog[i].id.startsWith("booking-"))catalog.splice(i,1);
  for(const offer of (result.offers||[]))catalog.push(offer);
  if(!result.configured){setProviderNotice("Ohne Live-Anbieterzugang zeigt StayMate fiktive Wohnideen und gespeicherte Anbieterinserate. Reisedaten und Verfügbarkeit sind nicht live geprüft.",bookingSearchUrl());return;}
  if(result.availability_checked){setProviderNotice(`${result.offers.length} für deine Reisedaten verfügbare Anbieterangebote in ${result.city||state.profile.place}. Verfügbarkeit vor dem Buchen erneut beim Anbieter prüfen.`,bookingSearchUrl());}
  else if(dates&&!group){setProviderNotice("Die Termine sind eingetragen, aber die Gästezahl ist nicht eindeutig. Die unten angezeigten Unterkünfte sind echte Inserate; Verfügbarkeit für diese Reise wurde noch nicht geprüft.",bookingSearchUrl());}
  else{setProviderNotice(`${result.offers.length} echte Unterkünfte in ${result.city||state.profile.place}. Ohne konkrete Reisedaten ist die Verfügbarkeit nicht geprüft.`,bookingSearchUrl());}
}
function matchListings(keepPage=false) {
  const p=state.profile,normalise=value=>String(value||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/ß/g,"ss").toLowerCase(),place=normalise(p.place),needs=normalise(`${p.needs} ${p.musthave}`);
  const parsedGroup=parseGuestRequest(p.guests),guestMatch=p.guests.match(/\d+/),guests=parsedGroup?.guests||(guestMatch?Number(guestMatch[0]):/allein|solo/i.test(p.guests)?1:/famil/i.test(p.guests)?4:2);
  const roomsMin=Number(p.size.match(/(\d+)\s*(?:zimmer|räume)/i)?.[1]||0),areaMin=Number(p.size.match(/(\d+)\s*m(?:²|2)?/i)?.[1]||0);
  const budgetMax=maxNightlyBudget(p.budget);
  const wantedType=/ferienhaus/i.test(p.type)?"house":/apartment|wohnung/i.test(p.type)&&!/beides|egal/i.test(p.type)?"apartment":"";
  const flexible=/flexibel|egal|offen/.test(place),nearby=/umgebung|region|naehe|nahe/.test(place),allGermany=/deutschland|alle staedte|ganz deutschland/.test(place),regionTokens=place.split(/[^a-z0-9]+/).filter(token=>token.length>=3);
  const countySearch=/landkreis boblingen|kreis boblingen/.test(place),stateSearch=/baden wurttemberg/.test(place);
  const sourceCatalog=catalog;
  const locationMatched=sourceCatalog.filter(item=>{
    const regions=(item.regions||[]).map(normalise);
    if(flexible||allGermany)return true;
    if(countySearch&&regions.includes("landkreis boblingen"))return true;
    if(stateSearch&&(item.demoOnly&&regions.includes("baden wurttemberg")||!item.demoOnly))return true;
    if(nearby&&place.includes("stuttgart")&&(regions.includes("landkreis boblingen")||regions.includes("stuttgart umgebung")))return true;
    return regions.some(region=>place.includes(region)||regionTokens.some(token=>token===region||region.includes(token)));
  });
  const typeMatched=locationMatched.filter(item=>{const label=normalise(item.type);const isHouse=/ferienhaus|holiday home|vacation home|cottage|villa|chalet|haus/.test(label);return !wantedType||(wantedType==="house"?isHouse:!isHouse);});
  const exactAvailabilityRequired=Boolean(parseStayDates(p.dates)&&parseGuestRequest(p.guests));
  const sized=typeMatched.filter(item=>{
    if(exactAvailabilityRequired&&!item.demoOnly&&!item.availabilityChecked)return false;
    if(!Number.isFinite(item.guests)||item.guests<guests)return false;
    if(roomsMin&&(!Number.isFinite(item.rooms)||item.rooms<roomsMin))return false;
    if(areaMin&&(!Number.isFinite(item.area)||item.area<areaMin))return false;
    if(budgetMax){
      if(item.demoOnly&&item.examplePricePerNight>budgetMax)return false;
      if(!item.demoOnly){
        if(item.priceTotal===null||item.priceTotal===undefined)return false;
        const nightlyPrice=item.nights?Number(item.priceTotal)/Number(item.nights):Number(item.priceTotal);
        if(!Number.isFinite(nightlyPrice)||nightlyPrice>budgetMax)return false;
      }
    }
    return true;
  }).map(item=>{
    if(item.sizeOptions){const variant=item.sizeOptions.find(option=>guests<=option.maxGuests)||item.sizeOptions[item.sizeOptions.length-1];return {...item,area:variant.area,rooms:variant.rooms};}
    return {...item};
  });
  let ranked=sized.map(item=>{
    let score=0;const text=`${item.location} ${item.name} ${item.description} ${item.features.join(" ")}`.toLowerCase();
    needs.split(/[ ,;]+/).filter(w=>w.length>3).forEach(word=>{if(text.includes(word))score+=2;});
    if(roomsMin&&item.rooms===roomsMin)score+=5;
    if(areaMin&&item.area>=areaMin)score+=3;
    if(budgetMax&&item.demoOnly&&item.examplePricePerNight<=budgetMax)score+=3;
    if(/natur|ruhe|see|wasser/.test(needs)&&/see|ruhig|bodensee|radolfzell|gaienhofen/i.test(text))score+=5;
    if(/stadt|kultur|zentral|öpnv/.test(needs)&&/stuttgart|konstanz|zentral|weilimdorf/i.test(text))score+=5;
    if(/wlan|arbeit|work/.test(needs)&&/arbeitsplatz/.test(text))score+=3;
    if(/park/.test(needs)&&/stellplatz|parkhaus/.test(text))score+=3;
    return {...item,score};
  }).sort((a,b)=>b.score-a.score||a.guests-b.guests);
  let relaxedMatches=false;
  if(!ranked.length){
    const fallbackPool=typeMatched.length?typeMatched:locationMatched;
    ranked=fallbackPool.map(item=>{
      const text=`${item.location} ${item.name} ${item.description} ${item.features.join(" ")}`.toLowerCase();
      let score=-Math.abs((item.guests||guests)-guests)*3;
      if(roomsMin)score-=Math.max(0,roomsMin-(item.rooms||0))*4;
      if(areaMin)score-=Math.max(0,areaMin-(item.area||0))/10;
      if(budgetMax&&Number.isFinite(item.examplePricePerNight))score-=Math.max(0,item.examplePricePerNight-budgetMax)/15;
      needs.split(/[ ,;]+/).filter(word=>word.length>3).forEach(word=>{if(text.includes(word))score+=2;});
      return {...item,score,relaxedMatch:true};
    }).sort((a,b)=>b.score-a.score||a.guests-b.guests).slice(0,6);
    relaxedMatches=ranked.length>0;
  }
  latestMatches=ranked;if(!keepPage)visibleListingCount=12;
  $("search-layout").classList.add("show-offers");
  $("match-count").textContent=ranked.length;
  $("results").hidden=true;
  $("listings").hidden=false;
  $("listings").innerHTML=ranked.length?ranked.slice(0,visibleListingCount).map((item,i)=>`<article class="listing-card ${selectedListingId===item.id?"selected-listing":""}"><div class="listing-image ${item.sourceUrl?"external-cover":"internal-cover"}">${item.image?item.imagePosition?`<div class="visualization-split ${esc(item.imagePosition)}" role="img" aria-label="${esc(item.alt)}"></div><span class="illustration-label">Visualisierung · kein Inseratsfoto</span>`:`<img src="${esc(resolveImageUrl(item.image))}" alt="${esc(item.alt)}" decoding="async"/><div class="image-fallback" role="img" aria-label="${esc(item.alt||item.name)} · fiktive Wohnidee"><span class="fallback-window"></span><span class="fallback-sofa"></span><b>Wohnidee · ${esc(item.location.split("·")[0].trim())}</b></div><span class="illustration-label">${esc(item.imageLabel||(item.sourceUrl?"Inseratsfoto":"Symbolbild"))}</span>`:`<div class="offer-cover-icon">${item.type==="Ferienhaus"?"⌂":"▦"}</div><div class="offer-cover-title"><span>${esc(item.type)}</span><b>${item.area?esc(item.area+" m²"):"Daten ansehen"}</b><small>${esc(item.sourceType)}</small></div><span class="illustration-label">Fotos beim Anbieter</span>`}<span class="match-badge">${item.id===recommendedListingId?"✦ WohnBuddy empfiehlt":i===0?"Weitere Option":"Vorschlag"}</span><button class="heart" aria-label="${esc(item.name)} merken" data-save="${item.id}">♡</button></div><div class="listing-content"><div class="listing-title"><div><span class="kicker">${esc(item.location)} · ${esc(item.type)}</span><h3>${esc(item.name)}</h3></div><span class="capacity">bis ${item.guests} Gäste</span></div><p class="description">${esc(item.description)}</p><p class="offer-dimensions">${item.rooms?`${item.rooms} Zimmer`:"Zimmerzahl nicht angegeben"}${item.area?` · ${item.area} m²`:" · Fläche nicht angegeben"}${item.guestNote?` · ${esc(item.guestNote)}`:""}</p><p class="difference-note"><b>Was hier anders ist:</b> ${esc(item.difference)}</p><div class="feature-list">${item.features.map(f=>`<span>✓ ${esc(f)}</span>`).join("")}</div>${item.layout?`<details class="floorplan"><summary>Raumaufteilung ansehen <span>Schematische Orientierung</span></summary><div class="rooms" aria-label="Schematische Raumaufteilung">${item.layout.map(room=>`<span>${esc(room)}</span>`).join("")}</div><small>Keine maßstabsgetreue Grundrisszeichnung.</small></details>`:`<p class="bed-line">Ein bestätigter Grundriss liegt nicht vor.</p>`}${item.roomTypes?.length?`<details class="floorplan"><summary>Raumtypen laut Anbieter</summary><div class="rooms">${item.roomTypes.map(room=>`<span>${esc(room)}</span>`).join("")}</div></details>`:""}<p class="availability-note">${item.demoOnly?"Nur Musteridee · keine reale Unterkunft oder Verfügbarkeit.":`Für ${esc(p.dates||"deinen Zeitraum")} ist die Verfügbarkeit nicht von StayMate geprüft.`}</p>${item.sourceUrl?`<a class="provider-link" href="${esc(item.sourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(item.sourceLabel)}</a><small class="provider-date">Inserat am ${esc(item.checked)} geprüft; Termine direkt dort prüfen.</small>`:item.demoOnly?`<a class="provider-link" href="${esc(item.searchUrl)}" target="_blank" rel="noopener noreferrer">${esc(item.searchLabel)}</a><small class="provider-date">Externe Stadtsuche · echte Angebote und Termine beim Anbieter prüfen.</small>`:`<span class="provider-link internal-source">Im StayMate-Bestand</span>`}<button class="select-listing" data-select="${item.id}">${selectedListingId===item.id?"Auswahl vorgemerkt ✓":item.demoOnly?"Wohnidee auswählen":"Dieses Objekt auswählen"}</button>${selectedListingId===item.id?`<p class="booking-note">${item.demoOnly?"Unverbindliche Wohnidee · kein Objekt gebucht":"Noch nicht gebucht · Buchung beim Anbieter bestätigen"}</p><a class="object-chat-link" href="/staymate.html?property_id=${encodeURIComponent(item.id)}">${item.demoOnly?"Wohnidee im Objekt-Chat ansehen":"Weiter zum Objekt-Chat"}</a>`:""}<button class="ask-listing" data-ask="${item.id}">Frage zu diesem Objekt stellen</button></div></article>`).join("")+(ranked.length>visibleListingCount?`<button class="load-more-listings" id="load-more-listings">Weitere ${Math.min(12,ranked.length-visibleListingCount)} von ${ranked.length-visibleListingCount} Treffern anzeigen</button>`:""):`<div class="results-empty"><div class="empty-illustration">⌕</div><h3>${!typeMatched.length?"Keine Unterkunft dieser Art gefunden":"Noch kein passendes Objekt im Bestand"}</h3><p>${!locationMatched.length?`Es gibt noch keinen Treffer für ${esc(p.place)}.`:!typeMatched.length?`Für ${esc(p.place)} sind keine passenden Unterkünfte vom Typ ${esc(p.type)} hinterlegt.`:exactAvailabilityRequired&&!sized.length?`Für ${esc(p.place)} und diese Reisedaten gibt es keine vom Anbieter bestätigten Live-Treffer. Ohne eingerichteten Partnerzugang kann StayMate die Verfügbarkeit nicht prüfen.`:`Keine Unterkunft passt zu ${esc(p.guests)} Gästen und der eingestellten Größe. Wir können die Umgebung einbeziehen oder die Suche lockern.`} Verfügbarkeit und Preis bitte beim Anbieter prüfen.</p></div>`;
  if(relaxedMatches){const notice=document.createElement("div");notice.className="results-adjustment-note";notice.setAttribute("role","status");notice.textContent="Kein Treffer erfüllt alle Suchkriterien. Hier sind die nächstliegenden Optionen im Suchgebiet. Größe, Kapazität, Unterkunftsart, Preis oder Termine können abweichen. Bitte Verfügbarkeit und Preis beim Anbieter prüfen; fiktive Wohnideen sind nicht buchbar.";$("listings").prepend(notice);}
  $("listings").querySelectorAll(".listing-card").forEach((card,index)=>{
    const item=ranked[index];if(!item)return;
    if(item.demoOnly){const title=card.querySelector(".listing-title > div");if(title){const tag=document.createElement("span");tag.className="concept-tag";tag.textContent="Fiktive Wohnidee · kein Inserat";title.prepend(tag);}}
    const capacity=card.querySelector(".capacity");if(capacity)capacity.textContent=item.demoOnly?`Beispiel: bis ${item.guests} Gäste`:item.availabilityChecked?`${item.searchedGuests} Gäste · verfügbar`:item.capacityBasis&&item.guests?`Raumangebot bis ${item.guests} Gäste`:item.guests?`bis ${item.guests} Gäste`:"Belegung beim Anbieter prüfen";
    const dimensions=card.querySelector(".offer-dimensions");if(dimensions&&item.demoOnly)dimensions.textContent=`Entwurf: ${item.rooms} Zimmer · ca. ${item.area} m²`;else if(dimensions&&item.sourceType==="Booking.com")dimensions.textContent=`${item.rooms?`${item.rooms} Schlafzimmer`:"Schlafzimmerzahl nicht angegeben"}${item.area?` · ${item.area} m²`:" · Fläche nicht angegeben"}`;
    if(item.demoOnly&&Number.isFinite(item.examplePricePerNight)){const price=document.createElement("p");price.className="offer-price sample-price";price.textContent=`ca. ${new Intl.NumberFormat("de-DE",{style:"currency",currency:"EUR"}).format(item.examplePricePerNight)} / Nacht · fiktiver Richtwert`;card.querySelector(".description")?.after(price);}
    if(item.priceTotal!==null&&item.priceTotal!==undefined){const amount=Number(item.priceTotal);if(Number.isFinite(amount)){const price=document.createElement("p");price.className="offer-price";price.textContent=`${new Intl.NumberFormat("de-DE",{style:"currency",currency:item.currency||"EUR"}).format(amount)}${item.nights?` gesamt für ${item.nights} Nächte`:""}`;card.querySelector(".description")?.after(price);}}
    const status=card.querySelector(".availability-note");if(status)status.textContent=item.demoOnly?"Nur Entwurf · kein echtes Objekt, kein Preis und keine Verfügbarkeit.":item.availabilityChecked?`Der Anbieter meldet Verfügbarkeit für ${state.profile.dates}; vor dem Buchen erneut prüfen.`:"Reisedaten nicht geprüft. Verfügbarkeit und Preis beim Anbieter ansehen.";
    const checked=card.querySelector(".provider-date");if(checked)checked.textContent=item.demoOnly?"Illustration und Beispieldaten · nicht buchbar":item.availabilityChecked?"Live-Verfügbarkeit vom Anbieter gemeldet · vor Buchung erneut prüfen":"Echtes Inserat · Reisedaten und Verfügbarkeit beim Anbieter prüfen";
    if(!item.image){const label=card.querySelector(".illustration-label");if(label)label.textContent="Kein Foto im Anbieterfeed";}
  });
  const favorites=JSON.parse(localStorage.getItem("staymate-demo-favorites")||"[]");
  $("listings").querySelectorAll(".listing-image img").forEach(img=>img.addEventListener("error",()=>{img.hidden=true;const cover=img.closest(".listing-image");cover.classList.add("image-unavailable");const fallback=cover.querySelector(".image-fallback");if(fallback)fallback.hidden=false;},{once:true}));
  $("listings").querySelectorAll("[data-save]").forEach(btn=>{if(favorites.includes(btn.dataset.save)){btn.classList.add("saved");btn.textContent="♥";}btn.addEventListener("click",()=>{btn.classList.toggle("saved");btn.textContent=btn.classList.contains("saved")?"♥":"♡";const next=JSON.parse(localStorage.getItem("staymate-demo-favorites")||"[]").filter(id=>id!==btn.dataset.save);if(btn.classList.contains("saved"))next.push(btn.dataset.save);localStorage.setItem("staymate-demo-favorites",JSON.stringify(next));if(btn.classList.contains("saved"))addBubble("Gemerkter Favorit! Er bleibt in diesem Browser gespeichert. ✨");});});
  $("listings").querySelectorAll("[data-ask]").forEach(btn=>btn.addEventListener("click",()=>{focusedListing=catalog.find(x=>x.id===btn.dataset.ask);addBubble(`Gern! Was möchtest du über ${focusedListing.name} wissen?`);showSuggestions(["WLAN", "Schlafplätze", "Parken", "Lage"]);$("message-input").focus();}));
  $("listings").querySelectorAll("[data-select]").forEach(btn=>btn.addEventListener("click",()=>selectListing(btn.dataset.select)));
  $("listings").querySelector("#load-more-listings")?.addEventListener("click",()=>{visibleListingCount+=12;matchListings(true);});
}
async function selectListing(id){
  if(isBusy)return;
  const item=catalog.find(x=>x.id===id);if(!item)return;
  isBusy=true;$("message-input").disabled=true;
  selectedListingId=id;recommendedListingId=recommendedListingId||latestMatches[0]?.id||id;focusedListing=item;state.phase="selected";
  localStorage.setItem("staymate-current-object",id);refreshObjectChatSwitch();
  matchListings();progress(state.step);
  const message=item.demoOnly?"Ich möchte die Wohnidee "+item.name+" als Inspiration auswählen.":"Ich möchte "+item.name+" für meine Reise auswählen.";
  addBubble(message,"user");
  const typing=addBubble("WohnBuddy prüft deine Auswahl …");
  try{
    const result=await askCodex(message,"recommendations",item.demoOnly?"Erkläre, dass die Auswahl nur eine fiktive Wohnidee und kein echtes Inserat ist. Nenne knapp, welche Gestaltung sie illustriert, und verweise für echte Unterkünfte auf die Stadtsuche beim Anbieter.":"Bestätige nur die unverbindliche Objektauswahl, nenne knapp den wichtigsten passenden Unterschied und erkläre, dass die Buchung erst beim Anbieter abgeschlossen wird.");
    typing.remove();addBubble(result.reply);
  }catch(error){
    typing.remove();addBubble("Codex ist gerade nicht erreichbar. Deine unverbindliche Auswahl ist vorgemerkt; ich habe keine Antwort geraten.");
  }
  matchListings();showSuggestions(["Andere Objekte ansehen","Frage zur Unterkunft","Zur Wohnungssuche"]);
  isBusy=false;$("message-input").disabled=false;$("message-input").focus();
}
async function submitAnswer(raw) {
  const answer=raw.trim();if(!answer||isBusy)return;
  await conceptCatalogPromise;
  if(state.phase==="selected"&&/^(zum objekt-chat öffnen|frage zur unterkunft)$/i.test(answer)){
    if(selectedListingId)location.href="/staymate.html?property_id="+encodeURIComponent(selectedListingId);
    return;
  }
  isBusy=true;$("message-input").disabled=true;addBubble(answer,"user");$("message-input").value="";
  const typing=addBubble("WohnBuddy denkt kurz nach …");
  let next=null,nextQuestion="",stage="gathering",showResults=false,chosenByYes=false;
  const qText=answer.toLowerCase();
  if(state.phase==="gathering"){
    if(state.step===0){state.profile.place=answer;state.step=1;next=questions[0];selectedListingId=null;recommendedListingId=null;localStorage.removeItem("staymate-current-object");refreshObjectChatSwitch();}
    else{
      const current=questions[state.step-1];state.profile[current.key]=answer;state.step++;
      if(state.step<questions.length+1)next=questions[state.step-1];
      else{state.phase="deepening";state.followupStep=0;next=followupQuestions[0];}
    }
  }else if(state.phase==="deepening"){
    const current=followupQuestions[state.followupStep];state.profile[current.key]=answer;state.followupStep++;
    if(state.followupStep<followupQuestions.length)next=followupQuestions[state.followupStep];
    else{state.phase="interim";stage="recommendations";matchListings();recommendedListingId=latestMatches[0]?.id||null;showResults=true;nextQuestion="Die Bedarfsklärung ist abgeschlossen. Empfiehl genau ein passendes Objekt aus der Liste anhand der IDs, erkläre kurz warum und frage, ob diese Empfehlung passt oder lieber eine Alternative gesucht werden soll.";}
  }else if(state.phase==="interim"){
    if(/diese empfehlung passt|empfehlung passt|das passt|ja,? passt/.test(qText)){
      if(recommendedListingId){chosenByYes=true;selectedListingId=recommendedListingId;focusedListing=catalog.find(x=>x.id===selectedListingId);state.phase="selected";localStorage.setItem("staymate-current-object",selectedListingId);stage="recommendations";nextQuestion="Bestätige kurz die unverbindliche Auswahl. Weise darauf hin, dass die Buchung noch beim Anbieter abgeschlossen wird.";}
      else{stage="refinement";nextQuestion="Erkläre kurz, dass noch kein passendes Objekt hinterlegt ist, und frage, ob eine Nachbarregion infrage kommt.";}
    }else if(/andere|alternative|noch ein wunsch|passt nicht|lieber/.test(qText)){
      state.phase="clarifying";state.clarificationStep=0;next=clarificationQuestions[0];stage="refinement";nextQuestion=next.ask;
    }else{
      state.profile.musthave=(state.profile.musthave+" "+answer).trim();state.phase="clarifying";state.clarificationStep=0;next=clarificationQuestions[0];stage="refinement";nextQuestion=next.ask;
    }
  }else if(state.phase==="clarifying"){
    const current=clarificationQuestions[state.clarificationStep];
    if(current.key==="refine_issue")state.profile.musthave=(state.profile.musthave+" "+answer).trim();
    else state.profile.needs=(state.profile.needs+" "+answer).trim();
    state.clarificationStep++;
    if(state.clarificationStep<clarificationQuestions.length){next=clarificationQuestions[state.clarificationStep];stage="refinement";}
    else{state.phase="interim";stage="recommendations";matchListings();recommendedListingId=latestMatches[0]?.id||null;showResults=true;nextQuestion="Nutze die neuen Wünsche, wähle die beste passende Objekt-ID, erkläre den Unterschied zur vorherigen Empfehlung und frage, ob diese Alternative passt.";}
  }else{
    if(/wohnungssuche|suche wechseln|andere objekte/.test(qText)){
      state.phase="clarifying";state.clarificationStep=0;selectedListingId=null;recommendedListingId=null;
      localStorage.removeItem("staymate-current-object");refreshObjectChatSwitch();
      state.profile.musthave="";next=clarificationQuestions[0];stage="refinement";matchListings();nextQuestion=next.ask;
    }else if(/noch vergleichen|alternative|andere/.test(qText)){
      state.phase="clarifying";state.clarificationStep=0;next=clarificationQuestions[0];stage="refinement";nextQuestion=next.ask;
    }else{
      stage="refinement";focusedListing=catalog.find(x=>x.id===selectedListingId)||focusedListing;
      nextQuestion="Beantworte nur mit den bestätigten Fakten zum ausgewählten Objekt. Bei offenen Buchungs-, Preis- oder Sonderwunschfragen sage, dass der Gastgeber sie bestätigen muss.";
    }
  }
  if(next){nextQuestion=next.ask;}
  if(showResults){
    await loadLiveOffers();
    matchListings();
    recommendedListingId=latestMatches[0]?.id||null;
    matchListings();
    if(latestMatches.some(item=>item.relaxedMatch))nextQuestion="Es gibt keine exakten Treffer. Stelle die aufgeführten fiktiven Wohnideen ausdrücklich als lockere Alternativen dar, nenne knapp welche Suchkriterien abweichen können, behaupte keine Verfügbarkeit und frage, ob der Gast eine davon näher ansehen oder Kriterien lockern möchte.";
    else if(!latestMatches.length)nextQuestion="Erkläre kurz, dass es für diesen Ort und diese Suchkriterien keine bestätigten passenden Live-Angebote gibt. Erfinde kein Objekt und frage, ob die Person den Umkreis erweitern oder ein Kriterium lockern möchte.";
  }
  progress(state.step);
  let result=null;
  try{
    result=await askCodex(answer,stage,nextQuestion);
    if(stage==="recommendations"&&showResults){
      const valid=new Set(latestMatches.map(item=>item.id));
      recommendedListingId=valid.has(result.recommendation_id)?result.recommendation_id:latestMatches[0]?.id||null;
      matchListings();
    }
    if(chosenByYes)matchListings();
    typing.remove();addBubble(result.reply);
  }catch(error){
    typing.remove();addBubble("Codex ist gerade nicht erreichbar. Ich habe keine Antwort erzeugt. Bitte versuche es erneut, sobald Codex verbunden ist.");
  }
  if(next){showSuggestions(next.suggestions);if(next.key==="size")showSizeChoices();}
  else if(showResults)showSuggestions(recommendedListingId?["Diese Empfehlung passt","Andere Objekte ansehen","Noch ein Wunsch"]:["Umgebung einbeziehen","Suchkriterien ändern"]);
  else if(state.phase==="selected")showSuggestions(["Zum Objekt-Chat öffnen","Andere Objekte ansehen"]);
  else if(state.phase==="interim")showSuggestions(["Diese Empfehlung passt","Andere Objekte ansehen","Noch ein Wunsch"]);
  else if(state.phase==="clarifying")showSuggestions(["Lieber größer","Zentraler gelegen","Noch ein Wunsch"]);
  if(stage==="recommendations"||stage==="refinement")$("match-panel").scrollIntoView({behavior:"smooth",block:"start"});
  isBusy=false;$("message-input").disabled=false;$("message-input").focus();
}
$("chat-form").addEventListener("submit",event=>{event.preventDefault();submitAnswer($("message-input").value);});
const savedObject=localStorage.getItem("staymate-current-object");if(catalog.some(x=>x.id===savedObject)){selectedListingId=savedObject;focusedListing=catalog.find(x=>x.id===savedObject);}refreshObjectChatSwitch();
progress(0);
showSuggestions(["Stuttgart", "Am Bodensee", "Ich bin flexibel"]);
loadLiveProviderStatus();

const dialog=$("account-dialog");
let accountMode="register", accountConfig={public_mode:false}, currentUser=null;
let saved=null;try{saved=JSON.parse(localStorage.getItem("staymate-demo-profile")||"null");}catch{}
if(saved?.name){$("account-label").textContent=saved.name.split(" ")[0];}
function setAccountMode(mode){accountMode=mode;const registering=mode==="register";$("account-title").textContent=registering?"Erstelle dein Gastkonto":"Melde dich bei StayMate an";$("account-description").textContent=registering?"Deine Chats werden deinem Konto zugeordnet.":"Melde dich mit deinem StayMate-Konto an.";$("name-label").hidden=!registering;$("name-input").hidden=!registering;$("name-input").required=registering;$("password-label").hidden=false;$("password-input").hidden=false;$("password-input").required=true;$("password-input").minLength=registering?12:1;$("password-input").autocomplete=registering?"new-password":"current-password";$("account-submit").textContent=registering?"Konto erstellen":"Anmelden";$("account-toggle").textContent=registering?"Ich habe bereits ein Konto":"Ich möchte ein Konto erstellen";$("account-toggle").hidden=false;$("account-footnote").textContent="Passwörter werden serverseitig gehasht und nicht im Browser gespeichert.";$("account-status").textContent="";}
async function loadAccountState(){try{accountConfig=await fetch("/api/auth/config").then(r=>r.json());const csrf=await fetch("/api/auth/csrf").then(r=>r.json());window.staymateCsrf=csrf.csrf_token;const state=await fetch("/api/auth/me").then(r=>r.json());currentUser=state.user||null;if(accountConfig.public_mode){setAccountMode("register");$("account-footnote").textContent="Verwende ein starkes Passwort mit mindestens 12 Zeichen.";if(currentUser){$("account-label").textContent=(currentUser.display_name||currentUser.email).split(" ")[0];$("account-logout").hidden=false;}}}catch{}}
$("account-open").addEventListener("click",()=>{if(accountConfig.public_mode)setAccountMode("register");dialog.showModal();});
$("account-toggle").addEventListener("click",()=>setAccountMode(accountMode==="register"?"login":"register"));
$("account-logout").addEventListener("click",async()=>{try{await fetch("/api/auth/logout",{method:"POST",headers:{"X-StayMate-CSRF":window.staymateCsrf}});location.reload();}catch{$("account-status").textContent="Abmelden hat nicht geklappt. Bitte erneut versuchen.";}});
$("account-form").addEventListener("submit",async event=>{event.preventDefault();const profile={name:$("name-input").value.trim(),email:$("email-input").value.trim()};if(!accountConfig.public_mode){localStorage.setItem("staymate-demo-profile",JSON.stringify(profile));$("account-label").textContent=profile.name.split(" ")[0];dialog.close();addBubble(`Schön, dass du da bist, ${profile.name.split(" ")[0]}! Dein Demo-Profil ist lokal gespeichert. ✨`);return;}const button=$("account-submit");button.disabled=true;try{const response=await fetch(`/api/auth/${accountMode}`,{method:"POST",headers:{"Content-Type":"application/json","X-StayMate-CSRF":window.staymateCsrf},body:JSON.stringify({email:profile.email,password:$("password-input").value,display_name:profile.name})}),data=await response.json();if(!response.ok)throw new Error(data.detail||"Anmeldung nicht möglich.");dialog.close();location.reload();}catch(error){$("account-status").textContent=error.message;}finally{button.disabled=false;}});
loadAccountState().then(()=>{if(new URLSearchParams(location.search).has("sign-in"))dialog.showModal();});
