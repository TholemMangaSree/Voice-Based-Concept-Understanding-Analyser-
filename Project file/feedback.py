def generate_feedback(score):
    if score >= 0.80:
        return " Excellent! Your answer matches the reference very well."

    elif score >= 0.60:
        return " Good! Your answer is mostly correct."

    elif score >= 0.40:
        return " Fair. Some concepts match, but improvement is needed."

    else:
        return " Needs Improvement. Please practice and try again."