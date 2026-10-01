"""PYTEST - AI 파이썬 문제 풀이 앱 (streamlit run app.py)"""

import json
from pathlib import Path

import streamlit as st

import ai_helper

PROGRESS_FILE = Path(__file__).with_name("progress.json")

# 문제 종류 / 난이도별 기본 경험치
BASE_XP = {
    "객관식": {"초급": 10, "중급": 20, "고난도": 35},
    "주관식": {"초급": 20, "중급": 40, "고난도": 70},
}

# 티어: (최소 레벨, 이름, 배경색, 강조색)
TIERS = [
    (10, "Expert", "#ffe5e5", "#d32f2f"),
    (5, "Student", "#fff8d6", "#f9a825"),
    (1, "Beginner", "#e6f6e6", "#2e7d32"),
]


# ---------- 진행 상황 (레벨 / 경험치) ----------

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"xp": 0, "solved": 0, "history": []}


def save_progress(progress: dict):
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def xp_needed(level: int) -> int:
    """level 에서 다음 레벨로 가기 위해 필요한 경험치."""
    return 100 + 50 * (level - 1)


def level_info(total_xp: int) -> tuple[int, int, int]:
    """(레벨, 현재 레벨에서 쌓인 경험치, 다음 레벨까지 필요한 경험치)"""
    level, xp = 1, total_xp
    while xp >= xp_needed(level):
        xp -= xp_needed(level)
        level += 1
    return level, xp, xp_needed(level)


def tier_of(level: int):
    return next(t for t in TIERS if level >= t[0])


def add_xp(amount: int):
    if amount <= 0:
        return
    progress = st.session_state.progress
    before = level_info(progress["xp"])[0]
    progress["xp"] += amount
    save_progress(progress)
    after = level_info(progress["xp"])[0]
    st.toast(f"+{amount} XP")
    if after > before:
        st.session_state.level_up = (after, tier_of(after)[1])


def subjective_xp(difficulty: str, grade: int) -> int:
    # 1등급 = 100%, 9등급 = 약 11%
    return round(BASE_XP["주관식"][difficulty] * (10 - grade) / 9)


# ---------- 화면 ----------

st.set_page_config(page_title="PYTEST", page_icon="🐍", layout="centered")

if "progress" not in st.session_state:
    st.session_state.progress = load_progress()
    st.session_state.problem = None
    st.session_state.titles = []

progress = st.session_state.progress
level, cur_xp, need_xp = level_info(progress["xp"])
_, tier_name, bg_color, accent = tier_of(level)

