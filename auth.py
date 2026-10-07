"""사용자 인증 및 데이터 관리"""

import json
import hashlib
from pathlib import Path
from datetime import datetime


USERS_FILE = Path(__file__).with_name("users.json")
USER_DATA_DIR = Path(__file__).with_name("user_data")


def init_data():
    """디렉토리 초기화"""
    USER_DATA_DIR.mkdir(exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text(json.dumps({}, ensure_ascii=False, indent=2), encoding="utf-8")


def hash_password(password: str) -> str:
    """비밀번호 해시화"""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> dict:
    """모든 사용자 정보 로드"""
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    return {}


def save_users(users: dict):
    """사용자 정보 저장"""
    USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")


def user_exists(nickname: str) -> bool:
    """사용자 존재 여부"""
    users = load_users()
    return nickname.lower() in {k.lower() for k in users.keys()}


def create_user(nickname: str, password: str, is_host: bool = False) -> bool:
    """새 사용자 생성"""
    if user_exists(nickname):
        return False

    users = load_users()
    users[nickname] = {
        "password_hash": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "is_host": is_host,
    }
    save_users(users)

    # 사용자 디렉토리 생성
    (USER_DATA_DIR / nickname).mkdir(exist_ok=True)

    return True


def is_host(nickname: str) -> bool:
    """호스트(강사) 여부 확인"""
    users = load_users()
    for user_nickname, user_data in users.items():
        if user_nickname.lower() == nickname.lower():
            return user_data.get("is_host", False)
    return False


def set_host(nickname: str, is_host: bool = True) -> bool:
    """사용자를 호스트로 설정/해제"""
    users = load_users()
    for user_nickname in users.keys():
        if user_nickname.lower() == nickname.lower():
            users[user_nickname]["is_host"] = is_host
            save_users(users)
            return True
    return False


def verify_password(nickname: str, password: str) -> bool:
    """비밀번호 확인"""
    users = load_users()

    # 대소문자 구분 없이 찾기
    for user_nickname, user_data in users.items():
        if user_nickname.lower() == nickname.lower():
            return user_data["password_hash"] == hash_password(password)

    return False


def get_user_progress_file(nickname: str) -> Path:
    """사용자별 진행도 파일 경로"""
    return USER_DATA_DIR / nickname / "progress.json"


def load_user_progress(nickname: str) -> dict:
    """사용자 진행도 로드"""
    progress_file = get_user_progress_file(nickname)
    if progress_file.exists():
        return json.loads(progress_file.read_text(encoding="utf-8"))
    return {
        "xp": 0,
        "solved": 0,
        "history": [],
        "topic_mastery": {},
        "current_topic": None,
    }


def save_user_progress(nickname: str, progress: dict):
    """사용자 진행도 저장"""
    progress_file = get_user_progress_file(nickname)
    progress_file.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def get_all_users() -> list[dict]:
    """모든 사용자 목록 (관리용)"""
    users = load_users()
    result = []
    for nickname, user_data in users.items():
        progress = load_user_progress(nickname)
        result.append({
            "nickname": nickname,
            "created_at": user_data["created_at"],
            "xp": progress.get("xp", 0),
            "solved": progress.get("solved", 0),
        })
    return sorted(result, key=lambda x: x["created_at"], reverse=True)
