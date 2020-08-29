from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer
from sister.modules.kurikulum.models import (
    TahunAjaran,
    Kurikulum,
    MataPelajaran,
    KurikulumMataPelajaran,
    KompetensiDasar
)


class TahunAjaranSerializer(ModelSerializer):
    class Meta:
        model = TahunAjaran
        exclude = [
            'created_at',
            'deleted',
            'deleted_at',
        ]


class KurikulumSerializer(ModelSerializer):
    class Meta:
        model = Kurikulum
        exclude = [
            'created_at',
            'deleted',
            'deleted_at',
        ]


class MataPelajaranSerializer(ModelSerializer):
    class Meta:
        model = MataPelajaran
        exclude = [
            'created_at',
            'deleted',
            'deleted_at',
        ]


class KompetensiIntiSerializer(Serializer):

    kode = CharField(read_only=True)
    keterangan = IntegerField(read_only=True)


class KompetensiDasarSerializer(Serializer):
    class Meta:
        model = KompetensiDasar
        exclude = [
            'created_at',
            'deleted',
            'deleted_at'
        ]


class KurikulumMataPelajaranSerializer(ModelSerializer):
    class Meta:
        model = KurikulumMataPelajaran
        exclude = [
            'created_at',
            'deleted',
            'deleted_at'
        ]