# 티어별 배경색 (Beginner 초록 / Student 노랑 / Expert 빨강)
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    .tier-badge {{
        display: inline-block; padding: 4px 14px; border-radius: 999px;
        background: {accent}; color: white; font-weight: 700; letter-spacing: .5px;
    }}
    .expected {{ border-left: 5px solid {accent}; }}
    /* 복사 방지: 코드 블록 선택 금지 + 복사 버튼 숨김 */
    [data-testid="stCode"] {{ user-select: none; -webkit-user-select: none; }}
    [data-testid="stCode"] button {{ display: none !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 복사/붙여넣기 방지: copy, cut, paste, 드래그 앤 드롭, 우클릭 메뉴를 막는다.
st.html(
    """
    <script>
    if (!window.__noCopyPaste) {
      window.__noCopyPaste = true;
      const notify = (msg) => {
        let box = document.getElementById("no-copy-paste-msg");
        if (!box) {
          box = document.createElement("div");
          box.id = "no-copy-paste-msg";
          box.style.cssText = "position:fixed;bottom:24px;left:50%;transform:translateX(-50%);"
            + "background:#333;color:#fff;padding:10px 18px;border-radius:8px;z-index:99999;"
            + "font-size:14px;transition:opacity .3s;";
          document.body.appendChild(box);
        }
        box.textContent = msg;
        box.style.opacity = "1";
        clearTimeout(window.__noCopyPasteTimer);
        window.__noCopyPasteTimer = setTimeout(() => (box.style.opacity = "0"), 1500);
      };
      const block = (msg) => (e) => { e.preventDefault(); e.stopPropagation(); notify(msg); };
      document.addEventListener("copy", block("🚫 복사할 수 없어요. 직접 타이핑해 주세요!"), true);
      document.addEventListener("cut", block("🚫 잘라내기를 할 수 없어요."), true);
      document.addEventListener("paste", block("🚫 붙여넣기를 할 수 없어요. 직접 타이핑해 주세요!"), true);
      document.addEventListener("drop", block("🚫 끌어다 놓기를 할 수 없어요."), true);
      document.addEventListener("contextmenu", (e) => e.preventDefault(), true);
    }
    </script>
    """,
    unsafe_allow_javascript=True,
)

st.title("🐍 PYTEST")
st.caption("AI가 내는 파이썬 문제를 풀고 레벨을 올리세요!")

# --- 사이드바: 레벨 & 설정 ---
with st.sidebar:
    st.markdown(f'<span class="tier-badge">{tier_name}</span>', unsafe_allow_html=True)
    st.subheader(f"Lv. {level}")
    st.progress(cur_xp / need_xp, text=f"{cur_xp} / {need_xp} XP")
    st.caption(f"누적 경험치 {progress['xp']} XP · 맞힌 문제 {progress['solved']}개")
    st.caption("🟢 Beginner Lv.1~4 · 🟡 Student Lv.5~9 · 🔴 Expert Lv.10+")

    st.divider()
    kind = st.radio("문제 종류", ["객관식", "주관식"], horizontal=True)
    difficulty = st.radio("난이도", ["초급", "중급", "고난도"], horizontal=True)
    st.caption(f"기본 경험치: {BASE_XP[kind][difficulty]} XP")

    if st.button("새 문제 출제", type="primary", use_container_width=True):
        with st.spinner("AI가 문제를 만드는 중..."):
            try:
                problem = ai_helper.generate_problem(kind, difficulty, st.session_state.titles)
            except Exception as e:
                st.error(f"문제 생성 실패: {e}")
            else:
                st.session_state.titles.append(problem.title)
                st.session_state.problem = {
                    "kind": kind, "difficulty": difficulty, "data": problem,
                    "attempts": 0, "solved": False, "best_grade": None, "result": None,
                }

    with st.expander("진행 상황 초기화"):
        if st.button("레벨/경험치 초기화"):
            st.session_state.progress = {"xp": 0, "solved": 0, "history": []}
            save_progress(st.session_state.progress)
            st.rerun()

if st.session_state.get("level_up"):
    new_level, new_tier = st.session_state.pop("level_up")
    st.balloons()
    st.success(f"🎉 레벨 업! Lv.{new_level} ({new_tier})")

current = st.session_state.problem
if current is None:
    st.info("왼쪽에서 문제 종류와 난이도를 고르고 **새 문제 출제**를 눌러 주세요.")
    st.stop()

p = current["data"]
st.subheader(f"[{current['kind']} · {current['difficulty']}] {p.title}")
st.write(p.situation)
st.markdown("**목표 출력 (이 결과가 나오면 정답)**")
st.code(p.expected_output, language="text")


def record(result: str, xp: int):
    progress["history"].append({
        "title": p.title, "kind": current["kind"], "difficulty": current["difficulty"],
        "result": result, "xp": xp,
    })
    save_progress(progress)


def code_lines(code: str) -> list[str]:
    """따라 적기 비교용: 탭을 공백으로 바꾸고, 줄 끝 공백과 빈 줄은 무시한다."""
    return [line.replace("\t", "    ").rstrip() for line in code.splitlines() if line.strip()]


def first_mismatch(typed: str, target: str) -> int | None:
    """처음으로 다른 줄 번호(1부터)를 돌려준다. 똑같으면 None, 덜 적었으면 -1."""
    typed_lines, target_lines = code_lines(typed), code_lines(target)
    for i, (a, b) in enumerate(zip(typed_lines, target_lines), start=1):
        if a != b:
            return i
    if len(typed_lines) < len(target_lines):
        return -1
    if len(typed_lines) > len(target_lines):
        return len(target_lines) + 1
    return None


def start_copy(target: str):
    current["mode"] = "copy"
    current["copy_target"] = target
    st.rerun()


# ---------- 객관식 ----------
if current["kind"] == "객관식":
    st.markdown("**아래 코드 중 목표 출력을 만드는 것을 고르세요.**")
    labels = ["①", "②", "③", "④"]
    for label, code in zip(labels, p.choices):
        st.markdown(label)
        st.code(code, language="python")

    choice = st.radio("정답 선택", labels[: len(p.choices)], horizontal=True,
                      disabled=current["solved"], key=f"mc_{p.title}")

    if st.button("제출", disabled=current["solved"]):
        current["attempts"] += 1
        idx = labels.index(choice)
        if idx == p.answer_index:
            current["solved"] = True
            base = BASE_XP["객관식"][current["difficulty"]]
            xp = base if current["attempts"] == 1 else base // 2  # 재도전 정답은 절반
            progress["solved"] += 1
            record("정답", xp)
            add_xp(xp)
            current["result"] = ("success", f"정답입니다! (+{xp} XP)")
        else:
            ok, out = ai_helper.run_code(p.choices[idx])
            current["result"] = ("error", "오답입니다. 선택한 코드의 실제 실행 결과를 보고 다시 풀어 보세요.\n\n"
                                          f"```\n{out.strip() if ok else out}\n```")
        st.rerun()

    if current["result"]:
        level_type, msg = current["result"]
        getattr(st, level_type)(msg)
    if current["solved"]:
        with st.expander("해설 보기", expanded=True):
            st.write(p.explanation)

# ---------- 주관식 ----------
else:
    st.markdown("**입력 데이터** (코드에 그대로 사용하세요)")
    st.code(p.input_description, language="python")

    current.setdefault("mode", "solve")   # solve: 풀이 / copy: 답안 따라 적기
    current.setdefault("round", 0)        # 재풀이 횟수 (편집기 초기화용)
    current.setdefault("copied_answer", False)

    # --- 재풀이 1단계: 답안 따라 적기 ---
    if current["mode"] == "copy":
        target = current["copy_target"]
        st.markdown("### ✍️ 재풀이 1단계: 답안 따라 적기")
        st.caption("아래 코드를 직접 타이핑해서 똑같이 적어 보세요. (줄 끝 공백과 빈 줄은 무시합니다) "
                   "다 적으면 답안이 사라지고, 기억을 떠올려 처음부터 다시 풀게 됩니다.")
        st.code(target, language="python")
        typed = st.text_area("따라 적기", height=280, key=f"copy_{p.title}_{current['round']}")

        if st.button("따라 적기 완료", type="primary", use_container_width=True):
            line = first_mismatch(typed, target)
            if line is None:
                current["mode"] = "solve"
                current["round"] += 1
                current["result"] = None
                st.rerun()
            elif line == -1:
                st.warning("아직 다 적지 않았어요. 끝까지 적어 주세요.")
            else:
                st.warning(f"{line}번째 줄이 답안과 달라요. 다시 확인해 보세요.")
        st.stop()

    if current["round"] > 0 and not current["result"]:
        st.info("✍️ 재풀이 2단계: 이제 답안 없이 처음부터 다시 풀어 보세요!")

    code = st.text_area("내 코드", height=280, key=f"code_{p.title}_{current['round']}",
                        placeholder="# 여기에 파이썬 코드를 작성하세요. 결과는 print 로 출력합니다.")

    col1, col2 = st.columns(2)
    run_clicked = col1.button("실행만 해보기", use_container_width=True)
    submit_clicked = col2.button("제출 (채점)", type="primary", use_container_width=True)

    if run_clicked and code.strip():
        ok, out = ai_helper.run_code(code)
        st.code(out if out else "(출력 없음)", language="text")

    if submit_clicked and code.strip():
        current["attempts"] += 1
        ok, out = ai_helper.run_code(code)
        if ok and ai_helper.outputs_match(out, p.expected_output):
            with st.spinner("AI가 효율성을 채점하는 중..."):
                grading = ai_helper.grade_solution(p, code)
            prev_best = current["best_grade"]
            prev_xp = subjective_xp(current["difficulty"], prev_best) if prev_best else 0
            new_best = min(grading.grade, prev_best) if prev_best else grading.grade
            gained = subjective_xp(current["difficulty"], new_best) - prev_xp  # 등급이 오른 만큼만 추가
            if current["copied_answer"] and not current["solved"]:
                gained //= 2  # 모범 답안을 보고 따라 적은 뒤 맞힌 경우 절반
            if not current["solved"]:
                progress["solved"] += 1
            current["solved"] = True
            current["best_grade"] = new_best
            record(f"정답 {grading.grade}등급", gained)
            add_xp(gained)
            current["result"] = ("correct", grading, gained)
        else:
            actual = out if ok else f"[에러]\n{out}"
            with st.spinner("AI가 오답 원인을 분석하는 중..."):
                fb = ai_helper.explain_wrong(p, code, actual)
            current["result"] = ("wrong", fb, actual)
        st.rerun()

    result = current["result"]
    if result and result[0] == "correct":
        _, g, gained = result
        st.success(f"정답입니다! 효율성 **{g.grade}등급** (1등급이 최고) · +{gained} XP")
        st.metric("시간 복잡도", g.time_complexity)
        st.markdown("#### 📝 AI 피드백")
        st.write(g.feedback)
        st.markdown("#### 🚀 더 효율적인 방법")
        st.write(g.better_approach)
        st.code(g.better_code, language="python")
        if g.grade > 1:
            st.info("위의 개선 코드를 따라 적은 뒤 다시 풀어서 더 높은 등급에 도전해 보세요. "
                    "등급이 오르면 차이만큼 경험치를 더 받습니다.")
            if st.button("✍️ 재풀이 (개선 코드 따라 적기)", type="primary", use_container_width=True):
                start_copy(g.better_code)
    elif result and result[0] == "wrong":
        _, fb, actual = result
        st.error("오답입니다. 실행 결과가 목표 출력과 다릅니다.")
        st.code(actual, language="text")
        st.markdown("#### 🔍 왜 틀렸을까?")
        st.write(fb.reason)
        st.markdown("#### 💡 힌트")
        st.write(fb.hint)
        st.info("힌트를 보고 바로 고쳐서 다시 제출하거나, 모범 답안을 따라 적은 뒤 처음부터 다시 풀 수 있어요. "
                "(모범 답안을 본 뒤 맞히면 경험치 절반)")
        if st.button("✍️ 재풀이 (모범 답안 따라 적기)", type="primary", use_container_width=True):
            current["copied_answer"] = True
            start_copy(p.reference_solution)
