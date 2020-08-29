from django.contrib import admin
from django.contrib.admin import ModelAdmin
from sister.core.admin import admin_site


from .models import (
    PersonContact,
    PersonAddress,
    PhotoProfile,
    Person,
    Wali,
    Guru,
    Siswa
)


class PhotoInline(admin.TabularInline):
    extra = 0
    model = PhotoProfile


class ContactInline(admin.StackedInline):
    model = PersonContact


class AddressInline(admin.StackedInline):
    extra = 1
    model = PersonAddress


class PersonAdmin(ModelAdmin):
    list_display = ['full_name', 'gender', 'date_of_birth']
    list_select_related = ['user']
    inlines = [PhotoInline, ContactInline, AddressInline]


class GuruAdmin(ModelAdmin):
    list_display = ['nip', 'full_name']
    list_select_related = ['person']

    def full_name(self, obj):
        return obj.person.full_name


class WaliInline(admin.TabularInline):
    extra = 0
    model = Wali


class SiswaAdmin(ModelAdmin):
    list_display = ['nis', 'full_name', 'nisn']
    list_select_related = ['person']
    inlines = [WaliInline]

    def full_name(self, obj):
        return obj.person.full_name


admin_site.register(Person, PersonAdmin)
admin_site.register(Guru, GuruAdmin)
admin_site.register(Siswa, SiswaAdmin)
