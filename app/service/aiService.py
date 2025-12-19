from decouple import config
from openai import OpenAI
from fastapi import HTTPException, status

from app.db.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
    AIAssignmentCheckRequest,
    AIAssignmentCheckResponse,
)


class AIService:
    def __init__(self):
        api_key = config("OPENAI_API_KEY", default="")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"

    def chat(self, request: AIChatRequest) -> AIChatResponse:
        prompt = f"""You are an AI tutor on an online course platform.

Your task:
- Explain concepts clearly and simply
- Help students understand the lesson

Course: {request.course_title}
Lesson: {request.lesson_title}

Rules:
- Act like a teacher
- Use simple examples
- be communicative
- always

Student question:
{request.question}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI tutor for an online learning platform.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=500,
            )

            answer = response.choices[0].message.content
            return AIChatResponse(answer=answer)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error communicating with AI service: {str(e)}",
            )

    def check_assignment(
        self, request: AIAssignmentCheckRequest
    ) -> AIAssignmentCheckResponse:
        prompt = f"""You are an AI tutor on an online course platform.
Your task:
- Check if the student's answer to the assignment is correct.
- If the answer is incorrect or incomplete, explain the mistake and show the correct solution.
- If the student clearly "doesn't know" (e.g. answers 'не знаю', 'I don't know', empty answer),
  then focus on step-by-step explanation and hints instead of just giving the final answer.

VERY IMPORTANT OUTPUT FORMAT (STRICT):
- First line MUST be exactly one word: either CORRECT or INCORRECT (in English, uppercase).
- After the first line, give a detailed explanation in Russian.
- If the answer is INCORRECT, at the end of your explanation show the correct solution / пример правильного ответа.

Course: {request.course_title}
Lesson: {request.lesson_title}

Assignment title: {request.assignment_title}
Assignment instructions: {request.assignment_instructions}

Student answer:
{request.user_answer}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict but friendly AI tutor. "
                            "You must follow the output format instructions exactly."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=800,
            )

            full_answer = (response.choices[0].message.content or "").strip()
            lines = full_answer.splitlines()
            first_line = lines[0].strip().upper() if lines else ""
            explanation = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

            is_correct = first_line.startswith("CORRECT")

            return AIAssignmentCheckResponse(
                is_correct=is_correct,
                explanation=explanation or full_answer,
                suggested_answer=None,
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error communicating with AI service (assignment check): {str(e)}",
            )

