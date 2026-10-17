"""PYTEST - AI 파이썬 문제 풀이 앱 (streamlit run app.py)"""

import json
from pathlib import Path
from datetime import datetime

import streamlit as st

import ai_helper
import auth
import survey
import dashboard
from learning_paths import LearningPath, Mastery, TOPIC_BY_ID

PROGRESS_FILE = Path(__file__).with_name("progress.json")

# 캐릭터 데이터
CHARACTERS = {
    "dog": {"name": "🐕 강아지", "emoji": "🐕", "color": "#D4A574"},
    "cat": {"name": "🐱 고양이", "emoji": "🐱", "color": "#FFB6C1"},
    "bird": {"name": "🐦 새", "emoji": "🐦", "color": "#87CEEB"},
    "eagle": {"name": "🦅 독수리", "emoji": "🦅", "color": "#8B4513"},
}

OUTFITS = {
    "suit": {"name": "정장", "price": 50},
    "hat": {"name": "모자", "price": 50},
    "scarf": {"name": "스카프", "price": 50},
    "glasses": {"name": "안경", "price": 50},
    "flower": {"name": "꽃 장식", "price": 100},
}

FONTS = {
    "default": {"name": "기본", "price": 0, "font_family": "Arial"},
    "comic": {"name": "만화체", "price": 50, "font_family": "'Comic Sans MS'"},
    "gothic": {"name": "고딕체", "price": 50, "font_family": "'Arial Black'"},
    "mono": {"name": "고정폭", "price": 50, "font_family": "'Courier New'"},
    "serif": {"name": "세리프", "price": 50, "font_family": "'Georgia'"},
}

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

# 배경 테마: {id: {name, price, bg_color, accent_color, text_color, description}}
BACKGROUNDS = {
    "default": {
        "name": "🌿 기본 테마",
        "price": 0,
        "bg_color": "#e6f6e6",
        "accent": "#2e7d32",
        "text": "#000",
        "description": "기본적이고 편안한 녹색 테마"
    },
    "purple": {
        "name": "💜 보라색 테마",
        "price": 200,
        "bg_color": "#f3e5f5",
        "accent": "#7b1fa2",
        "text": "#000",
        "description": "신비로운 보라색 테마"
    },
    "blue": {
        "name": "💙 하늘색 테마",
        "price": 200,
        "bg_color": "#e3f2fd",
        "accent": "#1976d2",
        "text": "#000",
        "description": "차분한 하늘색 테마"
    },
    "pink": {
        "name": "💗 핑크 테마",
        "price": 200,
        "bg_color": "#fce4ec",
        "accent": "#c2185b",
        "text": "#000",
        "description": "밝고 상큼한 핑크 테마"
    },
    "dark": {
        "name": "🌙 다크 테마",
        "price": 300,
        "bg_color": "#1a1a1a",
        "accent": "#64b5f6",
        "text": "#fff",
        "description": "눈이 편한 다크 테마"
    },
    "sunset": {
        "name": "🌅 석양 테마",
        "price": 300,
        "bg_color": "#fff3e0",
        "accent": "#e65100",
        "text": "#000",
        "description": "따뜻한 석양 테마"
    },
    "moving_slow": {
        "name": "✨ 그라데이션 (1000G)",
        "price": 1000,
        "bg_color": "#667eea",
        "accent": "#764ba2",
        "text": "#fff",
        "description": "천천히 흐르는 색상 그라데이션",
        "animation": "gradient-shift 20s ease infinite"
    },
    "moving_medium": {
        "name": "⚡ 기본 애니메이션 (2500G)",
        "price": 2500,
        "bg_color": "#f093fb",
        "accent": "#f5576c",
        "text": "#fff",
        "description": "중간 속도로 움직이는 애니메이션",
        "animation": "gradient-shift 12s ease infinite"
    },
    "moving_fast": {
        "name": "💨 고난도 애니메이션 (4000G)",
        "price": 4000,
        "bg_color": "#4facfe",
        "accent": "#00f2fe",
        "text": "#fff",
        "description": "빠르게 움직이는 고난도 애니메이션",
        "animation": "gradient-shift 8s ease infinite"
    },
    "moving_ultra": {
        "name": "🐕 캐릭터 배경 (6000G)",
        "price": 6000,
        "bg_color": "#ffd89b",
        "accent": "#ff6b6b",
        "text": "#333",
        "description": "앱 전체에서 뛰어다니는 귀여운 펫들! 귀엽고 동글동글한 강아지/고양이/새/독수리",
        "animation": "gradient-shift 10s ease infinite",
        "has_character": True
    },
}


# ---------- 진행 상황 (레벨 / 경험치) ----------

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {
        "xp": 0,
        "solved": 0,
        "history": [],
        "topic_mastery": {},
        "current_topic": None,
        "daily_problems_solved": 0,
        "last_daily_reset": None,
        "gold": 0,
        "selected_background": "default",
        "owned_backgrounds": ["default"],
        "selected_character": "dog",
        "owned_outfits": set(),
        "character_outfits": {},  # {"dog": "suit", "cat": "hat", ...}
        "selected_font": "default",
        "owned_fonts": ["default"],
    }


def save_progress(progress: dict):
    if "user" in st.session_state:
        auth.save_user_progress(st.session_state.user, progress)
    else:
        PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def check_and_reset_daily_progress(progress: dict) -> dict:
    """날짜가 바뀌었으면 일일 목표 초기화"""
    today = datetime.now().strftime("%Y-%m-%d")
    last_reset = progress.get("last_daily_reset")

    if last_reset != today:
        progress["daily_problems_solved"] = 0
        progress["last_daily_reset"] = today

    return progress


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


def update_topic_mastery(solved: bool, attempts: int, grade: int | None = None):
    """문제 풀이 결과에 따라 주제 숙련도 업데이트"""
    if not solved:
        return

    progress = st.session_state.progress
    topic_mastery = progress.get("topic_mastery", {})

    # 난이도별 추천 주제
    difficulty = st.session_state.problem["difficulty"] if st.session_state.problem else None
    if not difficulty:
        return

    # 난이도에 따른 주제 선택 (간단한 매핑)
    topic_by_difficulty = {
        "초급": ["vars_basic", "strings_lists", "if_else", "loops", "functions"],
        "중급": ["dicts_sets", "comprehension", "sorting", "string_methods", "algorithms_basics"],
        "고난도": ["recursion", "dynamic_programming", "graphs", "binary_search", "heaps", "advanced_dp"],
    }

    possible_topics = topic_by_difficulty.get(difficulty, [])
    if not possible_topics:
        return

    # 첫 번째 시도에 성공하면 INTERMEDIATE, 그 외에는 BASIC
    for topic_id in possible_topics:
        current_level = Mastery(topic_mastery.get(topic_id, Mastery.NOT_STARTED.value))

        if current_level == Mastery.NOT_STARTED:
            # 첫 풀이: 성공하면 INTERMEDIATE, 실패하면 LEARNING
            if attempts == 1:
                new_level = Mastery.INTERMEDIATE
            else:
                new_level = Mastery.LEARNING
        elif current_level == Mastery.LEARNING:
            # 재도전 성공: BASIC으로 업그레이드
            if attempts <= 3:
                new_level = Mastery.BASIC
            else:
                new_level = Mastery.LEARNING
        else:
            # 이미 완료한 수준이면 ADVANCED로 진행
            new_level = Mastery.ADVANCED

        if current_level.value < new_level.value:
            topic_mastery[topic_id] = new_level.value
            progress["topic_mastery"] = topic_mastery
            break


