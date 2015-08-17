import os

from django.http import HttpResponse
from django.conf import settings
from django.core.servers.basehttp import FileWrapper


#def downloadAFile(request, fileDate, fileTime, downloadFile):
#    return HttpResponse('OK. %s and %s The file %s has been downloaded' % (fileDate, fileTime, downloadFile))

baseDir = settings.MEDIA_ROOT
def downloadAFile(request, downloadFile):
    #return HttpResponse('OK. %s has been downloaded' % (filename))
    filename = baseDir + '/' + downloadFile
    f =open(filename)
    data = f.read()
    f.close()
    response = HttpResponse(data,mimetype='application/octet-stream') 
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
    return response
    #wrapper = FileWrapper(file(filename))
    #response = HttpResponse(wrapper, content_type='text/plain')
    #response['Content-Length'] = os.path.getsize(filename) 
    #return response
