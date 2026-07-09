def evaluate_fluency(pause_ratio, avg_rms, filler_count):

    score = 100

    # Penalize long pauses
    score -= pause_ratio * 40

    # Penalize filler words
    score -= filler_count * 5

    # Penalize low speaking energy
    if avg_rms < 0.03:
        score -= 15
    elif avg_rms < 0.06:
        score -= 8

    score = max(0, min(100, int(score)))

    if score >= 85:
        grade = "🟢 Confident Speaker"
    elif score >= 70:
        grade = "🟡 Good Fluency"
    elif score >= 50:
        grade = "🟠 Moderate Hesitation"
    else:
        grade = "🔴 Hesitant Speaker"

    return score, grade