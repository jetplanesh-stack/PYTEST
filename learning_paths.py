"""초급부터 고급까지 단계별 학습 경로 및 모듈 시스템."""

from dataclasses import dataclass
from enum import Enum


class Mastery(Enum):
    """개념 습득 수준"""
    NOT_STARTED = 0      # 시작 안 함
    LEARNING = 1         # 학습 중
    BASIC = 2            # 기초 이해
    INTERMEDIATE = 3     # 중급 이해
    ADVANCED = 4         # 숙련


@dataclass
class Topic:
    """학습 주제"""
    id: str               # 고유 ID (예: "vars_basic")
    name: str             # 주제명 (예: "변수와 자료형")
    description: str      # 설명
    difficulty: str       # "초급" / "중급" / "고난도"
    prerequisites: list[str]  # 선행 주제 ID
    skills: list[str]     # 학습할 기술 태그 (예: ["변수", "자료형", "타입 변환"])
    estimated_time: int   # 예상 소요 시간(분)

    def is_unlocked(self, completed: dict[str, Mastery]) -> bool:
        """모든 선행 주제를 완료했는지 확인"""
        return all(
            completed.get(prereq, Mastery.NOT_STARTED).value >= Mastery.BASIC.value
            for prereq in self.prerequisites
        )


# ==================== 초급 (Beginner) ====================
BEGINNER_TOPICS = [
    Topic(
        id="vars_basic",
        name="변수와 자료형",
        description="변수 선언, 기본 데이터 타입(int, float, str, bool) 이해",
        difficulty="초급",
        prerequisites=[],
        skills=["변수", "자료형", "타입 변환"],
        estimated_time=30,
    ),
    Topic(
        id="strings_lists",
        name="문자열과 리스트 기초",
        description="문자열/리스트 생성, 인덱싱, 슬라이싱, 기본 메서드",
        difficulty="초급",
        prerequisites=["vars_basic"],
        skills=["문자열", "리스트", "인덱싱", "슬라이싱"],
        estimated_time=40,
    ),
    Topic(
        id="if_else",
        name="조건문 (if/elif/else)",
        description="조건식 작성, 논리 연산자, 중첩 조건문",
        difficulty="초급",
        prerequisites=["vars_basic"],
        skills=["조건문", "비교 연산자", "논리 연산자"],
        estimated_time=30,
    ),
    Topic(
        id="loops",
        name="반복문 (for/while)",
        description="for 루프, while 루프, break/continue, 중첩 루프",
        difficulty="초급",
        prerequisites=["if_else"],
        skills=["for 루프", "while 루프", "제어문"],
        estimated_time=40,
    ),
    Topic(
        id="functions",
        name="함수 기초",
        description="함수 정의, 매개변수, 반환값, 변수 스코프",
        difficulty="초급",
        prerequisites=["loops"],
        skills=["함수", "매개변수", "반환값", "스코프"],
        estimated_time=35,
    ),
]

# ==================== 중급 (Intermediate) ====================
INTERMEDIATE_TOPICS = [
    Topic(
        id="dicts_sets",
        name="딕셔너리와 집합",
        description="딕셔너리/집합 생성, 조작, 메서드, 해시 개념",
        difficulty="중급",
        prerequisites=["strings_lists"],
        skills=["딕셔너리", "집합", "해시"],
        estimated_time=40,
    ),
    Topic(
        id="comprehension",
        name="리스트/딕셔너리 컴프리헨션",
        description="컴프리헨션 문법, 조건부 컴프리헨션, 중첩 컴프리헨션",
        difficulty="중급",
        prerequisites=["dicts_sets", "loops"],
        skills=["컴프리헨션", "리스트 생성식"],
        estimated_time=30,
    ),
    Topic(
        id="sorting",
        name="정렬과 검색",
        description="sorted(), sort(), key 함수, 검색 알고리즘",
        difficulty="중급",
        prerequisites=["strings_lists", "functions"],
        skills=["정렬", "검색", "정렬 키"],
        estimated_time=35,
    ),
    Topic(
        id="string_methods",
        name="문자열 심화",
        description="문자열 메서드, 정규표현식 기초, 문자열 포매팅",
        difficulty="중급",
        prerequisites=["strings_lists"],
        skills=["문자열 메서드", "정규표현식", "포매팅"],
        estimated_time=40,
    ),
    Topic(
        id="algorithms_basics",
        name="알고리즘 기초",
        description="투 포인터, 누적합, 슬라이딩 윈도우 기초",
        difficulty="중급",
        prerequisites=["sorting", "loops"],
        skills=["투 포인터", "누적합", "슬라이딩 윈도우"],
        estimated_time=45,
    ),
]

