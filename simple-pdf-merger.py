from os import walk, path
from pathlib import Path
from glob import glob
from PyInquirer import style_from_dict, Token, prompt, Separator
from PyPDF2 import PdfFileReader, PdfFileWriter

outputPath = str(Path(__file__).parent.absolute())
outFilename = 'out.pdf'

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def readAllFiles():
    sourcePath = askForSourcePath()
    paths = [y for x in walk(sourcePath)
             for y in glob(path.join(x[0], '*.pdf'))]
    return paths


def getFileListForQuestions():
    paths = readAllFiles()
    filelist = []
    for path in paths:
        p = path.split('/')
        filename = p[len(p) - 1]
        filelist.append({
            'name': filename,
            'value': path
        })
    return filelist


def generatePDF(paths):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    outputFileName = outputPath + '/' + outFilename
    with open(outputFileName, 'wb') as out:
        pdf_writer.write(out)


def askForSourcePath():
    sourcePathQuestion = [
        {
            'type': 'input',
            'message': 'Please type in the source path:',
            'name': 'path'
        }
    ]
    sourcePath = prompt(sourcePathQuestion, style=style)
    return sourcePath['path']


def askForPdfSelection():
    filelist = getFileListForQuestions()

    diplomaQuestions = [
        {
            'type': 'checkbox',
            'message': 'Select PDFs',
            'name': 'pdfs',
            'choices': filelist,
            'validate': lambda answer: 'Chose your PDFs to merge'
            if len(answer) == 0 else True
        }
    ]

    files = prompt(diplomaQuestions, style=style)
    return files['pdfs']


if __name__ == '__main__':
    paths = askForPdfSelection()

    if paths:
        generatePDF(paths)
