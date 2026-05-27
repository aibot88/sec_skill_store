const translations = {
  en: {
    title: "Sec Skills Store",
    description: "A static catalog of cybersecurity-related Codex, Claude Code, and OpenClaw skills.",
    navHome: "Home",
    navExplore: "Explore Skills",
    navTrending: "Trending Now",
    navRankings: "Rankings",
    starRepo: "Star repo",
    sideCardKicker: "Open corpus",
    sideCardTitle: "Make this the map security builders star first.",
    globalSearchPlaceholder: "Search security skills, CWE, OWASP, tools",
    eyebrow: "Security Skill Intelligence",
    heroTitle: "The security skills map worth starring.",
    heroText: "Track Codex, Claude Code, OpenClaw and GitHub security skills in one searchable catalog, ranked by CWE, OWASP and practical security workflow coverage.",
    starOnGithub: "Star on GitHub",
    browseCatalog: "Browse catalog",
    viewRepository: "View repository",
    metricStars: "GitHub stars",
    metricVisitors: "site visitors",
    metricForks: "forks",
    starNote: "If this saves you one search, star it so more security builders can find it.",
    starBannerKicker: "Open security catalog",
    starBannerTitle: "Help this become the default map for agent security skills.",
    starBannerText: "A GitHub star makes the catalog easier to discover, signals which corpus should stay maintained, and helps future contributors trust the project faster.",
    marketSnapshot: "Market snapshot",
    loading: "Loading",
    liveIndex: "Live index",
    metricSkills: "skills",
    metricDownloaded: "downloaded",
    metricCwe: "CWE tags",
    metricSources: "sources",
    trendKicker: "Trending Projects",
    trendTitle: "Security coverage people can scan in seconds.",
    openRankings: "Open rankings",
    coverageBoardKicker: "CWE and OWASP",
    coverageBoardTitle: "Top Security Coverage",
    workflowBoardKicker: "Workflows",
    workflowBoardTitle: "Top Security Workflows",
    sourceBoardKicker: "Sources",
    sourceBoardTitle: "Skill Source Index",
    skillsUnit: "skills",
    searchLabel: "Search",
    searchPlaceholder: "security, CWE-89, OWASP, privacy, skill guard",
    sourceLabel: "Source",
    securityLabel: "Security Domain",
    workflowLabel: "Workflow",
    statusLabel: "Status",
    allSources: "All sources",
    allSecurity: "All security domains",
    allWorkflows: "All workflows",
    allStatuses: "All statuses",
    coverageKicker: "Coverage",
    coverageTitle: "CWE and OWASP Coverage",
    workflowKicker: "Workflows",
    workflowTitle: "Security Workflows",
    leaderboardKicker: "Leaderboard",
    loadingCatalog: "Loading catalog...",
    resetFilters: "Reset filters",
    matchingSkills: "{count} matching skills",
    sourceLink: "Source",
    downloadLink: "Download",
    localLink: "Local",
    noDescription: "No description provided.",
    unknown: "unknown",
    downloaded: "downloaded",
    partial: "partial",
    failed: "failed",
    resultNote: "Showing the first {shown} results. Refine filters to inspect the remaining {remaining}.",
    loadError: "Catalog could not be loaded",
  },
  zh: {
    title: "Sec Skills Store",
    description: "面向 Codex、Claude Code 与 OpenClaw 的网络空间安全 Skill 静态目录。",
    navHome: "首页",
    navExplore: "探索 Skills",
    navTrending: "趋势榜",
    navRankings: "排行榜",
    starRepo: "点亮 Star",
    sideCardKicker: "开放语料",
    sideCardTitle: "让它成为安全开发者首先 Star 的地图。",
    globalSearchPlaceholder: "搜索安全技能、CWE、OWASP、工具",
    eyebrow: "安全 Skill 情报",
    heroTitle: "值得点 Star 的安全 Skills 地图。",
    heroText: "把 Codex、Claude Code、OpenClaw 与 GitHub 安全技能放进一个可搜索目录，并按 CWE、OWASP 与真实安全工作流排序。",
    starOnGithub: "去 GitHub 点 Star",
    browseCatalog: "浏览目录",
    viewRepository: "查看仓库",
    metricStars: "GitHub Stars",
    metricVisitors: "网站访问人数",
    metricForks: "Forks",
    starNote: "如果它帮你少搜一次，就点个 Star，让更多安全开发者也能找到它。",
    starBannerKicker: "开放安全目录",
    starBannerTitle: "一起把它变成 Agent 安全 Skills 的默认地图。",
    starBannerText: "GitHub Star 会让目录更容易被发现，也能让后来贡献者更快判断这个项目值得维护和信任。",
    marketSnapshot: "索引概览",
    loading: "加载中",
    liveIndex: "索引已加载",
    metricSkills: "技能",
    metricDownloaded: "已下载",
    metricCwe: "CWE 标签",
    metricSources: "来源",
    trendKicker: "趋势项目",
    trendTitle: "几秒钟看懂安全覆盖重点。",
    openRankings: "打开排行榜",
    coverageBoardKicker: "CWE 与 OWASP",
    coverageBoardTitle: "热门安全覆盖",
    workflowBoardKicker: "工作流",
    workflowBoardTitle: "热门安全工作流",
    sourceBoardKicker: "来源",
    sourceBoardTitle: "Skill 来源索引",
    skillsUnit: "技能",
    searchLabel: "搜索",
    searchPlaceholder: "安全、CWE-89、OWASP、隐私、skill guard",
    sourceLabel: "来源",
    securityLabel: "安全域",
    workflowLabel: "工作流",
    statusLabel: "状态",
    allSources: "全部来源",
    allSecurity: "全部安全域",
    allWorkflows: "全部工作流",
    allStatuses: "全部状态",
    coverageKicker: "覆盖范围",
    coverageTitle: "CWE 与 OWASP 覆盖",
    workflowKicker: "工作流",
    workflowTitle: "安全业务场景",
    leaderboardKicker: "排行榜",
    loadingCatalog: "正在加载目录...",
    resetFilters: "重置筛选",
    matchingSkills: "{count} 个匹配技能",
    sourceLink: "来源",
    downloadLink: "下载",
    localLink: "本地",
    noDescription: "暂无描述。",
    unknown: "未知",
    downloaded: "已下载",
    partial: "部分",
    failed: "失败",
    resultNote: "当前显示前 {shown} 条。继续细化筛选可查看剩余 {remaining} 条。",
    loadError: "目录加载失败",
  },
};

