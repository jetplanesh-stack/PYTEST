"""Claude API로 문제를 출제하고 채점/피드백을 받는 모듈."""

import os
import subprocess
import sys
import tempfile

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")  # 프록시에서 제공하는 모델
client = anthropic.Anthropic()  # ANTHROPIC_API_KEY / ANTHROPIC_BASE_URL 은 .env 에서 읽음

DIFFICULTY_GUIDE = {
    "초급": "변수, 조건문, 반복문, 리스트/문자열 기본 조작 수준. 5~15줄이면 풀 수 있는 문제.",
    "중급": "딕셔너리/집합, 함수, 정렬, 컴프리헨션, 간단한 알고리즘(투 포인터, 누적합 등) 수준.",
    "고난도": "자료구조와 알고리즘(DP, 그래프 탐색, 이분 탐색, 힙 등)이 필요하고 효율성이 중요한 문제.",
}


# ---------- 응답 스키마 ----------

class MultipleChoiceProblem(BaseModel):
    title: str
    situation: str          # 문제 상황 설명
    expected_output: str    # 정답 코드를 실행했을 때 나와야 하는 출력
    choices: list[str]      # 보기 4개 (각각 파이썬 코드)
    answer_index: int       # 정답 보기 번호 (0~3)
    explanation: str        # 해설


class SubjectiveProblem(BaseModel):
    title: str
    situation: str
    input_description: str  # 코드 안에서 사용할 입력 데이터 설명 (코드에 직접 작성)
    expected_output: str    # print 로 출력해야 하는 정확한 결과
    reference_solution: str # 모범 답안 (가장 효율적인 풀이)


class Grading(BaseModel):
    grade: int              # 1(가장 효율적) ~ 9(비효율적)
    time_complexity: str
    feedback: str           # 잘한 점 / 아쉬운 점
    better_approach: str    # 더 효율적인 방법 설명
    better_code: str        # 개선된 코드 예시


class WrongFeedback(BaseModel):
    reason: str             # 왜 결과가 다른지
    hint: str               # 다시 풀기 위한 힌트 (정답 코드는 주지 않음)


# ---------- 출제 ----------

SYSTEM = (
    "너는 파이썬 코딩 시험 출제자이자 채점관이다. 모든 설명은 한국어로 작성한다. "
    "문제는 표준 라이브러리만으로 풀 수 있어야 하고, input() 없이 코드 안에 데이터를 직접 정의해 "
    "print 로 결과를 출력하는 형태여야 한다. 출력 결과는 실행할 때마다 같아야 한다(난수, 시간 사용 금지)."
)


def _parse(prompt: str, schema: type[BaseModel]):
    response = client.messages.parse(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
        output_format=schema,
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("AI가 요청을 거절했습니다. 다시 시도해 주세요.")
    return response.parsed_output


def generate_problem(kind: str, difficulty: str, avoid_titles: list[str] | None = None):
    avoid = ""
    if avoid_titles:
        avoid = "\n이미 출제된 문제와 겹치지 않게 해라: " + ", ".join(avoid_titles[-10:])

    if kind == "객관식":
        prompt = (
            f"난이도: {difficulty} ({DIFFICULTY_GUIDE[difficulty]})\n"
            "파이썬으로 해결할 수 있는 현실적인 상황을 하나 제시하고, 그 상황의 목표 출력(expected_output)을 정해라. "
            "보기 4개는 각각 완성된 파이썬 코드이며, 그중 정확히 하나만 실행 결과가 expected_output 과 일치해야 한다. "
            "나머지 보기는 그럴듯하지만 오프바이원, 정렬 기준, 자료형 실수 등으로 다른 결과를 내야 한다."
            + avoid
        )
        problem = _parse(prompt, MultipleChoiceProblem)
        _verify_multiple_choice(problem)
        return problem

    prompt = (
        f"난이도: {difficulty} ({DIFFICULTY_GUIDE[difficulty]})\n"
        "파이썬으로 해결할 수 있는 현실적인 상황을 하나 제시하는 주관식 문제를 만들어라. "
        "input_description 에는 학생이 코드에 그대로 복사해 쓸 입력 데이터(파이썬 변수 정의)를 포함해라. "
        "expected_output 은 reference_solution 을 실행했을 때의 정확한 출력이어야 한다. "
        "풀이 방법에 따라 효율성 차이가 드러나는 문제가 좋다."
        + avoid
    )
    problem = _parse(prompt, SubjectiveProblem)
    # 모범 답안을 실제로 실행해 expected_output 을 확정한다.
    ok, out = run_code(problem.reference_solution)
    if ok and out.strip():
        problem.expected_output = out.strip()
    return problem


def _verify_multiple_choice(problem: MultipleChoiceProblem):
    """보기를 실제로 실행해서 정답 번호와 기대 출력을 실행 결과에 맞춘다."""
    ok, out = run_code(problem.choices[problem.answer_index])
    if ok and out.strip():
        problem.expected_output = out.strip()
    matches = [i for i, code in enumerate(problem.choices)
               if (r := run_code(code))[0] and r[1].strip() == problem.expected_output]
    if len(matches) == 1:
        problem.answer_index = matches[0]


# ---------- 실행 / 채점 ----------

def run_code(code: str, timeout: float = 5.0) -> tuple[bool, str]:
    """코드를 별도 프로세스에서 실행하고 (성공 여부, 출력/에러) 를 돌려준다."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=timeout, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, f"시간 초과 ({timeout}초) - 무한 루프이거나 너무 느린 코드입니다."
    finally:
        os.remove(path)


def outputs_match(actual: str, expected: str) -> bool:
    norm = lambda s: "\n".join(line.rstrip() for line in s.strip().splitlines())
    return norm(actual) == norm(expected)


def grade_solution(problem: SubjectiveProblem, code: str) -> Grading:
    prompt = (
        f"[문제]\n{problem.situation}\n\n[입력]\n{problem.input_description}\n\n"
        f"[모범 답안]\n```python\n{problem.reference_solution}\n```\n\n"
        f"[학생 코드 - 정답 출력 확인됨]\n```python\n{code}\n```\n\n"
        "학생 코드의 효율성(시간/공간 복잡도, 파이썬다운 표현, 불필요한 연산)을 평가해 "
        "1~9등급을 매겨라. 1등급이 가장 효율적이고 9등급이 가장 비효율적이다. "
        "모범 답안 수준이면 1~2등급. 더 효율적인 방법과 개선 코드를 제시해라. "
        "이미 최적이라면 better_approach 에 그렇다고 쓰고 better_code 는 학생 코드를 다듬은 버전으로 해라."
    )
    grading = _parse(prompt, Grading)
    grading.grade = min(9, max(1, grading.grade))
    return grading


def explain_wrong(problem: SubjectiveProblem, code: str, actual: str) -> WrongFeedback:
    prompt = (
        f"[문제]\n{problem.situation}\n\n[입력]\n{problem.input_description}\n\n"
        f"[기대 출력]\n{problem.expected_output}\n\n"
        f"[학생 코드]\n```python\n{code}\n```\n\n[실제 실행 결과]\n{actual}\n\n"
        "학생 코드가 왜 틀렸는지 설명하고 다시 풀 수 있도록 힌트를 줘라. 정답 코드를 통째로 알려주지는 마라."
    )
    return _parse(prompt, WrongFeedback)
