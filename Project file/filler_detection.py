def detect_fillers(transcript):
    filler_words = ["um", "uh", "like", "you know", "hmm", "ah"]

    transcript = transcript.lower()

    filler_count = {}
    total = 0

    for word in filler_words:
        count = transcript.count(word)
        filler_count[word] = count
        total += count

    return {
        "total_fillers": total,
        "details": filler_count
    }