const labelTranslations = {
  zh: {
    "Application Security": "应用安全",
    "Supply Chain": "供应链安全",
    "Secrets Management": "密钥管理",
    "Identity and Access": "身份与访问",
    "Cloud and IaC": "云与 IaC",
    "AI and Agent Security": "AI 与 Agent 安全",
    "Privacy and Data Protection": "隐私与数据保护",
    "Reverse Engineering and Malware": "逆向与恶意软件",
    "Offensive Security": "攻防与红队",
    "Detection and Response": "检测与响应",
    "Compliance": "合规",
    "Cryptography": "密码学",
    "Code Audit": "代码审计",
    "Secure Coding": "安全编码",
    "Dependency Scanning": "依赖扫描",
    "Incident Response": "应急响应",
    "Pentest and Red Team": "渗透测试与红队",
    "Binary and RE": "二进制与逆向",
    "Skill and Agent Security": "Skill 与 Agent 安全",
    "Privacy Operations": "隐私运营",
    "Cloud Security": "云安全",
    "Security Architecture": "安全架构",
  },
};

const state = {
  skills: [],
  filtered: [],
  query: "",
  source: "",
  security: "",
  business: "",
  status: "",
  lang: "en",
};

const MAX_RENDERED_CARDS = 240;
const REPO_API_URL = "https://api.github.com/repos/aibot88/sec_skill_store";
const VISITOR_COUNTER_GET_URL = "https://countapi.mileshilliard.com/api/v1/get/sec_skill_store_home";
const VISITOR_COUNTER_HIT_URL = "https://countapi.mileshilliard.com/api/v1/hit/sec_skill_store_home";
const VISITOR_COUNTED_KEY = "sec-skills-visitor-counted-v1";
const $ = (selector) => document.querySelector(selector);
const cards = $("#cards");
const template = $("#card-template");
const searchInputs = () => [$("#global-search"), $("#search")].filter(Boolean);

