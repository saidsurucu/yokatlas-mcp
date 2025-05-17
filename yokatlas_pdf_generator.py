import os
import datetime
import tempfile
from io import BytesIO
import base64

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm


def generate_pdf(
    data: dict,
    report_type: str,
    title: str = "YOKATLAS Raporu",
    language: str = "tr",  # 'tr' for Turkish, 'en' for English (future support)
    save_to_local: bool = False,
    output_dir: str = None,
) -> dict:
    """
    Generates a formatted PDF report from YOKATLAS data.

    Parameters:
    - data: The data dictionary from one of the YOKATLAS search or details functions
    - report_type: Type of report ('bachelor_search', 'associate_search', 'bachelor_details', 'associate_details')
    - title: Custom title for the report
    - language: Report language ('tr' for Turkish, 'en' for English - future)
    - save_to_local: If True, saves PDF to local file system
    - output_dir: Directory to save the PDF (if None, uses system temp directory)

    Returns:
    - A dictionary containing the Base64 encoded PDF content, filename, and local path if saved
    """
    try:
        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        heading_style = styles["Heading2"]
        normal_style = styles["Normal"]

        turkish_style = ParagraphStyle(
            "TurkishStyle",
            parent=normal_style,
            fontName="Helvetica",
            fontSize=10,
            leading=12,
        )

        elements = []

        elements.append(Paragraph(title, title_style))
        current_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        elements.append(Paragraph(f"Oluşturulma Tarihi: {current_date}", turkish_style))
        elements.append(Spacer(1, 0.5 * cm))

        # Process data based on report type
        if report_type == "bachelor_search" or report_type == "associate_search":
            if "results" in data and isinstance(data["results"], list):
                total_programs = len(data["results"])
                elements.append(
                    Paragraph(f"Toplam Program Sayısı: {total_programs}", heading_style)
                )
                elements.append(Spacer(1, 0.3 * cm))

                table_data = []

                if report_type == "bachelor_search":
                    headers = [
                        "Program Kodu",
                        "Üniversite",
                        "Program",
                        "Şehir",
                        "Puan Türü",
                        "Taban Puanı",
                        "Başarı Sırası",
                    ]
                    table_data.append(headers)

                    for program in data["results"]:
                        row = [
                            program.get("program_kodu", ""),
                            program.get("universite", ""),
                            program.get("program_adi", ""),
                            program.get("sehir", ""),
                            program.get("puan_turu", "").upper(),
                            program.get("taban_puani", ""),
                            program.get("basari_sirasi", ""),
                        ]
                        table_data.append(row)
                else:  # associate_search
                    headers = [
                        "Program Kodu",
                        "Üniversite",
                        "Program",
                        "Şehir",
                        "Taban Puanı",
                    ]
                    table_data.append(headers)

                    for program in data["results"]:
                        row = [
                            program.get("program_kodu", ""),
                            program.get("universite", ""),
                            program.get("program_adi", ""),
                            program.get("sehir", ""),
                            program.get("taban_puani", ""),
                        ]
                        table_data.append(row)

                table = Table(table_data, repeatRows=1)
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                            (
                                "ROWBACKGROUNDS",
                                (0, 1),
                                (-1, -1),
                                [colors.white, colors.lightgrey],
                            ),
                        ]
                    )
                )

                elements.append(table)

        elif report_type == "bachelor_details" or report_type == "associate_details":
            if "genel" in data and isinstance(data["genel"], dict):
                genel = data["genel"]
                program_name = genel.get("program_adi", "Program Bilgisi")
                university = genel.get("universite_adi", "")

                elements.append(
                    Paragraph(f"{university} - {program_name}", heading_style)
                )
                elements.append(Spacer(1, 0.3 * cm))

                elements.append(Paragraph("Genel Bilgiler", styles["Heading3"]))

                general_info = [
                    ["Üniversite", university],
                    ["Program", genel.get("program_adi", "")],
                    ["Fakülte", genel.get("fakulte", "")],
                    ["Şehir", genel.get("sehir", "")],
                    ["Program Türü", genel.get("program_turu", "")],
                    ["Öğretim Türü", genel.get("ogretim_turu", "")],
                    ["Burs/Ücret", genel.get("ucret_burs", "")],
                ]

                gen_table = Table(general_info)
                gen_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (0, -1), colors.lightblue),
                            ("TEXTCOLOR", (0, 0), (0, -1), colors.black),
                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ]
                    )
                )
                elements.append(gen_table)
                elements.append(Spacer(1, 0.5 * cm))

                if "kontenjan_yerlesen" in data:
                    elements.append(
                        Paragraph("Kontenjan ve Yerleşme Bilgileri", styles["Heading3"])
                    )
                    kontenjan = data["kontenjan_yerlesen"]

                    if isinstance(kontenjan, dict):
                        kontenjan_info = [
                            ["Kontenjan", kontenjan.get("kontenjan", "")],
                            ["Yerleşen", kontenjan.get("yerlesen", "")],
                            ["Doluluk Oranı", f"{kontenjan.get('doluluk_orani', '')}%"],
                        ]

                        kon_table = Table(kontenjan_info)
                        kon_table.setStyle(
                            TableStyle(
                                [
                                    ("BACKGROUND", (0, 0), (0, -1), colors.lightblue),
                                    ("TEXTCOLOR", (0, 0), (0, -1), colors.black),
                                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                                ]
                            )
                        )
                        elements.append(kon_table)
                        elements.append(Spacer(1, 0.5 * cm))

                if "taban_puan_bilgileri" in data:
                    elements.append(
                        Paragraph("Taban Puan ve Başarı Sırası", styles["Heading3"])
                    )
                    taban = data["taban_puan_bilgileri"]

                    if isinstance(taban, dict):
                        puan_info = [
                            ["Puan Türü", taban.get("puan_turu", "").upper()],
                            ["Taban Puanı", taban.get("taban_puani", "")],
                            ["Tavan Puanı", taban.get("tavan_puani", "")],
                            ["Başarı Sırası", taban.get("basari_sirasi", "")],
                        ]

                        puan_table = Table(puan_info)
                        puan_table.setStyle(
                            TableStyle(
                                [
                                    ("BACKGROUND", (0, 0), (0, -1), colors.lightblue),
                                    ("TEXTCOLOR", (0, 0), (0, -1), colors.black),
                                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                                ]
                            )
                        )
                        elements.append(puan_table)

        doc.build(elements)

        pdf_data = buffer.getvalue()

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"YOKATLAS_Rapor_{timestamp}.pdf"

        local_path = None
        if save_to_local:
            if output_dir is None:
                output_dir = tempfile.gettempdir()

            os.makedirs(output_dir, exist_ok=True)

            local_path = os.path.join(output_dir, filename)
            with open(local_path, "wb") as f:
                f.write(pdf_data)

        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
        buffer.close()

        return {
            "success": True,
            "filename": filename,
            "pdf_base64": pdf_base64,
            "local_path": local_path,
            "message": "PDF rapor başarıyla oluşturuldu"
            + (f" ve {local_path} konumuna kaydedildi." if local_path else "."),
        }

    except Exception as e:
        error_msg = str(e)
        print(f"Error in generate_pdf: {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "message": "PDF rapor oluşturma sırasında hata oluştu.",
        }


def get_downloads_folder():
    """Returns the downloads folder path for the current user."""
    home = os.path.expanduser("~")
    if os.name == "nt":
        return os.path.join(home, "Downloads")
    elif os.name == "posix":
        return os.path.join(home, "Downloads")
    else:
        return home
