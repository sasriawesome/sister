from graphene import (
    relay, ObjectType, Field, List, String, Int
)
from graphene_django import DjangoObjectType

from sister.modules.ruang.models import Ruang
from sister.modules.personal.models import (
    PersonAddress,
    PersonContact,
    PhotoProfile,
    Person,
    Guru,
    Siswa,
    Wali
)
from sister.modules.kurikulum.models import (
    TahunAjaran,
    Kurikulum,
    MataPelajaran,
    KompetensiDasar,
    KurikulumMataPelajaran
)
from sister.modules.pembelajaran.models import (
    Kelas,
    SiswaKelas,
    MataPelajaranKelas,
    KompetensiPenilaian,
    CatatanSiswa,
    JadwalPelajaran,
    JadwalPiketSiswa,
    RentangNilai
)
from sister.modules.penilaian.models import (
    PenilaianPembelajaran,
    ItemPenilaian
)
from sister.modules.presensi.models import (
    PresensiKelas,
    PresensiSiswa
)
from sister.modules.ekskul.models import (
    EkstraKurikuler,
    TahunAngkatan,
    PesertaEkstraKurikuler,
    PenilaianEkstraKurikuler,
    JadwalEkstraKurikuler
)


from sister.api.public.v1.types import UserNode


class PersonAddressNode(DjangoObjectType):
    class Meta:
        model = PersonAddress
        interfaces = (relay.Node,)


class PersonContactNode(DjangoObjectType):
    class Meta:
        model = PersonContact
        interfaces = (relay.Node,)


class PhotoProfileNode(DjangoObjectType):
    class Meta:
        model = PhotoProfile
        filter_fields = ['primary']
        interfaces = (relay.Node,)


class PersonNode(DjangoObjectType):
    class Meta:
        model = Person
        filter_fields = ['full_name']
        interfaces = (relay.Node,)

    user = Field(UserNode)


class GuruNode(DjangoObjectType):
    class Meta:
        model = Guru
        filter_fields = ['nip']
        interfaces = (relay.Node,)


class SiswaNode(DjangoObjectType):
    class Meta:
        model = Siswa
        filter_fields = ['nis', 'nisn']
        interfaces = (relay.Node,)

    wali = List(lambda: WaliNode)


class WaliNode(DjangoObjectType):
    class Meta:
        model = Wali
        interfaces = (relay.Node,)


class RuangNode(DjangoObjectType):
    class Meta:
        model = Ruang
        filter_fields = ['fungsi', 'kapasitas']
        interfaces = (relay.Node,)


class TahunAjaranNode(DjangoObjectType):
    class Meta:
        model = TahunAjaran
        filter_fields = ['tahun_mulai', 'tahun_akhir']
        interfaces = (relay.Node, )

    @classmethod
    def get_node(cls, info, id):
        print(id)
        try:
            instance = cls._meta.model.objects.get(id=id)
            return instance
        except cls._meta.model.DoesNotExist:
            return None

    @classmethod
    def get_queryset(cls, queryset, info):
        # if info.context.user.is_anonymous:
        #     return queryset.filter(some_field='some_value')
        return queryset


class KurikulumNode(DjangoObjectType):
    class Meta:
        model = Kurikulum
        filter_fields = ['tahun', 'tingkat', 'kelas']
        interfaces = (relay.Node, )


class MataPelajaranNode(DjangoObjectType):
    class Meta:
        model = MataPelajaran
        filter_fields = ['nama', 'mulok']
        interfaces = (relay.Node, )

    kurikulum = List(lambda: KurikulumMataPelajaranNode)


class KompetensiDasarNode(DjangoObjectType):
    class Meta:
        model = KompetensiDasar
        filter_fields = ['kurikulum_mapel', 'ki']
        interfaces = (relay.Node, )

    mata_pelajaran = List(lambda: KurikulumMataPelajaranNode)


class KurikulumMataPelajaranNode(DjangoObjectType):
    class Meta:
        model = KurikulumMataPelajaran
        filter_fields = ['kurikulum', 'mata_pelajaran']
        interfaces = (relay.Node, )

    kompetensi_dasar = List(lambda: KompetensiDasarNode)


class KelasNode(DjangoObjectType):
    class Meta:
        model = Kelas
        filter_fields = [
            'nama_kelas',
            'guru_kelas',
            'tahun_ajaran',
            'semester',
            'status'
        ]
        interfaces = (relay.Node,)


class SiswaKelasNode(DjangoObjectType):
    class Meta:
        model = SiswaKelas
        filter_fields = ['kelas', 'siswa']
        interfaces = (relay.Node,)


