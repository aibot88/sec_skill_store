const state = {
  skills: [],
  filtered: [],
  query: "",
  source: "",
  security: "",
  business: "",
  status: "",
};

const $ = (selector) => document.querySelector(selector);
const cards = $("#cards");
const template = $("#card-template");

const repoBase = "https://github.com/aibot88/sec_skill_store/blob/main/";

function uniq(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b));
}

function countValues(items, getter) {
  const counts = new Map();
  for (const item of items) {
    const values = getter(item);
    for (const value of values) {
      counts.set(value, (counts.get(value) || 0) + 1);
    }
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
}

function fillSelect(select, label, values) {
  select.innerHTML = "";
  select.append(new Option(label, ""));
  for (const value of values) {
    select.append(new Option(value, value));
  }
}

function renderMetrics() {
  $("#metric-total").textContent = state.skills.length.toLocaleString();
  $("#metric-downloaded").textContent = state.skills.filter((skill) => skill.download_status === "downloaded").length.toLocaleString();
  $("#metric-cwe").textContent = uniq(state.skills.flatMap((skill) => skill.cwe || [])).length.toLocaleString();
  $("#metric-sources").textContent = uniq(state.skills.map((skill) => skill.source)).length.toLocaleString();
}

function renderTaxonomy() {
  const coverage = countValues(state.skills, (skill) => [...(skill.cwe || []), ...(skill.owasp || [])]).slice(0, 32);
  const workflows = countValues(state.skills, (skill) => skill.business_domains || []).slice(0, 24);

  $("#coverage-list").innerHTML = coverage.map(([name, count]) => `<span class="chip">${escapeHtml(name)} · ${count}</span>`).join("");
  $("#workflow-list").innerHTML = workflows.map(([name, count]) => `<span class="chip">${escapeHtml(name)} · ${count}</span>`).join("");
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function searchableText(skill) {
  return [
    skill.name,
    skill.slug,
    skill.description,
    skill.source,
    skill.category,
    skill.license,
    ...(skill.cwe || []),
    ...(skill.owasp || []),
    ...(skill.security_domains || []),
    ...(skill.business_domains || []),
  ].join(" ").toLowerCase();
}

function applyFilters() {
  const query = state.query.trim().toLowerCase();
  state.filtered = state.skills.filter((skill) => {
    if (query && !searchableText(skill).includes(query)) return false;
    if (state.source && skill.source !== state.source) return false;
    if (state.security && !(skill.security_domains || []).includes(state.security)) return false;
    if (state.business && !(skill.business_domains || []).includes(state.business)) return false;
    if (state.status && skill.download_status !== state.status) return false;
    return true;
  });
  renderCards();
}

function tag(value, className = "") {
  return `<span class="${className}">${escapeHtml(value)}</span>`;
}

function renderCards() {
  cards.innerHTML = "";
  $("#results-count").textContent = `${state.filtered.length.toLocaleString()} matching skills`;

  const fragment = document.createDocumentFragment();
  for (const skill of state.filtered.slice(0, 240)) {
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector(".source").textContent = skill.source;
    node.querySelector("h3").textContent = skill.name || skill.slug;
    node.querySelector(".confidence").textContent = `${Math.round((skill.confidence || 0) * 100)}%`;
    node.querySelector(".description").textContent = skill.description || "No description provided.";

    const statusClass = skill.download_status === "failed" ? "status-failed" : skill.download_status === "partial" ? "status-partial" : "";
    const tags = [
      tag(skill.download_status || "unknown", statusClass),
      ...(skill.cwe || []).slice(0, 4).map((value) => tag(value)),
      ...(skill.owasp || []).slice(0, 2).map((value) => tag(value, "owasp")),
      ...(skill.security_domains || []).slice(0, 3).map((value) => tag(value)),
      ...(skill.business_domains || []).slice(0, 2).map((value) => tag(value)),
    ];
    node.querySelector(".tags").innerHTML = tags.join("");

    const sourceLink = node.querySelector(".source-link");
    sourceLink.href = skill.source_url || "#";
    sourceLink.classList.toggle("hidden", !skill.source_url);

    const downloadLink = node.querySelector(".download-link");
    downloadLink.href = skill.download_url || skill.external_source_url || "#";
    downloadLink.classList.toggle("hidden", !skill.download_url && !skill.external_source_url);

    const localLink = node.querySelector(".local-link");
    localLink.href = skill.local_path ? `../${skill.local_path}` : "#";
    localLink.classList.toggle("hidden", !skill.local_path);

    fragment.append(node);
  }
  cards.append(fragment);

  if (state.filtered.length > 240) {
    const note = document.createElement("p");
    note.className = "description";
    note.textContent = `Showing the first 240 results. Refine filters to inspect the remaining ${(state.filtered.length - 240).toLocaleString()}.`;
    cards.append(note);
  }
}

function wireControls() {
  $("#search").addEventListener("input", (event) => {
    state.query = event.target.value;
    applyFilters();
  });
  $("#source-filter").addEventListener("change", (event) => {
    state.source = event.target.value;
    applyFilters();
  });
  $("#security-filter").addEventListener("change", (event) => {
    state.security = event.target.value;
    applyFilters();
  });
  $("#business-filter").addEventListener("change", (event) => {
    state.business = event.target.value;
    applyFilters();
  });
  $("#status-filter").addEventListener("change", (event) => {
    state.status = event.target.value;
    applyFilters();
  });
  $("#reset").addEventListener("click", () => {
    state.query = "";
    state.source = "";
    state.security = "";
    state.business = "";
    state.status = "";
    $("#search").value = "";
    $("#source-filter").value = "";
    $("#security-filter").value = "";
    $("#business-filter").value = "";
    $("#status-filter").value = "";
    applyFilters();
  });
}

async function init() {
  wireControls();
  try {
    const response = await fetch("../data/skills.json", { cache: "no-store" });
    state.skills = await response.json();
    fillSelect($("#source-filter"), "All sources", uniq(state.skills.map((skill) => skill.source)));
    fillSelect($("#security-filter"), "All security domains", uniq(state.skills.flatMap((skill) => skill.security_domains || [])));
    fillSelect($("#business-filter"), "All workflows", uniq(state.skills.flatMap((skill) => skill.business_domains || [])));
    renderMetrics();
    renderTaxonomy();
    applyFilters();
  } catch (error) {
    $("#results-count").textContent = "Catalog could not be loaded";
    cards.innerHTML = `<p class="description">${escapeHtml(error.message)}</p>`;
  }
}

init();