function t(key, params = {}) {
  const dictionary = translations[state.lang] || translations.en;
  let value = dictionary[key] || translations.en[key] || key;
  for (const [param, replacement] of Object.entries(params)) {
    value = value.replace(`{${param}}`, replacement);
  }
  return value;
}

function displayLabel(value) {
  return labelTranslations[state.lang]?.[value] || value;
}

function formatNumber(value) {
  const locale = state.lang === "zh" ? "zh-CN" : "en-US";
  return Number(value || 0).toLocaleString(locale);
}

function uniq(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => displayLabel(a).localeCompare(displayLabel(b), state.lang === "zh" ? "zh-CN" : "en-US"));
}

function countValues(items, getter) {
  const counts = new Map();
  for (const item of items) {
    const values = getter(item);
    for (const value of values) {
      counts.set(value, (counts.get(value) || 0) + 1);
    }
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || displayLabel(a[0]).localeCompare(displayLabel(b[0])));
}

function syncSearchInputs(sourceInput = null) {
  for (const input of searchInputs()) {
    if (input !== sourceInput) {
      input.value = state.query;
    }
  }
}

function fillSelect(select, label, values, selectedValue = "") {
  select.innerHTML = "";
  select.append(new Option(label, ""));
  for (const value of values) {
    select.append(new Option(displayLabel(value), value));
  }
  select.value = selectedValue;
}

function fillStatusSelect() {
  const select = $("#status-filter");
  select.innerHTML = "";
  select.append(new Option(t("allStatuses"), ""));
  for (const status of ["downloaded", "partial", "failed"]) {
    select.append(new Option(t(status), status));
  }
  select.value = state.status;
}

function applyStaticTranslations() {
  document.documentElement.lang = state.lang === "zh" ? "zh-Hans" : "en";
  document.title = t("title");
  const description = document.querySelector('meta[name="description"]');
  if (description) description.setAttribute("content", t("description"));

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.setAttribute("placeholder", t(node.dataset.i18nPlaceholder));
  });
  document.querySelectorAll(".lang-button").forEach((button) => {
    const isActive = button.dataset.lang === state.lang;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
  document.querySelectorAll("[data-link-key]").forEach((link) => {
    link.textContent = t(link.dataset.linkKey);
  });
}

function refreshSelects() {
  fillSelect($("#source-filter"), t("allSources"), uniq(state.skills.map((skill) => skill.source)), state.source);
  fillSelect($("#security-filter"), t("allSecurity"), uniq(state.skills.flatMap((skill) => skill.security_domains || [])), state.security);
  fillSelect($("#business-filter"), t("allWorkflows"), uniq(state.skills.flatMap((skill) => skill.business_domains || [])), state.business);
  fillStatusSelect();
}

function renderMetrics() {
  $("#metric-total").textContent = formatNumber(state.skills.length);
  $("#metric-downloaded").textContent = formatNumber(state.skills.filter((skill) => skill.download_status === "downloaded").length);
  $("#metric-cwe").textContent = formatNumber(uniq(state.skills.flatMap((skill) => skill.cwe || [])).length);
  $("#metric-sources").textContent = formatNumber(uniq(state.skills.map((skill) => skill.source)).length);
}

function updateText(selector, value) {
  document.querySelectorAll(selector).forEach((node) => {
    node.textContent = value;
  });
}

async function loadGithubMetrics() {
  try {
    const response = await fetch(REPO_API_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`GitHub ${response.status}`);
    const repo = await response.json();
    updateText("[data-github-stars]", formatNumber(repo.stargazers_count || 0));
    updateText("[data-github-forks]", formatNumber(repo.forks_count || 0));
  } catch (error) {
    updateText("[data-github-stars]", "0");
    updateText("[data-github-forks]", "0");
  }
}

async function loadVisitorCount() {
  try {
    const isProduction = location.hostname === "aibot88.github.io";
    const alreadyCounted = localStorage.getItem(VISITOR_COUNTED_KEY) === "1";
    const url = isProduction && !alreadyCounted ? VISITOR_COUNTER_HIT_URL : VISITOR_COUNTER_GET_URL;
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`Counter ${response.status}`);
    const payload = await response.json();
    if (isProduction && !alreadyCounted && typeof payload.value === "number") {
      localStorage.setItem(VISITOR_COUNTED_KEY, "1");
    }
    updateText("[data-site-visitors]", formatNumber(payload.value || 0));
  } catch (error) {
    updateText("[data-site-visitors]", "0");
  }
}

