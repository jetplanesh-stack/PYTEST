"""학생 활동 로깅 및 모니터링 시스템"""

import json
from pathlib import Path
from datetime import datetime


ACTIVITY_LOG_DIR = Path(__file__).with_name("activity_logs")


def init_activity_log():
    """활동 로그 디렉토리 초기화"""
    ACTIVITY_LOG_DIR.mkdir(exist_ok=True)


def get_student_log_file(student_nickname: str) -> Path:
    """학생별 활동 로그 파일 경로"""
    return ACTIVITY_LOG_DIR / f"{student_nickname}_activities.json"


def log_activity(student_nickname: str, activity_type: str, details: dict):
    """학생 활동 기록"""
    init_activity_log()

    log_file = get_student_log_file(student_nickname)
    activities = []

    if log_file.exists():
        activities = json.loads(log_file.read_text(encoding="utf-8"))

    activity = {
        "timestamp": datetime.now().isoformat(),
        "type": activity_type,  # "problem_solved", "level_up", "topic_mastery", "login"
        "details": details,
    }

    activities.append(activity)
    log_file.write_text(json.dumps(activities, ensure_ascii=False, indent=2), encoding="utf-8")


def get_student_activities(student_nickname: str, limit: int = 20) -> list:
    """학생의 최근 활동 조회"""
    log_file = get_student_log_file(student_nickname)

    if not log_file.exists():
        return []

    try:
        activities = json.loads(log_file.read_text(encoding="utf-8"))
        recent = activities[-limit:] if len(activities) > limit else activities
        result = []
        for i in range(len(recent) - 1, -1, -1):
            result.append(recent[i])
        return result
    except:
        return []


def get_all_students_latest_activity() -> dict:
    """모든 학생의 최신 활동 조회"""
    init_activity_log()

    result = {}

    for log_file in ACTIVITY_LOG_DIR.glob("*_activities.json"):
        student_nickname = log_file.stem.replace("_activities", "")
        activities = json.loads(log_file.read_text(encoding="utf-8"))

        if activities:
            result[student_nickname] = activities[-1]  # 최신 활동만

    return result


def get_leaderboard() -> list:
    """전체 학생 순위표 (XP 기준)"""
    init_activity_log()

    leaderboard = []

    for log_file in ACTIVITY_LOG_DIR.glob("*_activities.json"):
        student_nickname = log_file.stem.replace("_activities", "")
        try:
            activities = json.loads(log_file.read_text(encoding="utf-8"))
        except:
            continue

        xp = 0
        solved = 0
        last_activity = None

        for i in range(len(activities) - 1, -1, -1):
            activity = activities[i]
            if activity.get("type") in ["problem_solved", "level_up"]:
                last_activity = activity
                xp = activity.get("details", {}).get("xp", 0)
                solved = activity.get("details", {}).get("solved", 0)
                break

        if xp > 0:
            leaderboard.append({
                "student": student_nickname,
                "xp": xp,
                "solved": solved,
                "last_activity": last_activity.get("timestamp", "") if last_activity else "",
                "activity_type": last_activity.get("type", "") if last_activity else "",
            })

    return sorted(leaderboard, key=lambda x: x["xp"], reverse=True)


def get_student_stats(student_nickname: str) -> dict:
    """학생의 활동 통계"""
    log_file = get_student_log_file(student_nickname)

    if not log_file.exists():
        return {
            "total_activities": 0,
            "problems_solved": 0,
            "level_ups": 0,
            "topics_mastered": 0,
            "total_xp": 0,
        }

    activities = json.loads(log_file.read_text(encoding="utf-8"))

    stats = {
        "total_activities": len(activities),
        "problems_solved": len([a for a in activities if a["type"] == "problem_solved"]),
        "level_ups": len([a for a in activities if a["type"] == "level_up"]),
        "topics_mastered": len([a for a in activities if a["type"] == "topic_mastery"]),
        "total_xp": 0,
    }

    # 최신 XP 추출
    for activity in reversed(activities):
        if "xp" in activity.get("details", {}):
            stats["total_xp"] = activity["details"]["xp"]
            break

    return stats