def add_xp(amount: int, gold: int = 100):
    if amount <= 0:
        return
    progress = st.session_state.progress
    before = level_info(progress["xp"])[0]
    progress["xp"] += amount
    progress["gold"] = progress.get("gold", 0) + gold

    # 일일 목표 진행도 저장
    progress["daily_problems_solved"] = st.session_state.get("daily_problems_solved", 0)
    progress["last_daily_reset"] = datetime.now().strftime("%Y-%m-%d")

    save_progress(progress)
    after = level_info(progress["xp"])[0]
    st.toast(f"+{amount} XP · +{gold}G 획득! 💫")
    if after > before:
        st.session_state.level_up = (after, tier_of(after)[1])

    # 일일 목표 달성
    daily_solved = st.session_state.get("daily_problems_solved", 0)
    if daily_solved == 5:
        st.session_state.daily_goal_achieved = True


def normalize_output(text: str) -> str:
    """출력값을 정규화: 공백, 줄바꿈, 대소문자 무시"""
    # 공백/줄바꿈 정규화 (여러 공백을 하나로, 빈 줄 제거)
    text = " ".join(text.split())
    return text.lower().strip()


def subjective_xp(difficulty: str, grade: int) -> int:
    # 1등급 = 100%, 9등급 = 약 11%
    return round(BASE_XP["주관식"][difficulty] * (10 - grade) / 9)


# ---------- 화면 ----------

st.set_page_config(page_title="PYTEST", page_icon="🐍", layout="centered")

auth.init_data()

# Session State 초기화
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.logged_in = False
    st.session_state.view = None
    st.session_state.progress = None
    st.session_state.daily_problems_solved = 0

# ==================== 로그인 화면 ====================
if not st.session_state.get("logged_in") or st.session_state.user is None:
    st.title("🐍 PYTEST")
    st.caption("AI가 내는 파이썬 문제를 풀고 레벨을 올리세요!")

    st.divider()

    tab_login, tab_signup = st.tabs(["🔓 로그인", "📝 회원가입"])

    with tab_login:
        st.subheader("로그인")
        login_nickname = st.text_input("닉네임", key="login_nickname")
        login_password = st.text_input("비밀번호", type="password", key="login_password")

        if st.button("로그인", type="primary", use_container_width=True):
            if login_nickname and login_password:
                if auth.verify_password(login_nickname, login_password):
                    # session_state를 먼저 모두 설정
                    st.session_state.user = login_nickname
                    progress = auth.load_user_progress(login_nickname)
                    progress = check_and_reset_daily_progress(progress)
                    st.session_state.progress = progress
                    st.session_state.daily_problems_solved = progress.get("daily_problems_solved", 0)
                    st.session_state.problem = None
                    st.session_state.titles = []

                    # 진도 설문 완료 여부 확인
                    progress_survey = survey.load_progress_survey(login_nickname)
                    if not progress_survey:
                        st.session_state.view = "progress_survey"
                    else:
                        st.session_state.view = "dashboard"

                    st.session_state.logged_in = True
                    st.success("✅ 로그인 성공!")
                    st.rerun()
                else:
                    st.error("❌ 닉네임 또는 비밀번호가 잘못되었습니다.")
            else:
                st.warning("닉네임과 비밀번호를 입력해주세요.")

    with tab_signup:
        st.subheader("회원가입")
        signup_nickname = st.text_input("닉네임", key="signup_nickname")
        signup_password = st.text_input("비밀번호", type="password", key="signup_password")
        signup_password_confirm = st.text_input("비밀번호 확인", type="password", key="signup_password_confirm")

        if st.button("회원가입", type="primary", use_container_width=True):
            if not signup_nickname or not signup_password:
                st.warning("닉네임과 비밀번호를 입력해주세요.")
            elif signup_password != signup_password_confirm:
                st.error("비밀번호가 일치하지 않습니다.")
            elif len(signup_password) < 4:
                st.error("비밀번호는 4자 이상이어야 합니다.")
            elif auth.user_exists(signup_nickname):
                st.error(f"❌ '{signup_nickname}'은 이미 사용 중인 닉네임입니다.")
            else:
                if auth.create_user(signup_nickname, signup_password):
                    st.success("✅ 회원가입 성공! 로그인해주세요.")
                    st.rerun()
                else:
                    st.error("회원가입에 실패했습니다.")

    st.stop()

# ==================== 메인 앱 ====================
if "progress" not in st.session_state:
    progress = auth.load_user_progress(st.session_state.user)
    progress = check_and_reset_daily_progress(progress)
    st.session_state.progress = progress
    st.session_state.daily_problems_solved = progress.get("daily_problems_solved", 0)
    st.session_state.problem = None
    st.session_state.titles = []
    st.session_state.view = "dashboard"  # 처음 로그인 후 대시보드 표시

progress = st.session_state.progress
level, cur_xp, need_xp = level_info(progress["xp"])
_, tier_name, bg_color, accent = tier_of(level)

# 선택된 배경 적용 (있으면 배경색 사용)
selected_bg_id = progress.get("selected_background", "default")
animation = ""
if selected_bg_id in BACKGROUNDS:
    selected_bg = BACKGROUNDS[selected_bg_id]
    bg_color = selected_bg["bg_color"]
    accent = selected_bg["accent"]
    text_color = selected_bg["text"]
    animation = selected_bg.get("animation", "")
else:
    text_color = "#000"

# 배경색 + 애니메이션 적용
animation_keyframes = ""
if animation:
    animation_keyframes = """
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    """

