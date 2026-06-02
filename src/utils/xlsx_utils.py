import logging
import pandas as pd

from PySide6.QtGui import QTextDocument
from PySide6.QtPrintSupport import QPrinter

from .utils import Utils


class XLSXUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing XLSXUtils...")

    @staticmethod
    def xlsx_to_pdf(source):
        output = Utils.output_file_name("xlsx_to_pdf", "pdf")
        Utils.creer_fichier(output)

        df = pd.read_excel(source)

        html_table = df.to_html(index=False)

        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 10pt;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid #999;
                    padding: 4px;
                }}
                th {{
                    background-color: #eee;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            {html_table}
        </body>
        </html>
        """

        document = QTextDocument()
        document.setHtml(html)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(str(output))

        document.print(printer)

        return output

    @staticmethod
    def xlsx_to_csv(source):
        output = Utils.output_file_name("xlsx_to_csv", "csv")
        Utils.creer_fichier(output)

        df = pd.read_excel(source)
        df.to_csv(output, index=False)

        return output