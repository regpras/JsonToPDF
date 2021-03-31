import re
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from textwrap import wrap
from reportlab.platypus import Image

xstart = 10
ystart = 800

class msgtemplete:
    id = 0
    type = ''
    date = ''
    fromname = ''
    from_id = 0
    author = ''
    reply_to_message_id = 0
    photo = ''
    width = 0
    height = 0
    text = 0

ID = "\"id\": "
TYPE = "\"type\": "
DATE = "\"date\": "
FROM = "\"from\": "
FROMID = "\"from_id\": "
AUTHOR = "\"author\": "
RID = "\"reply_to_message_id\": "
PHOTO = "\"photo\": "
WIDTH = "\"width\": "
HEIGHT = "\"height\": "
TEXT = "\"text\": "

basedatapath = r'C:\Prasanna\Python\Data'
jsonfilepath = r'C:\Prasanna\Python\Data\result.json'
#jsonfilepath = r'C:\Prasanna\Python\messaging-chat-parser-master\data\test.json'
parsedfilepath = r'C:\Prasanna\Python\Data\parsedresult.txt'
pdfpath = r'C:\Prasanna\Python\Data\TIC.pdf'
wfp = open(parsedfilepath, 'w', errors='ignore')

# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True

# document.add_heading('Heading, level 1', level=1)
# document.add_paragraph('Intense quote', style='Intense Quote')
#
# document.add_paragraph(
#     'first item in unordered list', style='List Bullet'
# )
# document.add_paragraph(
#     'first item in ordered list', style='List Number'
# )
#
# document.add_picture('Nifty23May_WD.png', width=Inches(1.25))

# records = (
#     (3, '101', 'Spam'),
#     (7, '422', 'Eggs'),
#     (4, '631', 'Spam, spam, eggs, and spam')
# )
#
# table = document.add_table(rows=1, cols=3)
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Qty'
# hdr_cells[1].text = 'Id'
# hdr_cells[2].text = 'Desc'
# for qty, id, desc in records:
#     row_cells = table.add_row().cells
#     row_cells[0].text = str(qty)
#     row_cells[1].text = id
#     row_cells[2].text = desc

def createdocx(allmsglist):

    document = Document()

    document.add_heading('Document Title', 0)

    try:
        for msg in allmsglist:
            p = document.add_paragraph(msg.text)

            #document.add_page_break()
        document.add_picture('Nifty23May_WD.png')
        document.save('demo.docx')
    except Exception as e:
        print(e)


def createpdf(allmsglist):
    canvas = Canvas(pdfpath)#,  pagesize=letter
    canvas.setFont("Times-Roman", 12)
    #textobject = canvas.beginText()
    #textobject.setTextOrigin(10, 730)
    #textobject.setFont("Helvetica", 12)
    linecount = 0
    x = xstart
    y = ystart
    try:
        for msg in allmsglist:
            y -= 5
            if msg.text == "\"\"\n":
                continue
            if msg.photo.find("photos") != -1:
                photopath = basedatapath + '\\' + msg.photo

                imgwidth = msg.width * .45
                if msg.width < msg.height:
                    imgheight = msg.height * .2
                else:
                    imgheight = msg.height * .5

                if y < imgheight:
                    print(photopath, x, y, msg.width, msg.height)
                    canvas.showPage()
                    x = xstart
                    y = ystart
                    canvas.setFont("Times-Roman", 12)

                canvas.drawImage(photopath, x, y-imgheight, imgwidth, imgheight,anchor='sw',anchorAtXY=True,showBoundary=False)
                y -= (imgheight + 15)

                if y < 30:
                    canvas.showPage()
                    x = xstart
                    y = ystart
                    canvas.setFont("Times-Roman", 12)

            #msg.text = msg.text.replace("\n","")
            texts = wrap(msg.text, 100)

            for line in texts:
                if True:
                    canvas.drawString(x, y, line)
                    linecount += 1
                    y -= 15
                if y < 30:
                    canvas.showPage()
                    x = xstart
                    y = ystart
                    canvas.setFont("Times-Roman", 12)

            # for line in texts:
            #     textobject.textLines(line)
            #     linecount += 1
            #     if linecount == 50:
            #         canvas.drawText(textobject)
            #         canvas.showPage()
            #         linecount = 0
            #         textobject = canvas.beginText()
            #         textobject.setTextOrigin(10, 730)
            #         textobject.setFont("Helvetica", 12)

        #canvas.drawText(textobject)
        #canvas.showPage()
        canvas.save()
    except Exception as e:
        print(e)

def parsenumber(strin, pattern):
    number = 0
    msgtext = strin.split(pattern)

    if msgtext != "":
        data = re.sub("[^0-9]", "", msgtext[1])
        number = int(data)
        wfp.write(str(number))
        wfp.write("\n")

    return number

def parsedata(strin, pattern):
    data = ''
    msgtext = strin.split(pattern)
    if msgtext != "":
        if pattern == PHOTO:
            data = re.sub('[^a-zA-Z0-9 /\.@_-]', '', msgtext[1])
        else:
            data = msgtext[1].replace("\\n", '')
            #data = re.sub('[\n]','',msgtext[1])
            #data = msgtext[1]
            data = data[1:]
            data = data[:-2]
        wfp.write(data)
    return data



def parsejsonfile(jsonfilepath):

    allmsgslist = []

    startallmessage = False
    startmsgfound = False
    try:
        with open(jsonfilepath, 'r',errors='ignore') as fp:
            while True:
                line = fp.readline()
                if line == "":
                    break
                if startallmessage == False:
                    if line.find("\"messages\": [") != -1:
                        startallmessage = True
                        continue
                else:
                    if line.find("{") != -1:
                        line = fp.readline()
                        if line == "":
                            break
                        msgobj = msgtemplete()
                        while (line.find("},") == -1):
                            if line.find(ID) != -1:
                                msgobj.id = parsenumber(line, ID)
                            if line.find(TYPE) != -1:
                                msgobj.type = parsedata(line, TYPE)
                            if line.find(DATE) != -1:
                                msgobj.date = parsedata(line, DATE)
                            if line.find(FROM) != -1:
                                msgobj.fromname = parsedata(line, FROM)
                            if line.find(FROMID) != -1:
                                msgobj.fromid = parsenumber(line, FROMID)
                            if line.find(AUTHOR) != -1:
                                msgobj.author = parsedata(line, AUTHOR)
                            if line.find(PHOTO) != -1:
                                msgobj.photo = parsedata(line, PHOTO)
                            if line.find(WIDTH) != -1:
                                msgobj.width =  parsenumber(line, WIDTH)
                            if line.find(HEIGHT) != -1:
                                msgobj.height =  parsenumber(line, HEIGHT)
                            if line.find(TEXT) != -1:
                                msgobj.text = parsedata(line, TEXT)
                            line = fp.readline()
                            if line == "":
                                break
                        allmsgslist.append(msgobj)
    except Exception as e:
        print(e)

    return allmsgslist

allmsglist = parsejsonfile(jsonfilepath)

createpdf(allmsglist)

wfp.close()
