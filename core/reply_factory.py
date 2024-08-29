
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question in the session.
    '''
    if current_question_id is None:
        return False, "No question to answer."

    # Save the answer to the session
    session["answers"] = session.get("answers", {})
    session["answers"][current_question_id] = answer
    session.save()

    return True, ""


def get_next_question(current_question_id):
   if current_question_id is None:
        # Start from the first question if there's no current question
        return PYTHON_QUESTION_LIST[0][0], 0

    # Move to the next question
        next_question_id = current_question_id + 1
        if next_question_id < len(PYTHON_QUESTION_LIST):
            return PYTHON_QUESTION_LIST[next_question_id][0], next_question_id
        else:
        # No more questions left
            return None, None


def generate_final_response(session):
    
    answers = session.get("answers", {})
    score = 0

    # Calculate the score based on correct answers
    for question_id, (question, correct_answer) in enumerate(PYTHON_QUESTION_LIST):
        user_answer = answers.get(question_id)
        if user_answer and user_answer.strip().lower() == correct_answer.strip().lower():
            score += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    final_response = (
        f"You've completed the quiz! Your score is {score} out of {total_questions}."
    )

    return final_response