function renderTaxonomy() {
  const coverage = countValues(state.skills, (skill) => [...(skill.cwe || []), ...(skill.owasp || [])]).slice(0, 32);
  const workflows = countValues(state.skills, (skill) => skill.business_domains || []).slice(0, 24);

  $("#coverage-list").innerHTML = coverage.map(([name, count]) => `<span class="chip">${escapeHtml(displayLabel(name))} · ${formatNumber(count)}</span>`).join("");
  $("#workflow-list").innerHTML = workflows.map(([name, count]) => `<span class="chip">${escapeHtml(displayLabel(name))} · ${formatNumber(count)}</span>`).join("");
}

function renderRankingBoard(selector, rows, filterType) {
  const container = $(selector);
  if (!container) return;

  container.innerHTML = rows.map(([name, count], index) => `
    <button class="ranking-row" type="button" data-rank-filter="${filterType}" data-rank-value="${escapeHtml(name)}">
      <span class="ranking-index">${String(index + 1).padStart(2, "0")}</span>
      <span class="ranking-name">${escapeHtml(displayLabel(name))}</span>
      <strong>${formatNumber(count)} ${t("skillsUnit")}</strong>
    </button>
  `).join("");
}

function renderTrendBoards() {
  const coverage = countValues(state.skills, (skill) => [
    ...(skill.cwe || []),
    ...(skill.owasp || []),
    ...(skill.security_domains || []),
  ]).slice(0, 6);
  const workflows = countValues(state.skills, (skill) => skill.business_domains || []).slice(0, 6);
  const sources = countValues(state.skills, (skill) => [skill.source]).slice(0, 6);

  renderRankingBoard("#top-coverage-board", coverage, "coverage");
  renderRankingBoard("#top-workflows-board", workflows, "business");
  renderRankingBoard("#source-board", sources, "source");
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
    ...(skill.security_domains || []).map(displayLabel),
    ...(skill.business_domains || []).map(displayLabel),
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
  return `<span class="${className}">${escapeHtml(displayLabel(value))}</span>`;
}

function statusLabel(status) {
  return t(status || "unknown");
}

