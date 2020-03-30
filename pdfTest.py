from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf


def read_pdf(fileName):
    with open(fileName, "rb") as pdf:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()

        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        process_pdf(rsrcmgr, device, pdf)
        device.close()
        content = retstr.getvalue()
        retstr.close()

        lines = str(content).split("\n")
        s=' '.join(lines)
        s=s.replace('  ',' ')
        s=s.replace('  ',' ')
        return s
print(read_pdf('/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/UserData/2resume.pdf'))