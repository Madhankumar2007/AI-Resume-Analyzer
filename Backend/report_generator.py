from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether
)


def clean_text(value):
    if value is None:
        return "Not available"

    return str(value)


def generate_pdf_report(result):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#234A9F"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#234A9F"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    normal_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14,
        spaceAfter=5
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11
    )

    story = []

    match_result = result.get("match_result", {})
    ats = result.get("ats_analysis", {})
    recommendations = result.get("recommendations", [])

    match_percentage = match_result.get("match_percentage", 0)
    semantic_score = result.get("semantic_similarity", 0)
    ats_score = ats.get("completeness_score", 0)

    # ATS keyword match percentage
    matched_keywords = ats.get("matched_keywords", [])
    missing_keywords = ats.get("missing_keywords", [])

    total_ats_keywords = (
        len(matched_keywords) + len(missing_keywords)
    )

    if total_ats_keywords > 0:
        ats_keyword_score = (
            len(matched_keywords) / total_ats_keywords
        ) * 100
    else:
        ats_keyword_score = 0

    # Title
    story.append(
        Paragraph("AI Resume Analyzer Report", title_style)
    )

    story.append(Spacer(1, 10))

    # Overall scores
    story.append(
        Paragraph("Overall Analysis Scores", heading_style)
    )

    score_data = [
        ["Metric", "Result"],
        ["Resume Keyword Match", f"{match_percentage}%"],
        ["Semantic Similarity (Sentence-BERT)", f"{semantic_score}%"],
        ["ATS Section Completeness", f"{ats_score}%"],
        ["ATS Keyword Match", f"{round(ats_keyword_score, 2)}%"],
        ["Total Resume Skills", str(result.get("total_skills", 0))],
        ["Matched Skills", str(len(match_result.get("matched_skills", [])))],
        ["Missing Skills", str(len(match_result.get("missing_skills", [])))]
    ]

    score_table = Table(
        score_data,
        colWidths=[3.8 * inch, 2.0 * inch],
        repeatRows=1
    )

    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#234A9F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F3F6FC")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    story.append(score_table)

    # Matched skills
    story.append(
        Paragraph("Matched Skills", heading_style)
    )

    matched_skills = match_result.get("matched_skills", [])

    story.append(
        Paragraph(
            clean_text(
                ", ".join(matched_skills)
                if matched_skills else "No matched skills found"
            ),
            normal_style
        )
    )

    # Missing skills
    story.append(
        Paragraph("Missing Skills", heading_style)
    )

    missing_skills = match_result.get("missing_skills", [])

    story.append(
        Paragraph(
            clean_text(
                ", ".join(missing_skills)
                if missing_skills else "No missing skills"
            ),
            normal_style
        )
    )

    # ATS section analysis
    story.append(
        Paragraph("ATS Resume Section Analysis", heading_style)
    )

    detected_sections = ats.get("detected_sections", [])
    missing_sections = ats.get("missing_sections", [])

    story.append(
        Paragraph("<b>Detected Sections:</b>", normal_style)
    )

    story.append(
        Paragraph(
            clean_text(
                ", ".join(detected_sections)
                if detected_sections else "None detected"
            ),
            normal_style
        )
    )

    story.append(
        Paragraph("<b>Missing Sections:</b>", normal_style)
    )

    story.append(
        Paragraph(
            clean_text(
                ", ".join(missing_sections)
                if missing_sections else "None"
            ),
            normal_style
        )
    )

    # ATS keyword analysis
    story.append(
        Paragraph("ATS Keyword Analysis", heading_style)
    )

    story.append(
        Paragraph("<b>Matched Technical Keywords:</b>", normal_style)
    )

    story.append(
        Paragraph(
            clean_text(
                ", ".join(matched_keywords)
                if matched_keywords else "None"
            ),
            normal_style
        )
    )

    story.append(
        Paragraph("<b>Missing Technical Keywords:</b>", normal_style)
    )

    story.append(
        Paragraph(
            clean_text(
                ", ".join(missing_keywords)
                if missing_keywords else "None"
            ),
            normal_style
        )
    )

    # ATS suggestions
    suggestions = ats.get("suggestions", [])

    if suggestions:
        story.append(
            Paragraph("ATS Improvement Suggestions", heading_style)
        )

        for suggestion in suggestions:
            story.append(
                Paragraph(
                    "• " + clean_text(suggestion),
                    normal_style
                )
            )

    # Skill recommendations
    story.append(
        Paragraph("Resume Improvement Recommendations", heading_style)
    )

    if recommendations:

        for recommendation in recommendations:

            skill = clean_text(
                recommendation.get("skill", "Skill")
            )

            description = clean_text(
                recommendation.get("description", "")
            )

            difficulty = clean_text(
                recommendation.get("difficulty", "Not specified")
            )

            topics = recommendation.get("topics", [])

            recommendation_content = [
                Paragraph(f"<b>{skill}</b>", normal_style),
                Paragraph(description, normal_style),
                Paragraph(
                    f"<b>Difficulty:</b> {difficulty}",
                    normal_style
                ),
                Paragraph(
                    "<b>Recommended Topics:</b> "
                    + clean_text(
                        ", ".join(topics)
                        if topics else "Not specified"
                    ),
                    normal_style
                ),
                Spacer(1, 8)
            ]

            story.append(
                KeepTogether(recommendation_content)
            )

    else:
        story.append(
            Paragraph("No recommendations available.", normal_style)
        )

    # Disclaimer
    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Disclaimer:</b> These scores are generated using "
            "automated keyword matching, semantic similarity and "
            "rule-based resume section analysis. They are guidance "
            "indicators, not a guarantee of ATS acceptance or job selection.",
            small_style
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer