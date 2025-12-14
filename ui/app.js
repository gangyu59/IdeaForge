const API_BASE = "http://127.0.0.1:8000";

/* =====================
   全局状态（保留 + 新增）
===================== */
let ideaId = null;
let sectionCache = {};
let currentSectionKey = null;

// Final 相关（新增，不影响原逻辑）
let finalProductDefinition = null;
let showingFinal = false;

const SECTION_LABELS = {
    product_overview: "产品概述",
    users_and_scenarios: "用户与场景",
    functional_structure: "功能结构",
    usage_flow: "使用方式",
    market_and_differentiation: "市场与差异",
    risks_and_assumptions: "风险与假设"
};

/* =====================
   页面初始化
===================== */
document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    ideaId = params.get("id");
    if (!ideaId) return;

    loadRefine(ideaId);
});

/* =====================
   加载 Section（保留原行为）
===================== */
async function loadRefine(ideaId) {
    const res = await fetch(`${API_BASE}/idea/${ideaId}/report`);
    const data = await res.json();

    sectionCache = data.sections || {};

    const listEl = document.getElementById("sectionList");
    listEl.innerHTML = "";

    Object.keys(sectionCache).forEach(key => {
        const item = document.createElement("div");
        item.className = "section-item";
        item.textContent = SECTION_LABELS[key] || key;
        item.onclick = () => selectSection(key, item);
        listEl.appendChild(item);
    });

    // ===== 原有 refine 按钮 =====
    document.getElementById("btnDeepen").onclick = () => refine("deepen");
    document.getElementById("btnChallenge").onclick = () => refine("challenge");
    document.getElementById("btnFreeze").onclick = () => refine("freeze");

    // ===== Final 按钮（新增）=====
    const btnConverge = document.getElementById("btnConverge");
    if (btnConverge) {
        btnConverge.onclick = () => onConvergeButtonClick();
    }

    // ===== Final 区按钮（新增）=====
    const btnBack = document.getElementById("btnBackToSections");
    if (btnBack) btnBack.onclick = backToSections;

    const btnPdf = document.getElementById("btnDownloadPdf");
    if (btnPdf) btnPdf.onclick = () => downloadFinal("pdf");

    const btnDocx = document.getElementById("btnDownloadDocx");
    if (btnDocx) btnDocx.onclick = () => downloadFinal("docx");

    document.getElementById("sectionContent").textContent =
        "请选择左侧一个部分";
}

/* =====================
   Section 选择（保留 + 防 Final 覆盖）
===================== */
function selectSection(sectionKey, el) {
    currentSectionKey = sectionKey;

    document.querySelectorAll(".section-item")
        .forEach(i => i.classList.remove("active"));
    el.classList.add("active");

    const sectionContentEl = document.getElementById("sectionContent");

    // ★ 确保 section 区域是可见的
    sectionContentEl.style.display = "block";

    const section = sectionCache[sectionKey];
    sectionContentEl.textContent =
        section?.content || "生成中…";
}


/* =====================
   Refine（原功能保留）
===================== */
async function refine(action) {
    if (!currentSectionKey) return;

    const contentEl = document.getElementById("sectionContent");

    contentEl.innerHTML = `
        <div class="ai-thinking">
            <div class="ai-hourglass"></div>
            <div>AI 正在思考...</div>
        </div>
    `;

    const res = await fetch(`${API_BASE}/idea/${ideaId}/refine`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            section: currentSectionKey,
            action: action
        })
    });

    const data = await res.json();
    sectionCache[currentSectionKey] = data;

    // 只在非 Final 状态下渲染
    if (!showingFinal) {
        contentEl.textContent = data.content || "";
    }
}

/* =====================
   Final 产品定义（新增，唯一入口）
===================== */
async function checkAndConverge() {
    showingFinal = true;

    const sectionEl = document.getElementById("sectionContent");
    const finalWrap = document.getElementById("finalOutput");
    const finalContentEl = document.getElementById("finalContent");

    sectionEl.style.display = "none";
    finalWrap.style.display = "block";

    // 已生成过，直接展示（留存）
    if (finalProductDefinition) {
        finalContentEl.textContent = finalProductDefinition;
        return;
    }

    finalContentEl.innerHTML = `
        <div class="ai-thinking">
            <div class="ai-hourglass"></div>
            <div>正在生成最终产品定义...</div>
        </div>
    `;

    const res = await fetch(`${API_BASE}/idea/${ideaId}/converge`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    });

    if (!res.ok) {
        finalContentEl.textContent = "生成失败";
        return;
    }

    const data = await res.json();
    finalProductDefinition = data.final_summary;
    finalContentEl.textContent = finalProductDefinition;
}

/* =====================
   返回 Section（新增）
===================== */
function backToSections() {
    showingFinal = false;

    document.getElementById("finalOutput").style.display = "none";
    document.getElementById("sectionContent").style.display = "block";

    if (currentSectionKey) {
        const section = sectionCache[currentSectionKey];
        document.getElementById("sectionContent").textContent =
            section?.content || "生成中…";
    } else {
        document.getElementById("sectionContent").textContent =
            "请选择左侧一个部分";
    }
}

function onConvergeButtonClick() {
    // 已经有最终产品定义 → 只展示
    if (finalProductDefinition) {
        showFinal();
        return;
    }

    // 还没生成过 → 生成 + 展示
    checkAndConverge();
}

function showFinal() {
    showingFinal = true;

    const finalWrap = document.getElementById("finalOutput");
    const finalContentEl = document.getElementById("finalContent");

    // ★ 只保证 Final 可见
    finalWrap.style.display = "block";

    // ★ 绝对不要动 sectionContent 的 display
    finalContentEl.textContent = finalProductDefinition || "";
}


/* =====================
   下载 Final（新增）
===================== */
function downloadFinal(format) {
    if (!finalProductDefinition) return;

    const blob = new Blob([finalProductDefinition], {
        type: "text/plain;charset=utf-8"
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");

    a.href = url;
    a.download = format === "pdf"
        ? "final_product_definition.pdf"
        : "final_product_definition.docx";

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}


function openIdea() {
    const input = document.getElementById("ideaId");
    if (!input || !input.value) {
        alert("请输入 Idea ID");
        return;
    }

    const ideaId = input.value;
    window.location.href = `idea.html?id=${ideaId}`;
}

function renderFinalDefinition(finalDef) {
    const box = document.getElementById("finalOutput");
    if (!box) return;

    if (!finalDef || !finalDef.content) {
        box.innerHTML = "<div class='muted'>尚未生成最终产品定义</div>";
        return;
    }

    box.innerHTML = `
        <div class="final-content">
            ${finalDef.content.replace(/\n/g, "<br>")}
        </div>
    `;
}
