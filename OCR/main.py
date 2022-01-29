import os
import wx
import pytesseract
import cv2
from PIL import Image
import fitz

#Habilitar Tesseract
tsr_path = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = tsr_path


#Janela de dialogo para abrir o arquivo
def obter_arquivo(extensao):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=extensao, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path


arquivo = obter_arquivo('*.*')
path = os.path.dirname(arquivo) + '\\'


#Rotina se caso for PDF transformar em imagem
vpdf = os.path.splitext(arquivo)[1]
if vpdf.lower() == '.pdf':
    input_pdf = arquivo
    output_name = path+'out.tif'
    compression = 'zip'

    zoom = 3
    mat = fitz.Matrix(zoom, zoom)

    doc = fitz.open(input_pdf)
    image_list = []
    for page in doc:
        pix = page.getPixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image_list.append(img)

    if image_list:
        image_list[0].save(
            output_name,
            save_all=True,
            append_images=image_list[1:],
            compression=compression,
            dpi=(500, 500),
        )
    arquivo = path+'out.tif'


#Rotina de corte da imagem
imagem = cv2.imread(arquivo)
roi = cv2.selectROI('Selecione', imagem)
cv2.destroyAllWindows()
imagem_selecionada = imagem[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
cv2.imwrite(path+'out.jpg', imagem_selecionada)

#Rotina se geração do TXT
string = pytesseract.image_to_string(cv2.imread(path+'out.jpg'), lang='por')
arquivo = open(path+'out.txt', 'w+')
arquivo.write(string)
arquivo.close()

#Remoção dos arquivos temporarios
if os.path.exists(path+'out.jpg'):
    os.remove(path+'out.jpg')

if os.path.exists(path+'out.tif'):
    os.remove(path+'out.tif')