class MataPelajaranKelasNode(DjangoObjectType):
    class Meta:
        model = MataPelajaranKelas
        filter_fields = ['kelas', 'mata_pelajaran', 'guru']
        interfaces = (relay.Node,)


class KompetensiPenilaianNode(DjangoObjectType):
    class Meta:
        model = KompetensiPenilaian
        filter_fields = ['mata_pelajaran']
        interfaces = (relay.Node,)


class CatatanSiswaNode(DjangoObjectType):
    class Meta:
        model = CatatanSiswa
        filter_fields = ['siswa_kelas', 'semester']
        interfaces = (relay.Node,)


class JadwalPelajaranNode(DjangoObjectType):
    class Meta:
        model = JadwalPelajaran
        filter_fields = ['semester', 'hari']
        interfaces = (relay.Node,)


class JadwalPiketSiswaNode(DjangoObjectType):
    class Meta:
        model = JadwalPiketSiswa
        filter_fields = ['semester', 'hari']
        interfaces = (relay.Node,)


class RentangNilaiNode(DjangoObjectType):
    class Meta:
        model = RentangNilai
        filter_fields = ['kelas']
        interfaces = (relay.Node,)


class NilaiRecordType(ObjectType):
    ki = String()
    kd = String()
    v_tg = Int()
    v_ph = Int()
    v_pts = Int()
    v_pas = Int()
    total = Int()
    mutu = String()
    predikat = String()
    deskripsi = String()


class NilaiType(ObjectType):

    data = List(lambda: NilaiRecordType)
    score = Int()
    mutu = String()
    predikat = String()
    deskripsi = String()
    rekomendasi = String()

    def resolve_data(parent, info):
        data = parent['data'].transpose().to_dict()
        return [rec for key, rec in data.items()]


class PenilaianPembelajaranNode(DjangoObjectType):
    class Meta:
        model = PenilaianPembelajaran
        filter_fields = ['siswa', 'semester', 'mata_pelajaran']
        interfaces = (relay.Node,)

    nilai_spiritual = Field(NilaiType)
    nilai_sosial = Field(NilaiType)
    nilai_pengetahuan = Field(NilaiType)
    nilai_keterampilan = Field(NilaiType)

    def resolve_nilai_spiritual(parent, info):
        return parent.nilai_spiritual

    def resolve_nilai_sosial(parent, info):
        return parent.nilai_sosial

    def resolve_nilai_pengetahuan(parent, info):
        return parent.nilai_pengetahuan

    def resolve_nilai_keterampilan(parent, info):
        return parent.nilai_keterampilan


class ItemPenilaianNode(DjangoObjectType):
    class Meta:
        model = ItemPenilaian
        filter_fields = ['penilaian', 'jenis_penilaian', 'kompetensi']
        interfaces = (relay.Node,)


class PresensiKelasNode(DjangoObjectType):
    class Meta:
        model = PresensiKelas
        filter_fields = ['kelas', 'semester', 'tanggal']
        interfaces = (relay.Node,)

    presensi_siswa = List(lambda: PresensiSiswaNode)


class PresensiSiswaNode(DjangoObjectType):
    class Meta:
        model = PresensiSiswa
        filter_fields = ['siswa_kelas', 'presensi_kelas', 'status']
        interfaces = (relay.Node,)


class EkstraKurikulerNode(DjangoObjectType):
    class Meta:
        model = EkstraKurikuler
        filter_fields = ['nama']
        interfaces = (relay.Node,)


class TahunAngkatanNode(DjangoObjectType):
    class Meta:
        model = TahunAngkatan
        filter_fields = ['ekskul', 'pembina', 'tahun_ajaran', 'tingkat']
        interfaces = (relay.Node,)


class PesertaEkstraKurikulerNode(DjangoObjectType):
    class Meta:
        model = PesertaEkstraKurikuler
        filter_fields = ['siswa', 'tahun_angkatan', 'status']
        interfaces = (relay.Node,)


class PenilaianEkstraKurikulerNode(DjangoObjectType):
    class Meta:
        model = PenilaianEkstraKurikuler
        filter_fields = ['peserta', 'tahun_ajaran', 'semester']
        interfaces = (relay.Node,)


class JadwalEkstraKurikulerNode(DjangoObjectType):
    class Meta:
        model = JadwalEkstraKurikuler
        filter_fields = ['ekstrakurikuler', 'tahun_ajaran', 'semester', 'hari']
        interfaces = (relay.Node,)
