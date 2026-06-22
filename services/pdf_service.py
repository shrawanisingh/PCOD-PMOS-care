from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(report, filename="ovacare_report.pdf"):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("OvaCare AI Assessment", styles["Title"])
    )

    story.append(Spacer(1, 20))

    for line in report.split("\n"):
        story.append(
            Paragraph(line, styles["Normal"])
        )

    doc.build(story)

    return filename