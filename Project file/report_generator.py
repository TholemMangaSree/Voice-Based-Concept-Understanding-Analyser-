from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_report(transcript, reference, score, feedback, analysis,fluency_score,fluency_grade,fillers):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Voice-Based Concept Understanding Analyser Report</b>", styles["Title"]))
    story.append(Paragraph(f"<b>Transcript:</b> {transcript}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Reference:</b> {reference}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Similarity Score:</b> {score:.2f}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Feedback:</b> {feedback}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Duration:</b> {analysis['duration']} seconds", styles["BodyText"]))
    story.append(Paragraph(f"<b>Average RMS:</b> {analysis['average_rms']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Pause Ratio:</b> {analysis['pause_ratio']}", styles["BodyText"]))
    story.append(Paragraph("<b>Speech Fluency Analysis</b>", styles["BodyText"]))
    story.append(Paragraph(f"<b>Fluency Score:</b> {fluency_score}/100", styles["BodyText"]))
    story.append(Paragraph(f"<b>Grade:</b> {fluency_grade}", styles["BodyText"]))
    story.append(Paragraph("<b>Filler Word Analysis</b>", styles["BodyText"]))
    story.append(Paragraph(f"<b>Total Filler Words:</b> {fillers['total_fillers']}", styles["BodyText"]))

    if fillers["total_fillers"] > 0:
        for word, count in fillers["details"].items():
            if count > 0:
                story.append(
                    Paragraph(f"{word}: {count}", styles["BodyText"])
                )
    else:
        story.append(
            Paragraph("No filler words detected. Your speech is clear.", styles["BodyText"])
        )

    doc.build(story)

    return "report.pdf"