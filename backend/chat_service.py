from retriever import retrieve_relevant_chunks
from prompt_templates import teacher_prompt
from sanitizer import sanitize_sources
from llm import generate_answer


def format_history(history):
    """
    Convert chat history into a readable dialogue string for the LLM
    """
    if not history:
        return ""

    lines = []
    for h in history:
        speaker = "Student" if h.role == "student" else "Teacher"
        lines.append(f"{speaker}: {h.content}")

    return "\n".join(lines)


def chat(question, history, vector_store, chunks):
    # ✅ Use history sent from frontend
    past_dialogue = format_history(history)

    # 🔍 Retrieve relevant chunks
    retrieved_chunks = retrieve_relevant_chunks(
        question=question,
        chunks=chunks,
        vector_store=vector_store
    )

    if not retrieved_chunks:
        return {
            "teacher": "This topic is not covered in the provided material.",
            "student": "",
            "teacher_followup": "",
            "sources": []
        }

    # Limit context
    retrieved_chunks = retrieved_chunks[:2]

    context = "\n\n".join(
        f"Page {c['page']}: {c['text']}" for c in retrieved_chunks
    )

    # 🧠 Build prompt
    prompt = teacher_prompt(
        context=context,
        question=question,
        history=past_dialogue
    )

    print("\n========== GEMINI PROMPT ==========\n")
    print(prompt)
    print("\n==================================\n")

    # 🤖 Generate answer (NON-STREAMING → join generator safely)
    raw_answer = "".join(generate_answer(prompt))

    # 🧩 Parse teacher-student dialogue
    teacher, student, teacher_followup = parse_dialogue(raw_answer)

    return {
        "teacher": teacher,
        "student": student,
        "teacher_followup": teacher_followup,
        "sources": sanitize_sources(retrieved_chunks)
    }


def parse_dialogue(text: str):
    teacher = ""
    student = ""
    followup = ""

    if "Student Follow-up Question:" in text:
        t, rest = text.split("Student Follow-up Question:", 1)
        teacher = t.replace("Teacher Explanation:", "").strip()

        if "Teacher Clarification:" in rest:
            s, f = rest.split("Teacher Clarification:", 1)
            student = s.strip()
            followup = f.strip()
        else:
            student = rest.strip()
    else:
        teacher = text.strip()

    return teacher, student, followup
