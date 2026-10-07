"""사용자 진도 대시보드"""

import json
from pathlib import Path
import streamlit as st
from learning_paths import LearningPath, Mastery, TOPIC_BY_ID


def get_progress_summary(progress: dict) -> dict:
    """진도 요약 정보"""
    topic_mastery = {k: Mastery(v) for k, v in progress.get("topic_mastery", {}).items()}
    stats = LearningPath.get_learning_stats(topic_mastery)

    return {
        "total_xp": progress.get("xp", 0),
        "solved_count": progress.get("solved", 0),
        "total_topics": stats["total"],
        "completed_topics": stats["completed"],
        "learning_topics": stats["learning"],
        "completion_rate": stats["completion_rate"],
        "next_topics": get_next_topics(topic_mastery),
    }


def get_level_info(total_xp: int) -> dict:
    """레벨 정보"""
    def xp_needed(level: int) -> int:
        return 100 + 50 * (level - 1)

    level, xp, need_xp = 1, total_xp, xp_needed(1)
    while xp >= xp_needed(level):
        xp -= xp_needed(level)
        level += 1

    return {
        "level": level,
        "current_xp": xp,
        "next_xp": need_xp,
        "progress": xp / need_xp if need_xp > 0 else 0,
    }


def get_tier(level: int) -> dict:
    """티어 정보"""
    TIERS = [
        (10, "Expert", "#ffe5e5", "#d32f2f"),
        (5, "Student", "#fff8d6", "#f9a825"),
        (1, "Beginner", "#e6f6e6", "#2e7d32"),
    ]
    min_level, tier_name, bg_color, accent = next(t for t in TIERS if level >= t[0])

    return {
        "name": tier_name,
        "level": level,
        "background": bg_color,
        "accent": accent,
    }


def get_next_topics(topic_mastery: dict) -> list:
    """다음 학습할 주제 (최대 3개)"""
    topics = []
    available_topics = LearningPath.get_all_topics()

    for topic in available_topics:
        if topic_mastery.get(topic.id, Mastery.NOT_STARTED) == Mastery.NOT_STARTED:
            if topic.is_unlocked(topic_mastery):
                topics.append(topic)
                if len(topics) >= 3:
                    break

    return topics


def get_achievement_badges(progress: dict) -> list:
    """달성 배지"""
    badges = []
    topic_mastery = {k: Mastery(v) for k, v in progress.get("topic_mastery", {}).items()}

    # 문제 풀이 관련 배지
    solved = progress.get("solved", 0)
    if solved >= 1:
        badges.append({"icon": "🎯", "name": "첫 문제 해결", "description": "첫 번째 문제를 풀었어요"})
    if solved >= 5:
        badges.append({"icon": "⚡", "name": "5개 해결", "description": "5개의 문제를 풀었어요"})
    if solved >= 10:
        badges.append({"icon": "🔥", "name": "10개 해결", "description": "10개의 문제를 풀었어요"})
    if solved >= 25:
        badges.append({"icon": "💪", "name": "25개 해결", "description": "25개의 문제를 풀었어요"})
    if solved >= 50:
        badges.append({"icon": "👑", "name": "50개 해결", "description": "50개의 문제를 풀었어요"})

    # 주제 완료 관련 배지
    completed_topics = sum(1 for m in topic_mastery.values() if m.value >= Mastery.BASIC.value)
    if completed_topics >= 1:
        badges.append({"icon": "📚", "name": "첫 주제 완료", "description": "첫 번째 주제를 완료했어요"})
    if completed_topics >= 5:
        badges.append({"icon": "📖", "name": "5개 주제 완료", "description": "5개의 주제를 완료했어요"})
    if completed_topics >= 10:
        badges.append({"icon": "🧠", "name": "10개 주제 완료", "description": "10개의 주제를 완료했어요"})

    return badges


