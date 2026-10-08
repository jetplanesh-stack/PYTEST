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
    tutorial: dict = None  # 실습 정보 (선택사항)

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
        tutorial={
            "title": "사용자 프로필 관리자",
            "app_description": "변수를 사용해서 사용자 정보를 저장하고 출력하는 앱을 만들어봅시다!",
            "steps": [
                {
                    "step": 1,
                    "title": "📖 개념 학습: 변수란?",
                    "type": "lesson",
                    "content": "변수는 데이터를 저장하는 상자입니다. 변수에 이름을 붙이고, 원하는 값을 저장할 수 있습니다.\n\n예를 들어:\n- name = '철수' → 문자열 저장\n- age = 15 → 숫자 저장\n- is_student = True → 참/거짓 저장",
                    "code_example": "name = '철수'\nage = 15\nheight = 175.5\nis_student = True\n\nprint(name)\nprint(age)\nprint(height)\nprint(is_student)"
                },
                {
                    "step": 2,
                    "title": "💻 실습 1: 사용자 정보 변수에 저장하기",
                    "type": "practice",
                    "task": "다음 정보를 변수에 저장하세요:\n- 이름: '김철수'\n- 나이: 25\n- 도시: '서울'\n\n그리고 각 변수를 출력하세요.",
                    "hint": "name = '김철수'와 같이 = 기호를 사용해서 값을 할당하면 됩니다. print()로 출력하세요.",
                    "validation": "output_contains",
                    "validation_keywords": ["김철수", "25", "서울"]
                },
                {
                    "step": 3,
                    "title": "💻 실습 2: 문자열 포맷팅으로 프로필 만들기",
                    "type": "practice",
                    "task": "저장된 변수들을 사용해서 다음처럼 출력하세요:\n'안녕하세요, 김철수입니다. 저는 25살이고 서울에 살고 있습니다.'",
                    "hint": "f-string을 사용하면 됩니다: print(f'안녕하세요, {name}입니다. ...')",
                    "expected_output": "안녕하세요, 김철수입니다. 저는 25살이고 서울에 살고 있습니다.",
                    "validation": "exact_output"
                },
                {
                    "step": 4,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**변수의 작동 원리**\n\n1. **메모리 할당**: Python이 컴퓨터의 메모리에 공간을 할당합니다.\n2. **값 저장**: 할당받은 공간에 데이터를 저장합니다.\n3. **이름 연결**: 변수 이름이 그 메모리 공간을 가리킵니다.\n\n예: `name = '철수'`라고 하면\n- 메모리에 문자 데이터 저장\n- 그 위치에 'name'이라는 라벨 붙이기\n- 나중에 name을 쓰면 그 위치의 값을 찾아옴\n\n**자료형의 종류**\n- **str (문자열)**: '철수', \"서울\" - 따옴표로 감싸야 함\n- **int (정수)**: 15, 100 - 숫자만\n- **float (실수)**: 175.5, 3.14 - 소수점 포함\n- **bool (불)**: True, False - 참/거짓만"
                }
            ]
        },
    ),
    Topic(
        id="strings_lists",
        name="문자열과 리스트 기초",
        description="문자열/리스트 생성, 인덱싱, 슬라이싱, 기본 메서드",
        difficulty="초급",
        prerequisites=["vars_basic"],
        skills=["문자열", "리스트", "인덱싱", "슬라이싱"],
        estimated_time=40,
        tutorial={
            "title": "할일 목록(Todo) 앱",
            "app_description": "할일을 리스트에 저장하고 관리하는 앱을 만들어봅시다!",
            "steps": [
                {
                    "step": 1,
                    "title": "📖 개념 학습: 문자열과 리스트",
                    "type": "lesson",
                    "content": "**문자열(String)**: 텍스트를 저장하는 데이터 타입. 인덱싱으로 개별 글자에 접근\n**리스트(List)**: 여러 데이터를 순서대로 저장. 대괄호 []로 생성\n\n예:\n- 문자열: text = '안녕하세요' → text[0] = '안'\n- 리스트: tasks = ['숙제하기', '밥먹기'] → tasks[0] = '숙제하기'",
                    "code_example": "text = '안녕'\nprint(text[0])\nprint(text[1])\n\ntasks = ['공부', '운동']\nprint(tasks[0])\nprint(tasks[1])"
                },
                {
                    "step": 2,
                    "title": "💻 실습 1: 리스트 생성하고 요소 접근하기",
                    "type": "practice",
                    "task": "다음 할일들을 리스트에 저장하세요: '수학공부', '영어공부', '밥먹기'\n그리고 첫 번째 항목과 마지막 항목을 출력하세요.",
                    "hint": "tasks = ['수학공부', '영어공부', '밥먹기']\nprint(tasks[0])\nprint(tasks[2])  # 또는 tasks[-1]",
                    "validation": "output_contains",
                    "validation_keywords": ["수학공부", "밥먹기"]
                },
                {
                    "step": 3,
                    "title": "💻 실습 2: 리스트에 항목 추가하기",
                    "type": "practice",
                    "task": "위의 tasks 리스트에 '영화보기'를 추가하고, 전체 리스트를 출력하세요.",
                    "hint": "tasks.append('영화보기')\nprint(tasks)",
                    "validation": "output_contains",
                    "validation_keywords": ["영화보기", "수학공부"]
                },
                {
                    "step": 4,
                    "title": "💻 실습 3: 리스트 슬라이싱과 길이",
                    "type": "practice",
                    "task": "tasks 리스트에서 첫 2개 항목만 출력하고, 전체 개수를 출력하세요.",
                    "hint": "print(tasks[0:2])\nprint(len(tasks))",
                    "validation": "output_contains",
                    "validation_keywords": ["4"]  # len(tasks) = 4
                },
                {
                    "step": 5,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**문자열과 리스트의 메모리 구조**\n\n문자열은 불변(immutable): 한 번 만들면 변경 불가\n```\ntext = '안녕'\ntext[0] = '잘'  # 에러! 불가능\n```\n\n리스트는 가변(mutable): 언제든 변경 가능\n```\ntasks = ['a', 'b']\ntasks[0] = 'c'  # 가능\ntasks.append('d')  # 추가 가능\n```\n\n**인덱싱**: 위치로 요소에 접근 (0부터 시작)\n- tasks[0] = 첫 번째\n- tasks[-1] = 마지막\n\n**슬라이싱**: 범위로 일부 추출\n- tasks[0:2] = 인덱스 0, 1만\n- tasks[:2] = 처음부터 2개\n- tasks[1:] = 1번째부터 끝까지"
                }
            ]
        },
    ),
    Topic(
        id="if_else",
        name="조건문 (if/elif/else)",
        description="조건식 작성, 논리 연산자, 중첩 조건문",
        difficulty="초급",
        prerequisites=["vars_basic"],
        skills=["조건문", "비교 연산자", "논리 연산자"],
        estimated_time=30,
        tutorial={
            "title": "학점 계산 프로그램",
            "app_description": "점수를 입력받아 학점을 자동으로 계산하는 앱을 만들어봅시다!",
            "steps": [
                {
                    "step": 1,
                    "title": "📖 개념 학습: 조건문이란?",
                    "type": "lesson",
                    "content": "조건문은 특정 조건이 참/거짓인지 확인해서 다른 코드를 실행합니다.\n\n**비교 연산자**:\n- == (같다)\n- != (다르다)\n- > (크다), < (작다)\n- >= (크거나 같다), <= (작거나 같다)\n\n**조건문 구조**:\nif 조건:\n    참일 때 실행\nelif 다른 조건:\n    참일 때 실행\nelse:\n    위 조건 모두 거짓일 때 실행",
                    "code_example": "score = 85\n\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelif score >= 70:\n    print('C')\nelse:\n    print('F')"
                },
                {
                    "step": 2,
                    "title": "💻 실습 1: 간단한 조건문 작성하기",
                    "type": "practice",
                    "task": "age = 20이라고 하고, age가 18 이상이면 '성인입니다'를 출력하세요.",
                    "hint": "if age >= 18:\n    print('성인입니다')",
                    "expected_output": "성인입니다",
                    "validation": "exact_output"
                },
                {
                    "step": 3,
                    "title": "💻 실습 2: elif를 사용한 다중 조건",
                    "type": "practice",
                    "task": "score = 85라고 하고, 학점을 계산해서 출력하세요.\n- 90 이상: A\n- 80 이상: B\n- 70 이상: C\n- 그 외: F",
                    "hint": "if score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\n...",
                    "expected_output": "B",
                    "validation": "exact_output"
                },
                {
                    "step": 4,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**조건문의 실행 순서**\n\n1. if 조건 확인 → True면 블록 실행, False면 다음으로\n2. elif 조건 확인 → True면 블록 실행, False면 다음으로\n3. else 블록 실행\n\n**주의사항**:\n- 조건이 여러 개라도 **처음 참인 것만 실행**\n- if, elif, else는 들여쓰기(indentation)로 블록을 구분\n- Python은 들여쓰기가 매우 중요!\n\n**논리 연산자**:\n- `and`: 모두 참이어야 참\n- `or`: 하나라도 참이면 참\n- `not`: 결과를 반대로\n\n예:\n```python\nage = 25\nif age >= 20 and age < 30:\n    print('20대입니다')\n```"
                }
            ]
        },
    ),
    Topic(
        id="loops",
        name="반복문 (for/while)",
        description="for 루프, while 루프, break/continue, 중첩 루프",
        difficulty="초급",
        prerequisites=["if_else"],
        skills=["for 루프", "while 루프", "제어문"],
        estimated_time=40,
        tutorial={
            "title": "구구단 출력기",
            "app_description": "반복문을 사용해서 구구단을 출력하는 앱을 만들어봅시다!",
            "steps": [
                {
                    "step": 1,
                    "title": "📖 개념 학습: 반복문이란?",
                    "type": "lesson",
                    "content": "반복문은 같은 코드를 여러 번 실행합니다.\n\n**for 루프**: 횟수가 정해져 있을 때\n```python\nfor i in range(5):\n    print(i)  # 0, 1, 2, 3, 4\n```\n\n**while 루프**: 조건이 거짓이 될 때까지\n```python\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1\n```\n\n**리스트 순회**:\n```python\nfruits = ['사과', '바나나', '딸기']\nfor fruit in fruits:\n    print(fruit)\n```",
                    "code_example": "# 1부터 5까지 출력\nfor i in range(1, 6):\n    print(i)\n\n# 2의 배수 찾기\nfor num in [1, 2, 3, 4, 5, 6]:\n    if num % 2 == 0:\n        print(num)"
                },
                {
                    "step": 2,
                    "title": "💻 실습 1: 기본 for 루프",
                    "type": "practice",
                    "task": "1부터 5까지의 숫자를 출력하세요.",
                    "hint": "for i in range(1, 6):\n    print(i)",
                    "validation": "output_contains",
                    "validation_keywords": ["1", "2", "3", "4", "5"]
                },
                {
                    "step": 3,
                    "title": "💻 실습 2: 구구단 (한 줄)",
                    "type": "practice",
                    "task": "3단 구구단을 출력하세요.\n형식: '3 × 1 = 3' 처럼 출력",
                    "hint": "for i in range(1, 10):\n    print(f'3 × {i} = {3*i}')",
                    "validation": "output_contains",
                    "validation_keywords": ["3 ×", "27"]
                },
                {
                    "step": 4,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**for 루프의 작동 원리**\n\n1. range(1, 6)은 [1, 2, 3, 4, 5] 리스트를 만듭니다\n2. 각 원소를 차례로 변수 i에 할당\n3. 루프 블록 실행\n4. 다음 원소로 반복\n\n**range() 함수**:\n- range(5) → 0, 1, 2, 3, 4\n- range(1, 6) → 1, 2, 3, 4, 5\n- range(1, 10, 2) → 1, 3, 5, 7, 9 (스텝)\n\n**while 루프**는 직접 조건을 확인:\n```python\ncount = 0\nwhile count < 5:  # count가 5 미만이면 반복\n    print(count)\n    count += 1  # 필수! 무한루프 방지\n```\n\n**break / continue**:\n- break: 루프 탈출\n- continue: 남은 코드 스킵하고 다음 반복"
                }
            ]
        },
    ),
    Topic(
        id="functions",
        name="함수 기초",
        description="함수 정의, 매개변수, 반환값, 변수 스코프",
        difficulty="초급",
        prerequisites=["loops"],
        skills=["함수", "매개변수", "반환값", "스코프"],
        estimated_time=35,
        tutorial={
            "title": "계산기 앱",
            "app_description": "함수를 사용해서 계산 기능을 만드는 앱을 만들어봅시다!",
            "steps": [
                {
                    "step": 1,
                    "title": "📖 개념 학습: 함수란?",
                    "type": "lesson",
                    "content": "함수는 재사용 가능한 코드 묶음입니다.\n\n**함수의 구조**:\n```python\ndef 함수명(매개변수):\n    # 함수의 본문\n    return 반환값\n```\n\n**예시**:\n```python\ndef add(a, b):\n    return a + b\n\nresult = add(3, 5)  # 8\nprint(result)\n```\n\n**매개변수**: 함수가 받는 입력\n**반환값**: 함수가 돌려주는 결과",
                    "code_example": "def greet(name):\n    return f'안녕하세요, {name}님!'\n\nmessage = greet('철수')\nprint(message)\n\ndef add(a, b):\n    return a + b\n\nresult = add(10, 20)\nprint(result)"
                },
                {
                    "step": 2,
                    "title": "💻 실습 1: 간단한 함수 만들기",
                    "type": "practice",
                    "task": "두 숫자를 받아서 더한 값을 반환하는 add() 함수를 만드세요.\nadd(5, 3)을 호출해서 결과를 출력하세요.",
                    "hint": "def add(a, b):\n    return a + b\n\nprint(add(5, 3))",
                    "expected_output": "8",
                    "validation": "exact_output"
                },
                {
                    "step": 3,
                    "title": "💻 실습 2: 여러 함수 만들기",
                    "type": "practice",
                    "task": "덧셈(add), 뺄셈(subtract), 곱셈(multiply) 함수를 만드세요.\nそれぞれを以下のように呼び出してください:\n- add(10, 5)\n- subtract(10, 5)\n- multiply(10, 5)",
                    "hint": "def add(a, b):\n    return a + b\ndef subtract(a, b):\n    return a - b\ndef multiply(a, b):\n    return a * b\n\nprint(add(10, 5))\nprint(subtract(10, 5))\nprint(multiply(10, 5))",
                    "validation": "output_contains",
                    "validation_keywords": ["15", "5", "50"]
                },
                {
                    "step": 4,
                    "title": "💻 실습 3: 조건문이 있는 함수",
                    "type": "practice",
                    "task": "숫자를 받아서, 양수면 'positive', 음수면 'negative', 0이면 'zero'를 반환하는 check_number() 함수를 만드세요.",
                    "hint": "def check_number(n):\n    if n > 0:\n        return 'positive'\n    elif n < 0:\n        return 'negative'\n    else:\n        return 'zero'\n\nprint(check_number(5))",
                    "expected_output": "positive",
                    "validation": "exact_output"
                },
                {
                    "step": 5,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**함수의 실행 과정**\n\n1. def로 함수 정의 (메모리에 저장됨)\n2. 함수 호출: `add(5, 3)`\n3. 인자값(5, 3)이 매개변수(a, b)에 대입\n4. 함수 본문 실행: `return a + b` → `return 8`\n5. 반환값(8)을 호출한 곳으로 전달\n\n**스코프(Scope)**:\n- 함수 내에서만 유효한 변수\n```python\ndef func():\n    x = 10  # 함수 내부에서만 유효\nprint(x)  # 에러! x는 함수 바깥에서 모름\n```\n\n**여러 값 반환**:\n```python\ndef get_name_age():\n    return 'John', 25  # 튜플로 반환\n\nname, age = get_name_age()\n```\n\n**기본값 설정**:\n```python\ndef greet(name='Guest'):\n    return f'Hello, {name}!'\n\ngreet()  # 'Hello, Guest!'\ngreet('Alice')  # 'Hello, Alice!'\n```"
                }
            ]
        },
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