# 캐릭터 배경의 경우 펫 애니메이션 추가
pet_animation = ""
if selected_bg_id == "moving_ultra":
    pet_animation = """
    @keyframes float-around {
        0% { transform: translate(0, 0); }
        25% { transform: translate(100px, -50px); }
        50% { transform: translate(50px, 100px); }
        75% { transform: translate(-100px, 50px); }
        100% { transform: translate(0, 0); }
    }
    .pet {
        position: fixed;
        font-size: 3em;
        pointer-events: none;
        z-index: 0;
        animation: float-around 8s ease-in-out infinite;
    }
    """

# 선택된 글씨체
selected_font_id = progress.get("selected_font", "default")
selected_font = FONTS.get(selected_font_id, FONTS["default"])
font_family = selected_font.get("font_family", "Arial")

st.markdown(
    f"""
    <style>
    {animation_keyframes}
    {pet_animation}
    .stApp {{
        background: linear-gradient(-45deg, {bg_color}, {accent}, {bg_color});
        background-size: 400% 400%;
        {f'animation: {animation};' if animation else 'background-color: ' + bg_color + ';'}
        color: {text_color};
        font-family: {font_family};
    }}
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

# 캐릭터 배경이면 귀여운 펫 표시
if selected_bg_id == "moving_ultra":
    pet_html = """
    <div id="pet-container" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999; overflow: hidden;">
    </div>

    <svg id="dog-svg" style="display: none;" viewBox="0 0 80 80" width="100" height="100">
        <!-- 강아지: 멍청하고 귀여운 느낌 -->
        <circle cx="40" cy="45" r="25" fill="#D4A574"/>
        <circle cx="25" cy="30" r="10" fill="#D4A574"/>
        <circle cx="55" cy="30" r="10" fill="#D4A574"/>
        <circle cx="35" cy="40" r="6" fill="#000"/>
        <circle cx="45" cy="40" r="6" fill="#000"/>
        <circle cx="35" cy="39" r="2" fill="#fff"/>
        <circle cx="45" cy="39" r="2" fill="#fff"/>
        <ellipse cx="40" cy="52" rx="3" ry="5" fill="#ff69b4"/>
        <path d="M 38 55 Q 40 57 42 55" stroke="#000" stroke-width="1" fill="none"/>
    </svg>

    <svg id="cat-svg" style="display: none;" viewBox="0 0 80 80" width="100" height="100">
        <!-- 고양이: 동글동글하고 멍청한 -->
        <circle cx="40" cy="45" r="25" fill="#FFB6C1"/>
        <polygon points="30,20 40,10 50,20" fill="#FFB6C1"/>
        <polygon points="28,22 35,18 33,28" fill="#FFB6C1"/>
        <polygon points="52,22 45,18 47,28" fill="#FFB6C1"/>
        <circle cx="35" cy="40" r="6" fill="#000"/>
        <circle cx="45" cy="40" r="6" fill="#000"/>
        <circle cx="35" cy="39" r="2" fill="#fff"/>
        <circle cx="45" cy="39" r="2" fill="#fff"/>
        <line x1="25" y1="45" x2="15" y2="43" stroke="#000" stroke-width="1"/>
        <line x1="55" y1="45" x2="65" y2="43" stroke="#000" stroke-width="1"/>
    </svg>

    <svg id="bird-svg" style="display: none;" viewBox="0 0 80 80" width="100" height="100">
        <!-- 새: 작고 귀여운 -->
        <circle cx="40" cy="45" r="18" fill="#87CEEB"/>
        <circle cx="30" cy="35" r="12" fill="#87CEEB"/>
        <circle cx="28" cy="32" r="5" fill="#000"/>
        <circle cx="27" cy="31" r="2" fill="#fff"/>
        <path d="M 38 45 L 50 48 L 48 45" fill="#FFA500"/>
        <path d="M 50 50 L 55 55 L 52 55" stroke="#000" stroke-width="1" fill="none"/>
    </svg>

    <svg id="eagle-svg" style="display: none;" viewBox="0 0 80 80" width="100" height="100">
        <!-- 독수리: 듬직하지만 멍청한 느낌 -->
        <circle cx="40" cy="45" r="22" fill="#8B4513"/>
        <circle cx="25" cy="30" r="10" fill="#8B4513"/>
        <circle cx="55" cy="30" r="10" fill="#8B4513"/>
        <circle cx="32" cy="38" r="7" fill="#000"/>
        <circle cx="48" cy="38" r="7" fill="#000"/>
        <circle cx="31" cy="37" r="2" fill="#fff"/>
        <circle cx="47" cy="37" r="2" fill="#fff"/>
        <path d="M 40 52 L 35 60 L 40 58 L 45 60" fill="#FFD700"/>
    </svg>

    <script>
    class Pet {
        constructor(x, y, svgId, name) {
            this.x = x;
            this.y = y;
            this.vx = (Math.random() - 0.5) * 2;
            this.vy = (Math.random() - 0.5) * 2;
            this.svgId = svgId;
            this.name = name;
            this.element = null;
            this.createElement();
        }

        createElement() {
            const svg = document.getElementById(this.svgId);
            this.element = svg.cloneNode(true);
            this.element.style.display = "block";
            this.element.style.position = "fixed";
            this.element.style.left = this.x + "px";
            this.element.style.top = this.y + "px";
            this.element.style.pointerEvents = "none";
            this.element.style.zIndex = "9999";
            this.element.id = ""; // 복제된 요소의 ID 제거
            this.element.style.filter = "drop-shadow(0 2px 4px rgba(0,0,0,0.3))";
            document.getElementById("pet-container").appendChild(this.element);
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // 패널 충돌 (window 경계)
            const margin = 100;
            if (this.x < margin) { this.vx = Math.abs(this.vx); this.x = margin; }
            if (this.x > window.innerWidth - margin) { this.vx = -Math.abs(this.vx); this.x = window.innerWidth - margin; }
            if (this.y < margin) { this.vy = Math.abs(this.vy); this.y = margin; }
            if (this.y > window.innerHeight - margin) { this.vy = -Math.abs(this.vy); this.y = window.innerHeight - margin; }

            this.element.style.left = this.x + "px";
            this.element.style.top = this.y + "px";
        }
    }

    const pets = [
        new Pet(Math.random() * window.innerWidth, Math.random() * window.innerHeight, "dog-svg", "강아지"),
        new Pet(Math.random() * window.innerWidth, Math.random() * window.innerHeight, "cat-svg", "고양이"),
        new Pet(Math.random() * window.innerWidth, Math.random() * window.innerHeight, "bird-svg", "새"),
        new Pet(Math.random() * window.innerWidth, Math.random() * window.innerHeight, "eagle-svg", "독수리")
    ];

    function animate() {
        pets.forEach(pet => pet.update());
        requestAnimationFrame(animate);
    }

    animate();
    </script>
    """
    st.html(pet_html, unsafe_allow_html=True)

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

col1, col2, col3, col4, col5, col6 = st.columns(6)
if col1.button("🏠 홈", use_container_width=True,
               type="primary" if st.session_state.view == "dashboard" else "secondary"):
    st.session_state.view = "dashboard"
    st.rerun()
if col2.button("💻 문제 풀이", use_container_width=True,
               type="primary" if st.session_state.view == "problem" else "secondary"):
    st.session_state.view = "problem"
    st.rerun()
if col3.button("📚 학습 경로", use_container_width=True,
               type="primary" if st.session_state.view == "learning" else "secondary"):
    st.session_state.view = "learning"
    st.rerun()
if col4.button("🔨 실습", use_container_width=True,
               type="primary" if st.session_state.view == "tutorial" else "secondary"):
    st.session_state.view = "tutorial"
    st.rerun()
if col5.button("📊 설문조사", use_container_width=True,
               type="primary" if st.session_state.view == "survey" else "secondary"):
    st.session_state.view = "survey"
    st.rerun()
if col6.button("🎯 진도 설정", use_container_width=True,
               type="primary" if st.session_state.view == "progress_survey" else "secondary"):
    st.session_state.view = "progress_survey"
    st.rerun()

col_shop = st.columns([1, 5])
with col_shop[0]:
    if st.button("🛍️ 상점", use_container_width=True,
                 type="primary" if st.session_state.view == "shop" else "secondary"):
        st.session_state.view = "shop"
        st.rerun()

st.divider()

# --- 사이드바: 레벨 & 설정 ---
with st.sidebar:
    # 사용자 정보
    st.caption(f"👤 {st.session_state.user}")
    if st.button("🚪 로그아웃", use_container_width=True):
        auth.save_user_progress(st.session_state.user, st.session_state.progress)
        del st.session_state.user
        del st.session_state.progress
        del st.session_state.problem
        st.rerun()

    st.divider()

    st.markdown(f'<span class="tier-badge">{tier_name}</span>', unsafe_allow_html=True)
    st.subheader(f"Lv. {level} ✨")
    st.progress(cur_xp / need_xp, text=f"{cur_xp} / {need_xp} XP")
    st.caption(f"누적 경험치 {progress['xp']} XP · 맞힌 문제 {progress['solved']}개")

    st.divider()

    # 📊 오늘의 도전
    st.markdown("### 📊 오늘의 도전")
    daily_goal = 5
    daily_solved = st.session_state.get("daily_problems_solved", 0)
    st.progress(min(daily_solved / daily_goal, 1.0), text=f"{daily_solved}/{daily_goal} 문제")

    st.divider()

    # 💰 골드
    gold = progress.get("gold", 0)
    st.markdown(f"### 💰 골드: **{gold}G**")

    st.divider()

    st.caption("🟢 Beginner Lv.1~4 · 🟡 Student Lv.5~9 · 🔴 Expert Lv.10+")

    st.divider()

    # 학습 경로 추천
    topic_mastery = {k: Mastery(v) for k, v in progress.get("topic_mastery", {}).items()}
    recommended = LearningPath.get_recommended_next(topic_mastery, level)
    if recommended:
        st.info(f"📚 추천: **{recommended.name}**\n\n{recommended.description[:60]}...")

    st.divider()

    # 🎨 글씨체 선택
    st.markdown("### 🎨 글씨체")
    font_options = list(FONTS.keys())
    font_names = [f"{FONTS[f]['name']} ({FONTS[f]['price']}G)" for f in font_options]
    selected_font_idx = font_options.index(progress.get("selected_font", "default"))
    selected_font = st.selectbox("글씨체 선택", font_options, index=selected_font_idx,
                                 format_func=lambda x: font_names[font_options.index(x)],
                                 key="font_select")
    if selected_font != progress.get("selected_font"):
        if selected_font in progress.get("owned_fonts", ["default"]):
            progress["selected_font"] = selected_font
            save_progress(progress)
            st.rerun()
        else:
            st.warning(f"이 글씨체를 보유하지 않았습니다. (가격: {FONTS[selected_font]['price']}G)")

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
            if st.session_state.get("user"):
                st.session_state.progress = {
                    "xp": 0, "solved": 0, "history": [],
                    "topic_mastery": {}, "current_topic": None
                }
                save_progress(st.session_state.progress)
                st.rerun()

# ==================== 홈 대시보드 섹션 ====================
if st.session_state.view == "dashboard":
    dashboard.show_welcome_dashboard(st.session_state.user, st.session_state.progress)

# ==================== 학습 경로 섹션 ====================
elif st.session_state.view == "learning":
    st.header("📚 학습 경로")

    # 📊 오늘의 도전
    st.markdown("### 📊 오늘의 도전")
    daily_goal = 5
    daily_solved = st.session_state.get("daily_problems_solved", 0)
    st.progress(min(daily_solved / daily_goal, 1.0), text=f"{daily_solved}/{daily_goal} 문제")

    st.divider()

    topic_mastery = {k: Mastery(v) for k, v in progress.get("topic_mastery", {}).items()}
    stats = LearningPath.get_learning_stats(topic_mastery)

    # 전체 진행도
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("전체 주제", f"{stats['completed']}/{stats['total']}")
    col2.metric("진행률", f"{stats['completion_rate']:.0f}%")
    col3.metric("학습 중", stats['learning'])
    col4.metric("완료", stats['completed'])

    st.progress(stats['completion_rate'] / 100)

    st.divider()

    # 난이도별 모듈 표시
    difficulty_order = {"초급": 0, "중급": 1, "고난도": 2}
    all_topics = sorted(LearningPath.get_all_topics(),
                       key=lambda t: (difficulty_order.get(t.difficulty, 99), t.name))

    for difficulty in ["초급", "중급", "고난도"]:
        topics = [t for t in all_topics if t.difficulty == difficulty]
        if not topics:
            continue

        icon = "🟢" if difficulty == "초급" else "🟡" if difficulty == "중급" else "🔴"
        completed = len([t for t in topics if topic_mastery.get(t.id) != Mastery.NOT_STARTED])
        with st.expander(f"{icon} {difficulty} ({completed}/{len(topics)}):"):
            for topic in topics:
                mastery = topic_mastery.get(topic.id, Mastery.NOT_STARTED)
                unlocked = topic.is_unlocked(topic_mastery)

                # 상태 아이콘
                status_map = {
                    Mastery.NOT_STARTED: "🔒" if not unlocked else "⭕",
                    Mastery.LEARNING: "🟡",
                    Mastery.BASIC: "🟢",
                    Mastery.INTERMEDIATE: "🔵",
                    Mastery.ADVANCED: "⭐",
                }
                status = status_map.get(mastery, "⭕")

                col1, col2, col3, col4 = st.columns([0.5, 2, 1.5, 1])
                col1.write(status)
                col2.write(f"**{topic.name}**")
                col3.caption(f"예상 {topic.estimated_time}분")

                # 실습 버튼 (튜토리얼이 있을 때)
                if topic.tutorial and unlocked:
                    if col4.button("🔨 실습", key=f"learn_{topic.id}", use_container_width=True):
                        st.session_state.view = "tutorial"
                        st.session_state.selected_tutorial = topic.id
                        st.rerun()

                if not unlocked and topic.prerequisites:
                    prereq_names = [TOPIC_BY_ID[p].name for p in topic.prerequisites]
                    st.caption(f"  ✓ 요구: {', '.join(prereq_names)}")

# ==================== 문제 풀이 섹션 ====================
elif st.session_state.view == "problem":
    if st.session_state.get("daily_goal_achieved"):
        st.session_state.pop("daily_goal_achieved")
        st.snow()
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown("<div style='text-align: center; font-size: 2em; font-weight: bold; color: #ff6b6b;'>❄️ 일일 목표 달성! ❄️</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 1.2em;'>5개 문제를 모두 풀었습니다! 🎯</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 1em; color: #666;'>내일도 도전해보세요! 💪</div>", unsafe_allow_html=True)

    if st.session_state.get("level_up"):
        new_level, new_tier = st.session_state.pop("level_up")
        st.balloons()
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown("""
            <style>
            @keyframes levelUpPulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            .level-up-text {
                animation: levelUpPulse 0.6s ease-in-out;
                font-size: 2.5em;
                font-weight: bold;
                text-align: center;
            }
            </style>
            <div class="level-up-text">
            🎉 레벨 업! 🎉<br>
            <span style="color: #d32f2f; font-size: 1.2em;">Lv.{}</span>
            </div>
            """.format(new_level), unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 1.3em;'>{new_tier} 달성! 🏆</div>", unsafe_allow_html=True)

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
                st.session_state.daily_problems_solved += 1
                record("정답", xp)
                update_topic_mastery(True, current["attempts"])
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
                    st.session_state.daily_problems_solved += 1
                current["solved"] = True
                current["best_grade"] = new_best
                record(f"정답 {grading.grade}등급", gained)
                update_topic_mastery(True, current["attempts"], grading.grade)
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

# ==================== 설문조사 섹션 ====================
elif st.session_state.view == "survey":
    st.header("📊 학습 진도 설문조사")

    survey_tab1, survey_tab2, survey_tab3 = st.tabs(["📈 통계", "📝 문제 피드백", "😊 만족도 조사"])

    # 통계 탭
    with survey_tab1:
        st.subheader("📈 설문 통계")

        if "user" in st.session_state:
            stats = survey.get_statistics(st.session_state.user)

            col1, col2, col3 = st.columns(3)
            col1.metric("총 피드백 건수", stats["total_feedback"])
            col2.metric("설문 참여", stats["total_satisfaction"])
            col3.metric("평가한 주제", stats["total_topics_rated"])

            st.divider()

            if stats["total_feedback"] > 0:
                st.subheader("📋 문제 피드백 분석")
                col1, col2 = st.columns(2)

                with col1:
                    difficulty_rating = stats["avg_difficulty_rating"]
                    difficulty_label = {
                        1: "🟢 너무 쉬움",
                        2: "🟡 적당함",
                        3: "🔴 너무 어려움",
                    }.get(round(difficulty_rating), "평가 없음")
                    st.metric("평균 난이도 평가", difficulty_label)

                with col2:
                    quality_rating = stats["avg_quality_rating"]
                    st.metric("평균 품질 평가", f"{quality_rating:.1f}/4.0 ⭐")

            if stats["total_satisfaction"] > 0:
                st.divider()
                st.subheader("😊 만족도 분석")
                col1, col2, col3 = st.columns(3)

                with col1:
                    satisfaction = stats["avg_satisfaction"]
                    st.metric("전반적 만족도", f"{satisfaction:.1f}/5.0")

                with col2:
                    difficulty_app = stats["avg_difficulty_appropriateness"]
                    st.metric("난이도 적절성", f"{difficulty_app:.1f}/5.0")

                with col3:
                    ui_rating = stats["avg_ui_rating"]
                    st.metric("UI/UX 만족도", f"{ui_rating:.1f}/5.0")

    # 문제 피드백 탭
    with survey_tab2:
        st.subheader("📝 문제별 피드백 작성")

        with st.form("problem_feedback_form"):
            st.markdown("**최근에 푼 문제에 대한 의견을 알려주세요**")

            problem_title = st.text_input("문제 제목 (선택사항)")

            difficulty = st.radio(
                "문제 난이도는 어떻게 느껴졌나요?",
                options=[1, 2, 3],
                format_func=lambda x: {
                    1: "🟢 너무 쉬웠어요",
                    2: "🟡 적당했어요",
                    3: "🔴 너무 어려웠어요",
                }[x]
            )

            quality = st.radio(
                "문제 품질은 어떻게 생각하세요?",
                options=[1, 2, 3, 4],
                format_func=lambda x: {
                    1: "😞 나쁨",
                    2: "😐 보통",
                    3: "😊 좋음",
                    4: "😍 매우 좋음",
                }[x]
            )

            comment = st.text_area(
                "추가 의견 (선택사항)",
                placeholder="이 문제를 개선할 점이 있으면 알려주세요...",
                height=100
            )

            if st.form_submit_button("피드백 제출", type="primary"):
                survey.add_problem_feedback(
                    st.session_state.user,
                    problem_title or "제목 없음",
                    "선택 안함",
                    difficulty,
                    quality,
                    comment
                )
                st.success("✅ 피드백이 저장되었습니다!")

    # 만족도 조사 탭
    with survey_tab3:
        st.subheader("😊 만족도 조사")

        with st.form("satisfaction_survey_form"):
            st.markdown("**앱 사용 경험에 대한 의견을 알려주세요**")

            overall = st.radio(
                "전반적으로 이 앱이 도움이 되셨나요?",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: {1: "😞 전혀", 2: "😐 조금", 3: "😐 보통", 4: "😊 많이", 5: "😍 매우"}[x],
                horizontal=True
            )

            difficulty_level = st.radio(
                "학습 난이도가 적절했나요?",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: {1: "너무 쉬움", 2: "쉬움", 3: "적당", 4: "어려움", 5: "너무 어려움"}[x],
                horizontal=True
            )

            ui_rating = st.radio(
                "앱의 UI/UX에 만족하신가요?",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: {1: "😞 나쁨", 2: "😐 보통", 3: "😐 괜찮음", 4: "😊 좋음", 5: "😍 매우좋음"}[x],
                horizontal=True
            )

            suggestion = st.text_area(
                "개선 제안 (선택사항)",
                placeholder="이 앱을 어떻게 개선하면 좋을까요?...",
                height=100
            )

            if st.form_submit_button("조사 완료", type="primary"):
                survey.add_satisfaction_survey(
                    st.session_state.user,
                    overall,
                    difficulty_level,
                    ui_rating,
                    suggestion
                )
                st.success("✅ 소중한 의견 감사합니다! 더 나은 앱을 만들겠습니다.")
                st.balloons()

# ==================== 진도 설정 섹션 ====================
elif st.session_state.view == "progress_survey":
    st.header("🎯 학습 진도 설정")
    st.markdown("당신의 파이썬 학습 수준을 선택하면, 그에 맞게 시작 레벨을 조정해드립니다!")

    st.divider()

    progress_level = st.radio(
        "현재 파이썬 학습 수준을 선택하세요:",
        options=[
            "완전 초보 (파이썬을 처음 배워요)",
            "파이썬 기초 학습 중 (변수, 반복문 등 기초를 배우고 있어요)",
            "파이썬 기초 완료 (기초는 이해했고, 더 복잡한 코드를 배우고 싶어요)",
            "중급 학습 중 (리스트, 딕셔너리 같은 자료구조를 배우고 있어요)",
            "고급 코더 (알고리즘이나 자료구조 등 고급 주제를 배우고 싶어요)",
        ]
    )

    st.divider()

    # 각 레벨별 설명
    level_descriptions = {
        "완전 초보 (파이썬을 처음 배워요)": {
            "level": 0,
            "xp": 0,
            "mastery": {},
            "description": "변수, 자료형, 조건문, 반복문 등 기초 개념부터 시작합니다.",
        },
        "파이썬 기초 학습 중 (변수, 반복문 등 기초를 배우고 있어요)": {
            "level": 1,
            "xp": 500,
            "mastery": {
                "vars_basic": Mastery.LEARNING.value,
                "if_else": Mastery.LEARNING.value,
            },
            "description": "기초 개념을 부분적으로 알고 있으니, 그 다음 단계부터 시작합니다.",
        },
        "파이썬 기초 완료 (기초는 이해했고, 더 복잡한 코드를 배우고 싶어요)": {
            "level": 2,
            "xp": 1200,
            "mastery": {
                "vars_basic": Mastery.BASIC.value,
                "strings_lists": Mastery.BASIC.value,
                "if_else": Mastery.BASIC.value,
                "loops": Mastery.BASIC.value,
                "functions": Mastery.BASIC.value,
            },
            "description": "기초 주제는 완료했으니, 중급 주제로 진행합니다.",
        },
        "중급 학습 중 (리스트, 딕셔너리 같은 자료구조를 배우고 있어요)": {
            "level": 3,
            "xp": 2500,
            "mastery": {
                "vars_basic": Mastery.INTERMEDIATE.value,
                "strings_lists": Mastery.BASIC.value,
                "if_else": Mastery.BASIC.value,
                "loops": Mastery.BASIC.value,
                "functions": Mastery.INTERMEDIATE.value,
                "dicts_sets": Mastery.LEARNING.value,
                "comprehension": Mastery.LEARNING.value,
            },
            "description": "중급 개념을 배우고 있으니, 당신의 레벨에 맞는 문제로 시작합니다.",
        },
        "고급 코더 (알고리즘이나 자료구조 등 고급 주제를 배우고 싶어요)": {
            "level": 4,
            "xp": 4000,
            "mastery": {
                "vars_basic": Mastery.ADVANCED.value,
                "strings_lists": Mastery.INTERMEDIATE.value,
                "if_else": Mastery.INTERMEDIATE.value,
                "loops": Mastery.INTERMEDIATE.value,
                "functions": Mastery.INTERMEDIATE.value,
                "dicts_sets": Mastery.BASIC.value,
                "comprehension": Mastery.BASIC.value,
                "sorting": Mastery.LEARNING.value,
                "recursion": Mastery.LEARNING.value,
            },
            "description": "고급 알고리즘 및 자료구조 문제로 진행합니다.",
        },
    }

    selected_info = level_descriptions[progress_level]

    with st.container(border=True):
        st.markdown(f"### 📍 {progress_level}")
        st.info(selected_info["description"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("시작 레벨", selected_info["xp"])
        with col2:
            start_level, _, _ = level_info(selected_info["xp"])
            st.metric("예상 시작 등급", f"Lv. {start_level}")
        with col3:
            completed = len([v for v in selected_info["mastery"].values() if v > 0])
            st.metric("해제된 주제", f"{completed}개")

    st.divider()

    if st.button("이 진도로 시작하기", type="primary", use_container_width=True):
        # 진도 설정
        st.session_state.progress["xp"] = selected_info["xp"]
        st.session_state.progress["topic_mastery"] = selected_info["mastery"]
        save_progress(st.session_state.progress)

        # 설문 저장
        survey.save_progress_survey(st.session_state.user, {
            "level": progress_level,
            "xp": selected_info["xp"],
        })

        st.success("✅ 진도가 설정되었습니다!")
        st.session_state.view = "dashboard"
        st.rerun()

# ==================== 실습 섹션 ====================
elif st.session_state.view == "tutorial":
    st.header("🔨 실습으로 배우기")
    st.markdown("함수를 배우고, 실제 앱을 만들면서 프로그래밍 개념을 익혀봅시다!")

    st.divider()

    # 실습 가능한 주제 필터링 (초급 주제)
    topic_mastery = {k: Mastery(v) for k, v in progress.get("topic_mastery", {}).items()}
    beginner_topics = [t for t in LearningPath.get_all_topics() if t.difficulty == "초급"]

    # 주제 선택
    default_idx = 0
    if hasattr(st.session_state, 'selected_tutorial'):
        for i, t in enumerate(beginner_topics):
            if t.id == st.session_state.selected_tutorial:
                default_idx = i
                break

    selected_topic = st.selectbox(
        "📖 배우고 싶은 주제를 선택하세요",
        beginner_topics,
        index=default_idx,
        format_func=lambda t: f"{t.name} (예상 {t.estimated_time}분)",
        key="tutorial_topic_select"
    )

    # 선택 후 상태 정리
    if hasattr(st.session_state, 'selected_tutorial'):
        del st.session_state.selected_tutorial

    if not selected_topic or not selected_topic.tutorial:
        st.warning("이 주제는 아직 실습자료가 없습니다.")
        st.stop()

    tutorial = selected_topic.tutorial
    tutorial_progress = survey.get_tutorial_progress(st.session_state.user)
    current_step = tutorial_progress.get(selected_topic.id, {}).get("step_completed", 0)

    st.markdown(f"### {tutorial['title']}")
    st.info(tutorial['app_description'])

    # 진행 바
    total_steps = len(tutorial['steps'])
    st.progress(min(current_step / total_steps, 1.0) if total_steps > 0 else 0, text=f"진행률: {current_step}/{total_steps}")

    st.divider()

    # 각 스텝 렌더링
    for step_data in tutorial['steps']:
        step_num = step_data['step']
        step_type = step_data.get('type', 'lesson')
        step_title = step_data.get('title', f"Step {step_num}")
        step_key = f"{selected_topic.id}_step_{step_num}"
        is_current = step_num == current_step + 1

        with st.expander(step_title, expanded=is_current):
            if step_type == "lesson":
                st.markdown(step_data.get('content', ''))
                if 'code_example' in step_data:
                    st.markdown("**예제 코드:**")
                    st.code(step_data['code_example'], language="python")

                if is_current and st.button("✅ 이해했어요", key=f"btn_{step_key}"):
                    survey.update_tutorial_step(st.session_state.user, selected_topic.id, step_num)
                    st.success("다음 스텝으로 진행하세요!")
                    st.rerun()

            elif step_type == "practice":
                st.markdown(f"**과제:** {step_data.get('task', '')}")

                if 'hint' in step_data:
                    with st.expander("💡 힌트"):
                        st.code(step_data['hint'], language="python")

                code_input = st.text_area(
                    "코드를 작성하세요:",
                    height=200,
                    key=f"code_{step_key}",
                    placeholder="# 파이썬 코드를 여기에 작성하세요"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("실행해보기", key=f"run_{step_key}"):
                        if code_input.strip():
                            ok, output = ai_helper.run_code(code_input)
                            if ok:
                                st.success("실행 결과:")
                                st.code(output, language="text")
                            else:
                                st.error("에러가 발생했습니다:")
                                st.code(output, language="text")

                with col2:
                    if st.button("제출하기", type="primary", key=f"submit_{step_key}"):
                        if not code_input.strip():
                            st.warning("코드를 작성해주세요.")
                        else:
                            ok, output = ai_helper.run_code(code_input)
                            validation_type = step_data.get('validation', 'output_contains')
                            is_correct = False

                            if validation_type == "output_contains" and ok:
                                keywords = step_data.get('validation_keywords', [])
                                normalized_output = normalize_output(output)
                                is_correct = all(normalize_output(kw) in normalized_output for kw in keywords)

                            elif validation_type == "exact_output" and ok:
                                expected = step_data.get('expected_output', '')
                                is_correct = normalize_output(output) == normalize_output(expected)

                            if is_correct:
                                st.success("✅ 정답입니다!")
                                survey.update_tutorial_step(st.session_state.user, selected_topic.id, step_num)
                                progress["solved"] = progress.get("solved", 0) + 1
                                add_xp(10)
                                st.rerun()
                            else:
                                st.error("다시 시도해주세요.")
                                if not ok:
                                    st.code(output, language="text")

            elif step_type == "explanation":
                st.markdown(step_data.get('content', ''))

                if is_current:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ 이해했어요", key=f"understand_{step_key}"):
                            survey.update_tutorial_step(st.session_state.user, selected_topic.id, step_num)

                            if step_num >= total_steps:
                                topic_mastery = progress.get("topic_mastery", {})
                                if topic_mastery.get(selected_topic.id, 0) < Mastery.BASIC.value:
                                    topic_mastery[selected_topic.id] = Mastery.BASIC.value
                                    progress["topic_mastery"] = topic_mastery
                                    add_xp(20)
                                    st.success(f"🎉 {selected_topic.name} 튜토리얼 완료! 숙련도: BASIC")

                            st.rerun()

                    with col2:
                        if st.button("다음 주제로", key=f"next_topic_{step_key}"):
                            st.session_state.view = "learning"
                            st.rerun()

# ==================== 상점 섹션 ====================
elif st.session_state.view == "shop":
    st.header("🛍️ 상점")
    st.markdown("골드로 배경, 옷, 글씨체를 구매해보세요!")

    gold = progress.get("gold", 0)
    st.markdown(f"## 보유 골드: **{gold}G**")

    st.divider()

    # 상점 탭
    tab_bg, tab_outfit, tab_font, tab_chars = st.tabs(["🎨 배경", "👔 옷", "✍️ 글씨체", "🐕 캐릭터"])

    # ===== 배경 탭 =====
    with tab_bg:
        owned = set(progress.get("owned_backgrounds", ["default"]))
        selected = progress.get("selected_background", "default")

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📦 보유 중인 배경")
            for bg_id in owned:
                if bg_id in BACKGROUNDS:
                    bg = BACKGROUNDS[bg_id]
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if bg_id == selected:
                            st.markdown(f"✅ **{bg['name']}** (사용 중)")
                        else:
                            st.markdown(f"{bg['name']}")
                    with col2:
                        if bg_id != selected:
                            if st.button("적용", key=f"select_{bg_id}"):
                                progress["selected_background"] = bg_id
                                save_progress(progress)
                                st.success(f"{bg['name']}으로 변경되었습니다!")
                                st.rerun()

        with col_right:
            st.subheader("🆕 구매 가능한 배경")
            for bg_id, bg in BACKGROUNDS.items():
                if bg_id not in owned and bg_id != "default":
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{bg['name']}**")
                        st.caption(bg['description'])
                        st.caption(f"💰 가격: {bg['price']}G")
                    with col2:
                        if gold >= bg['price']:
                            if st.button("구매", key=f"buy_{bg_id}"):
                                progress["gold"] -= bg['price']
                                progress["owned_backgrounds"].append(bg_id)
                                save_progress(progress)
                                st.success(f"{bg['name']}을(를) 구매했습니다!")
                                st.rerun()
                        else:
                            st.button("구매", disabled=True, key=f"buy_disabled_{bg_id}")
                            st.caption(f"💬 {bg['price'] - gold}G 더 필요")

                    st.divider()

    # ===== 옷 탭 =====
    with tab_outfit:
        st.subheader("👔 캐릭터 옷")
        st.markdown("캐릭터에게 옷을 입혀주세요! (50~100G)")

        owned_outfits = progress.get("owned_outfits", [])

        for outfit_id, outfit in OUTFITS.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{outfit['name']}** 👔")
            with col2:
                st.caption(f"{outfit['price']}G")
            with col3:
                if outfit_id in owned_outfits:
                    st.markdown("✅")
                elif gold >= outfit['price']:
                    if st.button("구매", key=f"buy_outfit_{outfit_id}"):
                        progress["gold"] -= outfit['price']
                        progress["owned_outfits"].append(outfit_id)
                        save_progress(progress)
                        st.success(f"{outfit['name']}을(를) 구매했습니다!")
                        st.rerun()
                else:
                    st.button("구매", disabled=True, key=f"buy_outfit_dis_{outfit_id}")
            st.divider()

    # ===== 글씨체 탭 =====
    with tab_font:
        st.subheader("✍️ 글씨체")
        st.markdown("앱의 글씨체를 변경해보세요! (50~100G)")

        owned_fonts = progress.get("owned_fonts", ["default"])

        for font_id, font in FONTS.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{font['name']}** ✍️")
            with col2:
                st.caption(f"{font['price']}G")
            with col3:
                if font_id in owned_fonts:
                    st.markdown("✅")
                elif gold >= font['price']:
                    if st.button("구매", key=f"buy_font_{font_id}"):
                        progress["gold"] -= font['price']
                        progress["owned_fonts"].append(font_id)
                        save_progress(progress)
                        st.success(f"{font['name']}을(를) 구매했습니다!")
                        st.rerun()
                else:
                    st.button("구매", disabled=True, key=f"buy_font_dis_{font_id}")
            st.divider()

    # ===== 캐릭터 탭 =====
    with tab_chars:
        st.subheader("🐕 캐릭터 소개")
        st.markdown("**6000G 프리미엄 배경**을 구매하면 이 귀여운 펫들이 앱 전체에서 돌아다닙니다!")
        st.divider()

        # 캐릭터 설명
        char_descriptions = {
            "dog": {
                "name": "🐕 강아지",
                "personality": "명랑하고 친근한 친구",
                "description": "항상 행복해 보이는 동글동글한 강아지. 어디든 따라다니며 응원해줄 거예요!",
            },
            "cat": {
                "name": "🐱 고양이",
                "personality": "까칠하지만 귀여운 친구",
                "description": "뾰족한 귀가 매력인 고양이. 독립적이지만 속으로는 응원하고 있어요.",
            },
            "bird": {
                "name": "🐦 새",
                "personality": "작지만 씩씩한 친구",
                "description": "작은 몸에 큰 용기를 가진 새. 빠르게 날아다니며 옆에서 격려합니다!",
            },
            "eagle": {
                "name": "🦅 독수리",
                "personality": "듬직하고 강한 친구",
                "description": "우리의 안내자이자 수호자. 무엇이든 극복할 수 있도록 함께합니다.",
            },
        }

        # 각 캐릭터를 2x2 그리드로 표시
        cols = st.columns(2)
        for idx, (char_id, char_info) in enumerate(char_descriptions.items()):
            with cols[idx % 2]:
                with st.container(border=True):
                    # SVG 렌더링
                    svg_map = {
                        "dog": '<svg viewBox="0 0 80 80" width="150" height="150"><circle cx="40" cy="45" r="25" fill="#D4A574"/><circle cx="25" cy="30" r="10" fill="#D4A574"/><circle cx="55" cy="30" r="10" fill="#D4A574"/><circle cx="35" cy="40" r="6" fill="#000"/><circle cx="45" cy="40" r="6" fill="#000"/><circle cx="35" cy="39" r="2" fill="#fff"/><circle cx="45" cy="39" r="2" fill="#fff"/><ellipse cx="40" cy="52" rx="3" ry="5" fill="#ff69b4"/><path d="M 38 55 Q 40 57 42 55" stroke="#000" stroke-width="1" fill="none"/></svg>',
                        "cat": '<svg viewBox="0 0 80 80" width="150" height="150"><circle cx="40" cy="45" r="25" fill="#FFB6C1"/><polygon points="30,20 40,10 50,20" fill="#FFB6C1"/><polygon points="28,22 35,18 33,28" fill="#FFB6C1"/><polygon points="52,22 45,18 47,28" fill="#FFB6C1"/><circle cx="35" cy="40" r="6" fill="#000"/><circle cx="45" cy="40" r="6" fill="#000"/><circle cx="35" cy="39" r="2" fill="#fff"/><circle cx="45" cy="39" r="2" fill="#fff"/><line x1="25" y1="45" x2="15" y2="43" stroke="#000" stroke-width="1"/><line x1="55" y1="45" x2="65" y2="43" stroke="#000" stroke-width="1"/></svg>',
                        "bird": '<svg viewBox="0 0 80 80" width="150" height="150"><circle cx="40" cy="45" r="18" fill="#87CEEB"/><circle cx="30" cy="35" r="12" fill="#87CEEB"/><circle cx="28" cy="32" r="5" fill="#000"/><circle cx="27" cy="31" r="2" fill="#fff"/><path d="M 38 45 L 50 48 L 48 45" fill="#FFA500"/><path d="M 50 50 L 55 55 L 52 55" stroke="#000" stroke-width="1" fill="none"/></svg>',
                        "eagle": '<svg viewBox="0 0 80 80" width="150" height="150"><circle cx="40" cy="45" r="22" fill="#8B4513"/><circle cx="25" cy="30" r="10" fill="#8B4513"/><circle cx="55" cy="30" r="10" fill="#8B4513"/><circle cx="32" cy="38" r="7" fill="#000"/><circle cx="48" cy="38" r="7" fill="#000"/><circle cx="31" cy="37" r="2" fill="#fff"/><circle cx="47" cy="37" r="2" fill="#fff"/><path d="M 40 52 L 35 60 L 40 58 L 45 60" fill="#FFD700"/></svg>',
                    }
                    st.html(f'<div style="text-align: center;">{svg_map[char_id]}</div>')

                    st.markdown(f"**{char_info['name']}**")
                    st.caption(f"_{char_info['personality']}_")
                    st.markdown(char_info['description'])

                    # 구매 버튼
                    if progress.get("selected_background") == "moving_ultra":
                        st.success("✅ 6000G 프리미엄 배경 소유중!")
                    elif gold >= 6000:
                        if st.button("프리미엄 배경 구매 (6000G)", key=f"buy_premium_{char_id}"):
                            progress["gold"] -= 6000
                            progress["owned_backgrounds"].append("moving_ultra")
                            progress["selected_background"] = "moving_ultra"
                            save_progress(progress)
                            st.success("🎉 프리미엄 배경을 구매했습니다!")
                            st.rerun()
                    else:
                        st.button("프리미엄 배경 구매 (6000G)", disabled=True)
