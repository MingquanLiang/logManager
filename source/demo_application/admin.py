from django.contrib import admin
#from demo_application.models import ExperimentResult, ExperimentItem
from demo_application.models import SimulatorTestResult, SimulatorTestItem
from demo_application.models import UploadFilename




class SimulatorTestItemInline(admin.StackedInline):
    model = SimulatorTestItem
    extra = 1

class SimulatorTestResultAdmin(admin.ModelAdmin):
    fields = ['testUser', 'testRecordTime', 'testComment', 'testResultDetailLink']
    # when auto_now and auto_now_add of testRecordTime == True, can not add testRecordTime into fields
    #fields = ['testUser', 'testComment']
    inlines = [SimulatorTestItemInline]
    list_display = ('testUser', 'testRecordTime', 'testComment', 'testResultDetailLink')
    search_fields = ('testUser', 'testComment')

class UploadFilenameAdmin(admin.ModelAdmin):
    fields = ['testUser', 'testRecordTime', 'filename', 'testComment', 'testResultDetailLink']
    list_display = ['testUser', 'filename', 'testRecordTime', 'testComment', 'testResultDetailLink']
    search_fields = ('testUser', 'filename', 'testComment')

admin.site.register(SimulatorTestResult, SimulatorTestResultAdmin)
admin.site.register(UploadFilename, UploadFilenameAdmin)
