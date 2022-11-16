import pytest
from scrapper import get_video_info

class TestClass:
    def test_video1(self):
        assert get_video_info["fmsoym8I-3o"].Titre == "Pierre Niney : L\u2019interview face cach\u00e9e par HugoD\u00e9crypte"
        assert get_video_info["fmsoym8I-3o"].Description == "\ud83c\udf7f L'acteur Pierre Niney est dans L\u2019interview face cach\u00e9e ! Ces prochains mois, le format revient plus fort avec des artistes, sportifs, etc.\ud83d\udd14 Abonnez-vous ..."
        assert get_video_info["fmsoym8I-3o"].Commentaires.len() == 10
        assert get_video_info["fmsoym8I-3o"].Nombre_de_vues > 0
        assert get_video_info["fmsoym8I-3o"].Nombre_de_likes > -1
        assert get_video_info["fmsoym8I-3o"].Id_de_la_video == "fmsoym8I-3o"