# ==================== 고급 (Advanced) ====================
ADVANCED_TOPICS = [
    Topic(
        id="recursion",
        name="재귀와 백트래킹",
        description="재귀 함수, 분할 정복, 백트래킹 알고리즘",
        difficulty="고난도",
        prerequisites=["functions"],
        skills=["재귀", "분할 정복", "백트래킹"],
        estimated_time=50,
    ),
    Topic(
        id="dynamic_programming",
        name="동적 계획법 (DP)",
        description="DP의 원리, 메모이제이션, 타뷸레이션, DP 최적화",
        difficulty="고난도",
        prerequisites=["recursion", "algorithms_basics"],
        skills=["DP", "메모이제이션", "타뷸레이션"],
        estimated_time=60,
    ),
    Topic(
        id="graphs",
        name="그래프 탐색 (DFS/BFS)",
        description="그래프 표현, DFS, BFS, 위상 정렬, 연결성 문제",
        difficulty="고난도",
        prerequisites=["dicts_sets", "recursion"],
        skills=["DFS", "BFS", "그래프", "위상 정렬"],
        estimated_time=55,
    ),
    Topic(
        id="binary_search",
        name="이분 탐색과 이분 답",
        description="이분 탐색, 이분 답, Parametric Search",
        difficulty="고난도",
        prerequisites=["sorting", "algorithms_basics"],
        skills=["이분 탐색", "이분 답", "Parametric Search"],
        estimated_time=40,
    ),
    Topic(
        id="heaps",
        name="힙과 우선순위 큐",
        description="힙의 구조, heapq 모듈, 우선순위 큐 활용",
        difficulty="고난도",
        prerequisites=["algorithms_basics"],
        skills=["힙", "우선순위 큐", "heapq"],
        estimated_time=45,
    ),
    Topic(
        id="advanced_dp",
        name="고급 DP (LIS, 구간 DP)",
        description="최장 증가 수열, 구간 DP, 확률/게임 DP",
        difficulty="고난도",
        prerequisites=["dynamic_programming"],
        skills=["LIS", "구간 DP", "최적화"],
        estimated_time=60,
    ),
]

# ==================== 모든 주제 모음 ====================
ALL_TOPICS = BEGINNER_TOPICS + INTERMEDIATE_TOPICS + ADVANCED_TOPICS
TOPIC_BY_ID = {t.id: t for t in ALL_TOPICS}


class LearningPath:
    """사용자별 학습 경로 관리"""

    @staticmethod
    def get_all_topics() -> list[Topic]:
        """모든 주제 반환"""
        return ALL_TOPICS

    @staticmethod
    def get_topics_by_level(level: int) -> list[Topic]:
        """현재 레벨에 추천되는 주제들"""
        if level < 5:
            return BEGINNER_TOPICS
        elif level < 10:
            return BEGINNER_TOPICS + INTERMEDIATE_TOPICS
        else:
            return ALL_TOPICS

    @staticmethod
    def get_recommended_next(completed: dict[str, Mastery], current_level: int) -> Topic | None:
        """다음에 학습할 주제 추천"""
        available_topics = LearningPath.get_topics_by_level(current_level)

        # 1. 시작하지 않은 주제 중 선행 조건을 만족하는 것
        for topic in available_topics:
            if completed.get(topic.id, Mastery.NOT_STARTED) == Mastery.NOT_STARTED:
                if topic.is_unlocked(completed):
                    return topic

        # 2. 학습 중인 주제
        for topic in available_topics:
            if completed.get(topic.id, Mastery.NOT_STARTED) == Mastery.LEARNING:
                return topic

        # 3. 기초만 완료한 주제
        for topic in available_topics:
            if completed.get(topic.id, Mastery.NOT_STARTED) == Mastery.BASIC:
                return topic

        return None

    @staticmethod
    def get_learning_stats(completed: dict[str, Mastery]) -> dict:
        """학습 통계"""
        total = len(ALL_TOPICS)
        not_started = sum(1 for m in completed.values() if m == Mastery.NOT_STARTED)
        learning = sum(1 for m in completed.values() if m == Mastery.LEARNING)
        basic = sum(1 for m in completed.values() if m == Mastery.BASIC)
        intermediate = sum(1 for m in completed.values() if m == Mastery.INTERMEDIATE)
        advanced = sum(1 for m in completed.values() if m == Mastery.ADVANCED)

        completed_count = basic + intermediate + advanced
        completion_rate = (completed_count / total * 100) if total > 0 else 0

        return {
            "total": total,
            "not_started": not_started,
            "learning": learning,
            "basic": basic,
            "intermediate": intermediate,
            "advanced": advanced,
            "completed": completed_count,
            "completion_rate": completion_rate,
        }