function renderCards() {
  cards.innerHTML = "";
  $("#results-count").textContent = t("matchingSkills", { count: formatNumber(state.filtered.length) });

  const fragment = document.createDocumentFragment();
  for (const [index, skill] of state.filtered.slice(0, MAX_RENDERED_CARDS).entries()) {
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector(".rank").textContent = `#${index + 1}`;
    node.querySelector(".source").textContent = skill.source;
    node.querySelector("h3").textContent = skill.name || skill.slug;
    node.querySelector(".confidence").textContent = `${Math.round((skill.confidence || 0) * 100)}%`;
    node.querySelector(".description").textContent = skill.description || t("noDescription");

    const statusClass = skill.download_status === "failed" ? "status-failed" : skill.download_status === "partial" ? "status-partial" : "";
    const tags = [
      tag(statusLabel(skill.download_status), statusClass),
      ...(skill.cwe || []).slice(0, 4).map((value) => tag(value)),
      ...(skill.owasp || []).slice(0, 2).map((value) => tag(value, "owasp")),
      ...(skill.security_domains || []).slice(0, 3).map((value) => tag(value)),
      ...(skill.business_domains || []).slice(0, 2).map((value) => tag(value)),
    ];
    node.querySelector(".tags").innerHTML = tags.join("");

    const sourceLink = node.querySelector(".source-link");
    sourceLink.href = skill.source_url || "#";
    sourceLink.textContent = t("sourceLink");
    sourceLink.classList.toggle("hidden", !skill.source_url);

    const downloadLink = node.querySelector(".download-link");
    downloadLink.href = skill.download_url || skill.external_source_url || "#";
    downloadLink.textContent = t("downloadLink");
    downloadLink.classList.toggle("hidden", !skill.download_url && !skill.external_source_url);

    const localLink = node.querySelector(".local-link");
    localLink.href = skill.local_path ? `../${skill.local_path}` : "#";
    localLink.textContent = t("localLink");
    localLink.classList.toggle("hidden", !skill.local_path);

    fragment.append(node);
  }
  cards.append(fragment);

  if (state.filtered.length > MAX_RENDERED_CARDS) {
    const note = document.createElement("p");
    note.className = "result-note";
    note.textContent = t("resultNote", {
      shown: formatNumber(MAX_RENDERED_CARDS),
      remaining: formatNumber(state.filtered.length - MAX_RENDERED_CARDS),
    });
    cards.append(note);
  }
}

function setLanguage(lang) {
  state.lang = lang === "zh" ? "zh" : "en";
  localStorage.setItem("sec-skills-lang", state.lang);
  applyStaticTranslations();
  refreshSelects();
  renderMetrics();
  renderTaxonomy();
  renderTrendBoards();
  applyFilters();
}

function applyBoardFilter(type, value) {
  state.query = "";
  state.source = type === "source" ? value : "";
  state.business = type === "business" ? value : "";
  state.security = "";
  state.status = "";

  if (type === "coverage") {
    const securityValues = new Set(state.skills.flatMap((skill) => skill.security_domains || []));
    if (securityValues.has(value)) {
      state.security = value;
    } else {
      state.query = value;
    }
  }

  syncSearchInputs();
  refreshSelects();
  applyFilters();
  $("#catalog")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function wireControls() {
  const handleSearch = (event) => {
    state.query = event.target.value;
    syncSearchInputs(event.target);
    applyFilters();
  };
  searchInputs().forEach((input) => input.addEventListener("input", handleSearch));
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
    syncSearchInputs();
    refreshSelects();
    applyFilters();
  });
  document.addEventListener("click", (event) => {
    const row = event.target.closest("[data-rank-filter]");
    if (!row) return;
    applyBoardFilter(row.dataset.rankFilter, row.dataset.rankValue);
  });
  document.querySelectorAll(".lang-button").forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.lang));
  });
}

async function init() {
  state.lang = localStorage.getItem("sec-skills-lang") || (navigator.language?.toLowerCase().startsWith("zh") ? "zh" : "en");
  wireControls();
  applyStaticTranslations();
  fillStatusSelect();
  loadGithubMetrics();
  loadVisitorCount();
  try {
    const response = await fetch("../data/skills.json", { cache: "no-store" });
    state.skills = await response.json();
    $("#snapshot-status").textContent = t("liveIndex");
    refreshSelects();
    renderMetrics();
    renderTaxonomy();
    renderTrendBoards();
    applyFilters();
  } catch (error) {
    $("#snapshot-status").textContent = t("failed");
    $("#results-count").textContent = t("loadError");
    cards.innerHTML = `<p class="result-note">${escapeHtml(error.message)}</p>`;
  }
}

init();
