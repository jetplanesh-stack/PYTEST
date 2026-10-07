"""학습 진도 설문조사 시스템"""

import json
from pathlib import Path
from datetime import datetime
import streamlit as st


SURVEY_DIR = Path(__file__).with_name("user_data")


def get_survey_file(nickname: str) -> Path:
    """사용자별 설문 파일 경로"""
    return SURVEY_DIR / nickname / "survey.json"


def load_survey(nickname: str) -> dict:
    """설문 데이터 로드"""
    survey_file = get_survey_file(nickname)
    if survey_file.exists():
        return json.loads(survey_file.read_text(encoding="utf-8"))
    return {
        "feedback": [],
        "satisfaction": [],
        "difficulty_ratings": {},
    }


def save_survey(nickname: str, survey: dict):
    """설문 데이터 저장"""
    survey_file = get_survey_file(nickname)
    survey_file.write_text(json.dumps(survey, ensure_ascii=False, indent=2), encoding="utf-8")


def add_problem_feedback(nickname: str, title: str, difficulty: str,
                         rating: int, quality: int, comment: str = ""):
    """문제별 피드백 추가"""
    survey = load_survey(nickname)

    feedback = {
        "timestamp": datetime.now().isoformat(),
        "problem_title": title,
        "difficulty": difficulty,
        "difficulty_rating": rating,  # 1: 너무 쉬움, 2: 적당, 3: 너무 어려움
        "quality_rating": quality,     # 1: 나쁨, 2: 보통, 3: 좋음, 4: 매우 좋음
        "comment": comment,
    }

    survey["feedback"].append(feedback)
    save_survey(nickname, survey)


def add_satisfaction_survey(nickname: str, overall: int, difficulty_level: int,
                           ui_rating: int, suggestion: str = ""):
    """만족도 설문 추가"""
    survey = load_survey(nickname)

    satisfaction = {
        "timestamp": datetime.now().isoformat(),
        "overall_satisfaction": overall,      # 1~5
        "difficulty_appropriateness": difficulty_level,  # 1~5
        "ui_ux_rating": ui_rating,            # 1~5
        "suggestion": suggestion,
    }

    survey["satisfaction"].append(satisfaction)
    save_survey(nickname, survey)


def add_topic_difficulty_rating(nickname: str, topic_id: str, topic_name: str,
                                rating: int, comment: str = ""):
    """주제별 난이도 평가"""
    survey = load_survey(nickname)

    if "difficulty_ratings" not in survey:
        survey["difficulty_ratings"] = {}

    survey["difficulty_ratings"][topic_id] = {
        "topic_name": topic_name,
        "rating": rating,  # 1: 너무 쉬움, 2: 쉬움, 3: 적당, 4: 어려움, 5: 매우 어려움
        "comment": comment,
        "timestamp": datetime.now().isoformat(),
    }

    save_survey(nickname, survey)


def get_statistics(nickname: str) -> dict:
    """설문 통계 계산"""
    survey = load_survey(nickname)

    stats = {
        "total_feedback": len(survey.get("feedback", [])),
        "total_satisfaction": len(survey.get("satisfaction", [])),
        "total_topics_rated": len(survey.get("difficulty_ratings", {})),
        "avg_difficulty_rating": 0,
        "avg_quality_rating": 0,
        "avg_satisfaction": 0,
        "avg_difficulty_appropriateness": 0,
        "avg_ui_rating": 0,
    }

    # 문제 피드백 통계
    feedback_list = survey.get("feedback", [])
    if feedback_list:
        difficulty_ratings = [f["difficulty_rating"] for f in feedback_list if "difficulty_rating" in f]
        quality_ratings = [f["quality_rating"] for f in feedback_list if "quality_rating" in f]

        if difficulty_ratings:
            stats["avg_difficulty_rating"] = sum(difficulty_ratings) / len(difficulty_ratings)
        if quality_ratings:
            stats["avg_quality_rating"] = sum(quality_ratings) / len(quality_ratings)

    # 만족도 통계
    satisfaction_list = survey.get("satisfaction", [])
    if satisfaction_list:
        overall = [s["overall_satisfaction"] for s in satisfaction_list if "overall_satisfaction" in s]
        difficulty = [s["difficulty_appropriateness"] for s in satisfaction_list if "difficulty_appropriateness" in s]
        ui = [s["ui_ux_rating"] for s in satisfaction_list if "ui_ux_rating" in s]

        if overall:
            stats["avg_satisfaction"] = sum(overall) / len(overall)
        if difficulty:
            stats["avg_difficulty_appropriateness"] = sum(difficulty) / len(difficulty)
        if ui:
            stats["avg_ui_rating"] = sum(ui) / len(ui)

    return stats


def load_progress_survey(nickname: str) -> dict:
    """진도 설문 데이터 로드"""
    survey_file = get_survey_file(nickname)
    if survey_file.exists():
        survey = json.loads(survey_file.read_text(encoding="utf-8"))
        return survey.get("progress_survey", {})
    return {}


def save_progress_survey(nickname: str, survey_data: dict):
    """진도 설문 결과 저장"""
    survey_file = get_survey_file(nickname)
    survey_file.parent.mkdir(parents=True, exist_ok=True)

    if survey_file.exists():
        survey = json.loads(survey_file.read_text(encoding="utf-8"))
    else:
        survey = {"feedback": [], "satisfaction": [], "difficulty_ratings": {}}

    survey["progress_survey"] = {
        **survey_data,
        "timestamp": datetime.now().isoformat(),
    }
    survey_file.write_text(json.dumps(survey, ensure_ascii=False, indent=2), encoding="utf-8")


def show_feedback_form():
    """문제 풀이 후 피드백 폼"""
    st.markdown("---")
    st.subheader("📋 이 문제에 대한 의견을 알려주세요")

    col1, col2 = st.columns(2)

    with col1:
        difficulty = st.radio(
            "문제 난이도는 어떻게 느껴졌나요?",
            options=[1, 2, 3],
            format_func=lambda x: {
                1: "🟢 너무 쉬웠어요",
                2: "🟡 적당했어요",
                3: "🔴 너무 어려웠어요",
            }[x],
            key=f"difficulty_{id(st.session_state.problem)}"
        )

    with col2:
        quality = st.radio(
            "문제 품질은 어떻게 생각하세요?",
            options=[1, 2, 3, 4],
            format_func=lambda x: {
                1: "😞 나쁨",
                2: "😐 보통",
                3: "😊 좋음",
                4: "😍 매우 좋음",
            }[x],
            key=f"quality_{id(st.session_state.problem)}"
        )

    comment = st.text_area(
        "추가 의견 (선택사항)",
        placeholder="이 문제를 개선할 점이 있으면 알려주세요...",
        key=f"comment_{id(st.session_state.problem)}"
    )

    if st.button("피드백 제출", key=f"submit_feedback_{id(st.session_state.problem)}"):
        if "user" in st.session_state and st.session_state.problem:
            p = st.session_state.problem["data"]
            add_problem_feedback(
                st.session_state.user,
                p.title,
                st.session_state.problem["difficulty"],
                difficulty,
                quality,
                comment
            )
            st.success("✅ 피드백이 저장되었습니다!")
