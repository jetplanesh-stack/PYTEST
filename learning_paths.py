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
                    "title": "📖 변수의 정의와 자료형",
                    "type": "lesson",
                    "content": "**변수란?** 데이터를 저장하는 상자입니다. 변수에 이름을 붙이고 원하는 값을 저장할 수 있습니다.\n\n**기본 문법**:\n```python\n변수명 = 값\n```\n\n**예시**:\n```python\nname = '철수'      # 문자열\nage = 15           # 정수\nheight = 175.5     # 실수\nis_student = True  # 불(참/거짓)\n```\n\n**자료형의 종류**\n- **str (문자열)**: '철수', \"서울\" → 따옴표로 감싸야 함\n- **int (정수)**: 15, 100 → 숫자만\n- **float (실수)**: 175.5, 3.14 → 소수점 포함\n- **bool (불)**: True, False → 참/거짓\n\n**변수의 장점**\n1. 값을 저장했다가 나중에 사용 가능\n2. 코드가 읽기 쉬워짐\n3. 같은 값을 여러 번 쓸 때 편함",
                    "code_example": "name = '철수'\nage = 15\nheight = 175.5\nis_student = True\n\nprint(name)\nprint(age)\nprint(height)\nprint(is_student)"
                },
                {
                    "step": 2,
                    "title": "💡 실습 1: 변수 선언 및 출력",
                    "type": "lesson",
                    "content": "**실습**: 사용자 정보를 변수에 저장하고 출력해보세요.\n\n**풀이 과정**:\n1. `name = '김철수'` → 이름 변수 생성\n2. `age = 25` → 나이 변수 생성\n3. `city = '서울'` → 도시 변수 생성\n4. `print()` → 각 변수를 출력\n\n**전체 코드**:\n```python\nname = '김철수'\nage = 25\ncity = '서울'\n\nprint(name)\nprint(age)\nprint(city)\n```\n\n**출력 결과**:\n```\n김철수\n25\n서울\n```\n\n**이제 해보세요!**"
                },
                {
                    "step": 3,
                    "title": "📝 실습 2: 변수 저장 및 출력",
                    "type": "practice",
                    "task": "다음 정보를 변수에 저장하세요:\n- 이름: '박영희'\n- 나이: 28\n- 도시: '부산'\n\n그리고 각 변수를 차례대로 출력하세요.",
                    "hint": "name = '박영희'\nage = 28\ncity = '부산'\n\nprint(name)\nprint(age)\nprint(city)",
                    "expected_output": "박영희\n28\n부산",
                    "validation": "exact_output"
                },
                {
                    "step": 4,
                    "title": "🚀 실습 3: 문자열 포맷팅 (조금 더 어려움)",
                    "type": "practice",
                    "task": "위의 변수들을 사용해서 다음처럼 출력하세요:\n'이름: 박영희, 나이: 28, 도시: 부산'",
                    "hint": "f-string을 사용하면 됩니다:\nprint(f'이름: {name}, 나이: {age}, 도시: {city}')",
                    "expected_output": "이름: 박영희, 나이: 28, 도시: 부산",
                    "validation": "exact_output"
                },
                {
                    "step": 5,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**변수의 실행 순서**\n\n1. **변수 정의**: `name = '철수'` → 메모리에 공간 할당, '철수' 저장\n2. **변수 호출**: `print(name)` → 저장된 '철수' 값을 찾아옴\n3. **출력**: 화면에 '철수' 표시\n\n**메모리 구조**\n```\n변수명    |  메모리 주소  |  값\n---------|------------|--------\nname     |  0x1000   |  '철수'\nage      |  0x1008   |  15\ncity     |  0x1010   |  '서울'\n```\n\n**자료형의 중요성**\n- `age = 25` → int 타입 (숫자 계산 가능)\n- `age = '25'` → str 타입 (문자 취급, 계산 불가능)\n- 같은 값이어도 타입에 따라 동작이 다름\n\n**f-string 포매팅**\n```python\nname = '철수'\nage = 15\nprint(f'이름: {name}, 나이: {age}')\n# 출력: 이름: 철수, 나이: 15\n```"
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
                    "title": "📖 리스트와 문자열의 정의",
                    "type": "lesson",
                    "content": "**리스트(List)**: 여러 데이터를 순서대로 저장하는 컨테이너\n- 대괄호 `[]`로 생성\n- 같은 타입 또는 다른 타입의 데이터 저장 가능\n- 추가, 제거, 수정 가능 (가변)\n\n**기본 문법**:\n```python\ntasks = ['공부', '운동', '밥먹기']\n```\n\n**인덱싱**: 위치로 요소에 접근 (0부터 시작)\n```python\nprint(tasks[0])   # '공부' (첫 번째)\nprint(tasks[2])   # '밥먹기' (세 번째)\nprint(tasks[-1])  # '밥먹기' (마지막)\n```\n\n**리스트의 장점**\n1. 여러 데이터를 하나의 변수에 저장\n2. 반복문으로 일괄 처리 가능\n3. 동적으로 추가/제거 가능",
                    "code_example": "tasks = ['공부하기', '운동하기', '밥먹기']\nprint(tasks[0])\nprint(tasks[1])\nprint(tasks[2])\nprint(tasks[-1])"
                },
                {
                    "step": 2,
                    "title": "💡 실습 1: 리스트 생성 및 인덱싱",
                    "type": "lesson",
                    "content": "**실습**: 리스트를 만들고 특정 항목에 접근해보세요.\n\n**풀이 과정**:\n1. 리스트 생성: `fruits = ['딸기', '사과', '포도']`\n2. 첫 번째 항목: `fruits[0]` = '딸기'\n3. 세 번째 항목: `fruits[2]` = '포도'\n4. 마지막 항목: `fruits[-1]` = '포도'\n\n**전체 코드**:\n```python\nfruits = ['딸기', '사과', '포도']\nprint(fruits[0])\nprint(fruits[2])\n```\n\n**출력 결과**:\n```\n딸기\n포도\n```\n\n**이제 해보세요!**"
                },
                {
                    "step": 3,
                    "title": "📝 실습 2: 리스트 접근",
                    "type": "practice",
                    "task": "다음 리스트를 만드세요: colors = ['빨강', '노랑', '파랑', '초록']\n첫 번째와 마지막 요소를 출력하세요.",
                    "hint": "colors = ['빨강', '노랑', '파랑', '초록']\nprint(colors[0])\nprint(colors[-1])",
                    "expected_output": "빨강\n초록",
                    "validation": "exact_output"
                },
                {
                    "step": 4,
                    "title": "🚀 실습 3: 리스트 추가 및 길이 (조금 더 어려움)",
                    "type": "practice",
                    "task": "위의 colors 리스트에 '보라색'을 추가하고, 전체 항목 개수를 출력하세요.",
                    "hint": "colors.append('보라색')\nprint(len(colors))",
                    "expected_output": "5",
                    "validation": "exact_output"
                },
                {
                    "step": 5,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**리스트의 메모리 구조**\n\n리스트는 메모리에 순서대로 저장됩니다:\n```\n인덱스:    0      1      2       3\ntasks:  ['공부' '운동' '밥먹기' '쉬기']\n```\n\n**인덱싱 동작**\n- `tasks[0]` → 0번째 위치 → '공부'\n- `tasks[2]` → 2번째 위치 → '밥먹기'\n- `tasks[-1]` → 마지막(-1) → '쉬기'\n\n**리스트 메서드**\n```python\ntasks = ['a', 'b', 'c']\ntasks.append('d')      # 끝에 추가 → ['a', 'b', 'c', 'd']\ntasks.insert(0, 'x')   # 특정 위치에 삽입\ntasks.remove('a')      # 특정 값 제거\ntasks.pop(0)           # 인덱스로 제거\nlen(tasks)             # 길이 확인\n```\n\n**리스트 vs 문자열**\n- 리스트: 가변(수정 가능), 여러 항목 저장\n- 문자열: 불변(수정 불가), 텍스트만 저장"
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
            "app_description": "조건문을 사용해서 점수에 따른 학점을 계산하는 앱을 만들어봅시다!",
            "steps": [
                {
                    "step": 1,
                    "title": "📖 조건문의 정의와 사용",
                    "type": "lesson",
                    "content": "**조건문이란?** 특정 조건이 참/거짓인지 확인해서 다른 코드를 실행합니다.\n\n**비교 연산자**:\n- `==` 같다\n- `!=` 다르다\n- `>` 크다, `<` 작다\n- `>=` 크거나 같다, `<=` 작거나 같다\n\n**조건문 구조**:\n```python\nif 조건:\n    조건이 참일 때 실행\nelif 다른 조건:\n    다른 조건이 참일 때 실행\nelse:\n    위 조건 모두 거짓일 때 실행\n```\n\n**실제 예시**:\n```python\nage = 20\nif age >= 18:\n    print('성인입니다')\nelse:\n    print('미성년자입니다')\n```\n\n**조건문의 장점**:\n1. 프로그램이 상황에 따라 다르게 동작\n2. 사용자 입력에 따라 반응 가능\n3. 데이터 검증 가능",
                    "code_example": "score = 85\n\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelif score >= 70:\n    print('C')\nelse:\n    print('F')"
                },
                {
                    "step": 2,
                    "title": "💡 실습 1: 간단한 if 문",
                    "type": "lesson",
                    "content": "**실습**: 나이를 확인해서 성인 여부를 판단하는 프로그램\n\n**풀이 과정**:\n1. `age = 20` → 나이 변수 설정\n2. `if age >= 18:` → 18 이상인지 확인\n3. `print('성인입니다')` → 조건이 참이면 출력\n\n**전체 코드**:\n```python\nage = 20\nif age >= 18:\n    print('성인입니다')\n```\n\n**출력 결과**:\n```\n성인입니다\n```\n\n**이제 해보세요!**"
                },
                {
                    "step": 3,
                    "title": "📝 실습 2: if 조건문",
                    "type": "practice",
                    "task": "age = 25라고 하고, age가 18 이상이면 '성인입니다'를 출력하세요.",
                    "hint": "age = 25\nif age >= 18:\n    print('성인입니다')",
                    "expected_output": "성인입니다",
                    "validation": "exact_output"
                },
                {
                    "step": 4,
                    "title": "🚀 실습 3: elif를 사용한 다중 조건 (조금 더 어려움)",
                    "type": "practice",
                    "task": "score = 85라고 하고, 학점을 계산해서 출력하세요.\n- 90 이상: A\n- 80 이상: B\n- 70 이상: C\n- 그 외: F",
                    "hint": "score = 85\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelif score >= 70:\n    print('C')\nelse:\n    print('F')",
                    "expected_output": "B",
                    "validation": "exact_output"
                },
                {
                    "step": 5,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**조건문의 실행 순서**\n\n1. if 조건 확인 → True면 블록 실행 후 종료\n2. False면 elif 조건 확인 → True면 블록 실행 후 종료\n3. False면 다음 elif 확인\n4. 모두 False면 else 블록 실행\n\n**중요**: **처음 참인 조건만 실행**, 나머지는 무시됨\n\n```python\nscore = 85\nif score >= 90:     # False\n    print('A')\nelif score >= 80:   # True → 이것만 실행!\n    print('B')\nelif score >= 70:   # 확인 안 함\n    print('C')\nelse:               # 실행 안 됨\n    print('F')\n```\n\n**들여쓰기(Indentation)**:\n- Python은 들여쓰기로 블록을 구분\n- if 아래의 코드는 반드시 들여쓰기 필요\n- 들여쓰기 오류 = 문법 오류\n\n**논리 연산자**:\n```python\nage = 25\nif age >= 20 and age < 30:  # 둘 다 참이어야 참\n    print('20대입니다')\n\nif score >= 80 or score < 50:  # 하나라도 참이면 참\n    print('통과 또는 재시험')\n```"
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
            "app_description": "반복문을 사용해서 반복적인 작업을 자동화하는 앱을 만들어봅시다!",
            "steps": [
                {
                    "step": 1,
                    "title": "📖 반복문의 정의와 종류",
                    "type": "lesson",
                    "content": "**반복문이란?** 같은 코드를 여러 번 실행하는 문법입니다.\n\n**for 루프**: 횟수가 정해져 있을 때 사용\n```python\nfor i in range(5):  # 0, 1, 2, 3, 4\n    print(i)\n```\n\n**while 루프**: 조건이 거짓이 될 때까지 반복\n```python\ncount = 0\nwhile count < 5:    # count < 5이면 계속 반복\n    print(count)\n    count += 1\n```\n\n**range() 함수**:\n- `range(5)` → 0, 1, 2, 3, 4\n- `range(1, 6)` → 1, 2, 3, 4, 5\n- `range(1, 10, 2)` → 1, 3, 5, 7, 9 (스텝)\n\n**반복문의 장점**:\n1. 같은 코드 반복 작성 불필요\n2. 대량의 데이터 처리 가능\n3. 프로그램 코드를 간단하게",
                    "code_example": "# 1부터 5까지 출력\nfor i in range(1, 6):\n    print(i)\n\n# 2의 배수 찾기\nfor num in [1, 2, 3, 4, 5, 6]:\n    if num % 2 == 0:\n        print(num)"
                },
                {
                    "step": 2,
                    "title": "💡 실습 1: 기본 for 루프",
                    "type": "lesson",
                    "content": "**실습**: 1부터 5까지 출력하는 반복문\n\n**풀이 과정**:\n1. `range(1, 6)` → 1, 2, 3, 4, 5를 생성\n2. `for i in` → 각 숫자를 차례대로 i에 할당\n3. `print(i)` → 각 i를 출력\n4. 자동으로 반복됨\n\n**전체 코드**:\n```python\nfor i in range(1, 6):\n    print(i)\n```\n\n**출력 결과**:\n```\n1\n2\n3\n4\n5\n```\n\n**이제 해보세요!**"
                },
                {
                    "step": 3,
                    "title": "📝 실습 2: for 루프 사용",
                    "type": "practice",
                    "task": "1부터 5까지의 숫자를 출력하세요.",
                    "hint": "for i in range(1, 6):\n    print(i)",
                    "expected_output": "1\n2\n3\n4\n5",
                    "validation": "exact_output"
                },
                {
                    "step": 4,
                    "title": "🚀 실습 3: 문자열 포맷팅과 반복 (조금 더 어려움)",
                    "type": "practice",
                    "task": "2단 구구단을 출력하세요.\n형식: '2 × 1 = 2' 처럼 출력",
                    "hint": "for i in range(1, 10):\n    print(f'2 × {i} = {2*i}')",
                    "validation": "output_contains",
                    "validation_keywords": ["2 ×", "18"]
                },
                {
                    "step": 5,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**for 루프의 실행 순서**\n\n```python\nfor i in range(1, 6):\n    print(i)\n```\n\n1. range(1, 6)이 [1, 2, 3, 4, 5] 리스트를 생성\n2. 첫 번째 원소(1)를 i에 할당 → print(1)\n3. 두 번째 원소(2)를 i에 할당 → print(2)\n4. ... 반복\n5. 마지막 원소(5)를 i에 할당 → print(5)\n6. 리스트 끝 → 루프 종료\n\n**메모리 구조**:\n```\n반복 1: i = 1 → print(1)\n반복 2: i = 2 → print(2)\n반복 3: i = 3 → print(3)\n...\n```\n\n**range() 함수 상세**:\n- `range(5)`: 0부터 5 미만 (0, 1, 2, 3, 4)\n- `range(1, 6)`: 1부터 6 미만 (1, 2, 3, 4, 5)\n- `range(1, 10, 2)`: 1부터 10 미만, 2씩 증가 (1, 3, 5, 7, 9)\n\n**while 루프와의 차이**:\n- for: 정해진 횟수만큼 반복\n- while: 조건을 직접 제어\n\n```python\ncount = 0\nwhile count < 5:    # count가 5 미만이면 반복\n    print(count)\n    count += 1      # 필수! 무한루프 방지\n```"
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
            "app_description": "함수를 사용해서 간단한 계산 프로그램을 만들어봅시다!",
            "steps": [
                {
                    "step": 1,
                    "title": "📖 함수의 정의와 기능",
                    "type": "lesson",
                    "content": "**함수란?** 특정 작업을 수행하는 재사용 가능한 코드 묶음입니다.\n\n**함수의 기본 구조**:\n```python\ndef 함수명(매개변수):\n    # 함수의 본문 (작업 수행)\n    return 반환값\n```\n\n**실제 예시**:\n```python\ndef add(a, b):           # 함수 정의\n    return a + b         # a + b의 결과를 반환\n\nresult = add(5, 3)       # 함수 호출\nprint(result)            # 출력: 8\n```\n\n**용어 설명**:\n- **def**: 함수를 정의하는 키워드\n- **매개변수**: 함수가 받는 입력값 (a, b)\n- **반환값**: 함수가 돌려주는 결과\n\n**함수를 사용하는 이유**:\n1. 같은 코드를 반복해서 쓰지 않아도 됨\n2. 코드가 깔끔하고 읽기 쉬워짐\n3. 실수를 줄일 수 있음",
                    "code_example": "# 간단한 인사 함수\ndef greet(name):\n    return f'안녕하세요, {name}님!'\n\nmessage = greet('철수')\nprint(message)  # 출력: 안녕하세요, 철수님!\n\n# 계산 함수\ndef multiply(a, b):\n    return a * b\n\nresult = multiply(4, 5)\nprint(result)   # 출력: 20"
                },
                {
                    "step": 2,
                    "title": "💡 실습 1: 간단한 함수 만들기",
                    "type": "lesson",
                    "content": "**실습**: 두 숫자를 받아서 더한 값을 반환하는 add() 함수를 만들고 호출해보세요.\n\n**풀이 과정**:\n1. `def add(a, b):` - add 함수 정의, a와 b를 매개변수로 받음\n2. `return a + b` - a + b의 결과를 반환\n3. `add(5, 3)` - 함수 호출: 5와 3을 입력\n4. 함수가 8을 반환하고 print로 출력\n\n**전체 코드**:\n```python\ndef add(a, b):\n    return a + b\n\nresult = add(5, 3)\nprint(result)  # 출력: 8\n```\n\n**이제 해보세요!**"
                },
                {
                    "step": 3,
                    "title": "📝 실습 2: 덧셈 함수 만들기",
                    "type": "practice",
                    "task": "두 숫자를 받아서 더한 값을 반환하는 add() 함수를 만드세요.\nadd(7, 2)을 호출해서 결과를 출력하세요.",
                    "hint": "def add(a, b):\n    return a + b\n\nprint(add(7, 2))",
                    "expected_output": "9",
                    "validation": "exact_output"
                },
                {
                    "step": 4,
                    "title": "🚀 실습 3: 뺄셈 함수 만들기 (조금 더 어려움)",
                    "type": "practice",
                    "task": "두 숫자를 받아서 빼는 subtract() 함수를 만드세요.\nsubtract(10, 3)을 호출해서 결과를 출력하세요.",
                    "hint": "def subtract(a, b):\n    return a - b\n\nprint(subtract(10, 3))",
                    "expected_output": "7",
                    "validation": "exact_output"
                },
                {
                    "step": 5,
                    "title": "📚 작동원리 설명",
                    "type": "explanation",
                    "content": "**함수의 실행 순서**\n\n1. **정의 단계**: `def add(a, b):` → 함수를 메모리에 저장\n2. **호출 단계**: `add(5, 3)` → 함수 실행 시작\n3. **매개변수 대입**: a=5, b=3 으로 설정\n4. **본문 실행**: `return a + b` → `return 5 + 3` → `return 8`\n5. **반환**: 8을 호출한 곳으로 전달\n6. **출력**: `print(8)` → 화면에 8 출력\n\n**매개변수와 인자의 차이**\n- **매개변수**: 함수 정의할 때 사용 (a, b)\n- **인자(인수)**: 함수 호출할 때 전달하는 실제 값 (5, 3)\n\n```python\ndef add(a, b):      # a, b는 매개변수\n    return a + b\n\nadd(5, 3)           # 5, 3은 인자\n```\n\n**함수의 장점**\n1. **코드 재사용**: add 함수를 여러 번 호출 가능\n2. **가독성**: add(10, 20) 이 명확함\n3. **유지보수**: 함수 내용만 수정하면 모든 호출에 반영됨"
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
