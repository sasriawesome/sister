from graphene import relay, ObjectType, Field
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from ...public.v1.types import UserNode
from .types import (
    TahunAjaranNode, KurikulumNode, MataPelajaranNode, KompetensiDasarNode,
    KelasNode, SiswaKelasNode, MataPelajaranKelasNode, KompetensiPenilaianNode,
    CatatanSiswaNode, JadwalPelajaranNode, RentangNilaiNode, RuangNode,
    PenilaianPembelajaranNode, PresensiKelasNode, EkstraKurikulerNode,
    TahunAngkatanNode, PesertaEkstraKurikulerNode, JadwalEkstraKurikulerNode,
    PenilaianEkstraKurikulerNode, PersonNode, SiswaNode, GuruNode
)


class Query(ObjectType):

    account = Field(UserNode)

    person = relay.Node.Field(PersonNode)
    person_list = DjangoFilterConnectionField(PersonNode)

    siswa = relay.Node.Field(SiswaNode)
    siswa_list = DjangoFilterConnectionField(SiswaNode)

    guru = relay.Node.Field(GuruNode)
    guru_list = DjangoFilterConnectionField(GuruNode)

    ruang = relay.Node.Field(RuangNode)
    ruang_list = DjangoFilterConnectionField(RuangNode)

    tahun_ajaran = relay.Node.Field(TahunAjaranNode)
    tahun_ajaran_list = DjangoFilterConnectionField(TahunAjaranNode)

    kurikulum = relay.Node.Field(KurikulumNode)
    kurikulum_list = DjangoFilterConnectionField(KurikulumNode)

    mata_pelajaran = relay.Node.Field(MataPelajaranNode)
    mata_pelajaran_list = DjangoFilterConnectionField(MataPelajaranNode)

    kompetensi_dasar = relay.Node.Field(KompetensiDasarNode)
    kompetensi_dasar_list = DjangoFilterConnectionField(KompetensiDasarNode)

    kelas = relay.Node.Field(KelasNode)
    kelas_list = DjangoFilterConnectionField(KelasNode)

    siswa_kelas = relay.Node.Field(SiswaKelasNode)
    siswa_kelas_list = DjangoFilterConnectionField(SiswaKelasNode)

    mata_pelajaran_kelas = relay.Node.Field(MataPelajaranKelasNode)
    mata_pelajaran_kelas_list = DjangoFilterConnectionField(
        MataPelajaranKelasNode)

    kompetensi_penilaian = relay.Node.Field(KompetensiPenilaianNode)
    kompetensi_penilaian_list = DjangoFilterConnectionField(
        KompetensiPenilaianNode)

    catatan_siswa = relay.Node.Field(CatatanSiswaNode)
    catatan_siswa_list = DjangoFilterConnectionField(CatatanSiswaNode)

    jadwal_pelajaran = relay.Node.Field(JadwalPelajaranNode)
    jadwal_pelajaran_list = DjangoFilterConnectionField(JadwalPelajaranNode)

    rentang_nilai = relay.Node.Field(RentangNilaiNode)
    rentang_nilai_list = DjangoFilterConnectionField(RentangNilaiNode)

    penilaian_pembelajaran = relay.Node.Field(
        PenilaianPembelajaranNode)
    penilaian_pembelajaran_list = DjangoFilterConnectionField(
        PenilaianPembelajaranNode)

    presensi = relay.Node.Field(PresensiKelasNode)
    presensi_list = DjangoFilterConnectionField(PresensiKelasNode)

    ekstrakurikuler = relay.Node.Field(EkstraKurikulerNode)
    ekstrakurikuler_list = DjangoFilterConnectionField(EkstraKurikulerNode)

    tahun_angkatan = relay.Node.Field(TahunAngkatanNode)
    tahun_angkatan_list = DjangoFilterConnectionField(TahunAngkatanNode)

    peserta_ekstrakurikuler = relay.Node.Field(PesertaEkstraKurikulerNode)
    peserta_ekstrakurikuler_list = DjangoFilterConnectionField(
        PesertaEkstraKurikulerNode)

    jadwal_ekstrakurikuler = relay.Node.Field(JadwalEkstraKurikulerNode)
    jadwal_ekstrakurikuler_list = DjangoFilterConnectionField(
        JadwalEkstraKurikulerNode)

    penilaian_extrakurikuler = relay.Node.Field(PenilaianEkstraKurikulerNode)
    penilaian_extrakurikuler_list = DjangoFilterConnectionField(
        PenilaianEkstraKurikulerNode)

    @login_required
    def resolve_account(root, info):
        return info.context.user
