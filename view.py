from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import psycopg2
import base64
from base64 import b64encode
from django.shortcuts import redirect

# function for html form submit
def deviceModelEdit(request):
    conn = psycopg2.connect(
        host="localhost",
        database="",
        user="",
        password="")
    cur = conn.cursor()

    if request.method == 'POST':
        drawing_DataSheetFile = ''
        drawing_ChassisFile = ''
        DataSheetUploadFileType = ''
        ChassisSlotUploadFileType = ''
        drawing_DataSheetFile_base_64 = ''
        drawing_ChassisFile_base_64 = ''
        try:
            if request.FILES['DataSheetFile']:
                DataSheetUploadFileType = request.POST.get('DataSheetFileType')
                DataSheetFile = request.FILES['DataSheetFile']
                fs = FileSystemStorage()
                filename = fs.save(DataSheetFile.name, DataSheetFile)
                uploaded_file_url = fs.url(filename)
                # read data from a file, here 'app' is Django project name, and our media directory is inside this directory
                path_to_file = '/app/'+uploaded_file_url
                drawing_DataSheetFile = open(path_to_file, 'rb').read()
                drawing_DataSheetFile_base_64 = base64.b64encode(drawing_DataSheetFile)
                # drawing_DataSheetFile_psycopg2_bin = psycopg2.Binary(drawing_DataSheetFile)

            # print("Checking for ChassisFile uploaded file type.")
            if request.FILES['ChassisFile']:
                # print("ChassisFile file found")
                ChassisSlotUploadFileType = request.POST.get('ChassisFileType')
                ChassisFile = request.FILES['ChassisFile']
                fs = FileSystemStorage()
                filename = fs.save(ChassisFile.name, ChassisFile)
                uploaded_file_url = fs.url(filename)
                # print("ChassisFile detected. filename = ",filename, " uploaded_file_url: ",uploaded_file_url)
                
                # read data from a file
                path_to_file = '/app/'+uploaded_file_url
                drawing_ChassisFile = open(path_to_file, 'rb').read()
                drawing_ChassisFile_base_64 = base64.b64encode(drawing_ChassisFile)
                # drawing_ChassisFile_psycopg2_bin = psycopg2.Binary(drawing_ChassisFile)

        cur.execute("""
        INSERT INTO file_name_db 
        (datasheetuploadfile,DataSheetUploadFileType, chassisslotuploadfile,ChassisSlotUploadFileType ) 
        VALUES (%s,%s,%s,%s)
        """,( drawing_DataSheetFile_base_64,DataSheetUploadFileType, drawing_ChassisFile_base_64,ChassisSlotUploadFileType ))
        conn.commit();
        conn.close()
        cur.close()
        return redirect('/deviceModel/') # returning to home page
        except Exception as e:
            print(e)
    return render(request, "deviceModelEdit.html") # form edit page
    
    
    
# function for storing data to db    
def deviceModelView(request):
    conn = psycopg2.connect(
        host="",
        database="",
        user="",
        password="")
    cur = conn.cursor()
    ModelName = request.GET.get('ModelName','')
    query_model_table = "SELECT datasheetuploadfiletype,chassisslotuploadfiletype,datasheetuploadfile,chassisslotuploadfile FROM public.file_name_db where devicemodelname like '" + ModelName + "';"
    cur.execute(query_model_table)
    rows = cur.fetchall()
    datasheetuploadfiletype,chassisslotuploadfiletype, datasheetuploadfile, chassisslotuploadfile = '','','',''
    for row in rows:
        datasheetuploadfiletype,chassisslotuploadfiletype, datasheetuploadfile, chassisslotuploadfile = row[0],row[1],row[2].tobytes().decode("utf-8"), row[3].tobytes().decode("utf-8")
        break
    conn.close()
    cur.close()
    return render(request, "deviceModelView.html",{'datasheetuploadfiletype':datasheetuploadfiletype,'chassisslotuploadfiletype':chassisslotuploadfiletype, 'datasheetuploadfile':datasheetuploadfile, 'chassisslotuploadfile':chassisslotuploadfile})
    