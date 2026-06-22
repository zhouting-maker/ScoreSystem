const problemEl = document.getElementById("problem");
const solveBtn = document.getElementById("solve-btn");
const reasoningEl = document.getElementById("reasoning");
const answerEl = document.getElementById("answer");

let currentSource = null;

function reset() {
  reasoningEl.textContent = "";
  answerEl.textContent = "";
}

function renderMath() {
  if (window.MathJax && window.MathJax.typesetPromise) {
    window.MathJax.typesetPromise([reasoningEl, answerEl]).catch(() => {});
  }
}

function setBusy(busy) {
  solveBtn.disabled = busy;
  solveBtn.textContent = busy ? "解题中…" : "开始解题";
}

function solve() {
  const problem = problemEl.value.trim();
  if (!problem) {
    problemEl.focus();
    return;
  }

  if (currentSource) currentSource.close();
  reset();
  setBusy(true);

  const url = "/api/solve/stream?problem=" + encodeURIComponent(problem);
  const source = new EventSource(url);
  currentSource = source;

  source.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "reasoning") {
      reasoningEl.textContent += data.text;
    } else if (data.type === "answer") {
      answerEl.textContent += data.text;
    } else if (data.type === "error") {
      answerEl.textContent += "\n[错误] " + data.text;
    } else if (data.type === "done") {
      source.close();
      currentSource = null;
      setBusy(false);
      renderMath();
    }
  };

  source.onerror = () => {
    source.close();
    currentSource = null;
    setBusy(false);
    renderMath();
  };
}

solveBtn.addEventListener("click", solve);
problemEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) solve();
});