def show_welcome_dashboard(nickname: str, progress: dict):
    """환영 대시보드"""

    # 정보 수집
    summary = get_progress_summary(progress)
    level_info = get_level_info(summary["total_xp"])
    tier_info = get_tier(level_info["level"])
    badges = get_achievement_badges(progress)

    # 환영 헤더
    st.markdown(f"""
    <div style='text-align: center; padding: 20px;'>
        <h1>👋 환영합니다, <span style='color: {tier_info["accent"]}'>{nickname}</span>님!</h1>
        <p style='font-size: 18px;'>당신의 학습 진도를 확인해보세요</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # 레벨 & 진행도
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style='background: {tier_info["background"]}; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='margin: 0;'>{tier_info["name"]}</h2>
            <h1 style='margin: 10px 0 0 0; color: {tier_info["accent"]};'>Lv. {level_info["level"]}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.metric("누적 경험치", f"{summary['total_xp']} XP")
        st.metric("문제 해결", f"{summary['solved_count']}개")

    with col3:
        progress_pct = level_info["progress"] * 100
        st.metric("다음 레벨까지", f"{level_info['current_xp']}/{level_info['next_xp']} XP")
        st.progress(level_info["progress"], text=f"{progress_pct:.0f}%")

    st.divider()

    # 학습 진도
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 학습 진도")

        completion = summary["completion_rate"]
        difficulty_colors = {
            "초급": ("🟢", "#e6f6e6"),
            "중급": ("🟡", "#fff8d6"),
            "고난도": ("🔴", "#ffe5e5"),
        }

        for difficulty in ["초급", "중급", "고난도"]:
            topics = [t for t in LearningPath.get_all_topics() if t.difficulty == difficulty]
            topic_mastery = {k: Mastery(v) for k, v in progress.get("topic_mastery", {}).items()}
            completed = sum(1 for t in topics if topic_mastery.get(t.id, Mastery.NOT_STARTED).value >= Mastery.BASIC.value)

            icon, color = difficulty_colors[difficulty]
            st.markdown(f"""
            <div style='background: {color}; padding: 15px; border-radius: 8px; margin-bottom: 10px;'>
                <strong>{icon} {difficulty}: {completed}/{len(topics)}</strong>
                <div style='background: #ddd; border-radius: 5px; height: 8px; margin-top: 5px;'>
                    <div style='background: {color}; width: {completed/len(topics)*100 if len(topics) > 0 else 0}%; height: 100%; border-radius: 5px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.metric("전체 진행률", f"{completion:.0f}%")

    with col2:
        st.subheader("🎯 다음 학습 추천")

        topic_mastery = {k: Mastery(v) for k, v in progress.get("topic_mastery", {}).items()}
        next_topics = LearningPath.get_recommended_next(topic_mastery, level_info["level"])

        if next_topics:
            st.markdown(f"""
            <div style='background: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3;'>
                <h3 style='margin-top: 0;'>📖 {next_topics.name}</h3>
                <p>{next_topics.description}</p>
                <small>예상 소요시간: {next_topics.estimated_time}분</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("🎉 모든 주제를 완료했습니다!")

    st.divider()

    # 달성 배지
    if badges:
        st.subheader("🏆 획득한 배지")
        cols = st.columns(len(badges) if len(badges) <= 5 else 5)

        for i, badge in enumerate(badges[:5]):
            with cols[i % 5]:
                st.markdown(f"""
                <div style='text-align: center; padding: 10px;'>
                    <div style='font-size: 40px;'>{badge["icon"]}</div>
                    <small><strong>{badge["name"]}</strong></small>
                    <br><small style='color: #666;'>{badge["description"]}</small>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # 학습 통계
    st.subheader("📊 학습 통계")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("완료한 주제", f"{summary['completed_topics']}/{summary['total_topics']}")
    col2.metric("학습 중인 주제", summary["learning_topics"])
    col3.metric("평균 해결 시간", "~15분" if summary["solved_count"] > 0 else "-")
    col4.metric("연속 풀이", f"{progress.get('streak', 0)}일" if progress.get('streak', 0) > 0 else "0일")

    st.divider()

    # 학습 팁
    st.info("""
    💡 **학습 팁**

    1. **순차적 학습**: 선행 주제를 완료해야 다음 주제가 해제됩니다
    2. **정기적 복습**: 같은 주제의 여러 문제를 풀어 숙련도를 높이세요
    3. **피드백 수집**: 설문조사에서 의견을 남기면 앱 개선에 도움이 됩니다
    4. **목표 설정**: 주당 문제 해결 목표를 정하고 달성해보세요
    """)
