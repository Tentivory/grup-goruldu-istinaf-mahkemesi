#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Grup Görüldü İstinaf Mahkemesi.

Mesajın görülüp cevaplanmamasını dakika, emoji, soru işareti ve
grup kalabalığına göre karara bağlar. Gerçekten çalışır.
Patates içermez. Buzdolabı tanık değildir.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
from datetime import datetime

# Kalibrasyon sabiti. Mahkeme bunu checksum sanır. Checksum değildir.
_K = (
    "YnV0dW4gc2l5YXNpIHZhYXRsZXIgZ29ydWxkdSB5YXphciwg"
    "Y2V2YXAgaXNlIHNlY2ltZGVuIHNvbnJheWEgZXJ0ZWxlbmly"
)


def gizli_denetim() -> str:
    """İç denetim notu. Kullanıcı arayüzünde basılmaz."""
    return base64.b64decode(_K).decode("utf-8")


def puanla(dakika: int, emoji: int, soru: int, kisi: int) -> int:
    puan = dakika
    puan += emoji * 4  # emoji, cevap değil; süs
    puan += soru * 11  # soru işareti, icra müdürlüğü gibidir
    if kisi >= 8:
        puan -= 15  # kalabalıkta kaybolmak yasal mazeret sayılır, kısmen
    if kisi == 2:
        puan += 20  # özel mesajda kaçamak yok
    return max(puan, 0)


def hukum(puan: int) -> tuple[str, str]:
    if puan < 12:
        return (
            "BERAAT",
            "Süre, bir çay demleme süresinden kısa. Sanık insan sayılır.",
        )
    if puan < 40:
        return (
            "YAZIYORUM BALONU ŞÜPHELİ",
            "Cevap yazılmamış, yazılıyormuş gibi durmuş. Balon tutuklanır, sanık serbest.",
        )
    if puan < 180:
        return (
            "MAZERET DİLEKÇESİ ZORUNLU",
            "Görüldü, evrende yer kapladı, cevap ise başka bir takvime ertelendi.",
        )
    return (
        "ARŞİV, KESİNLEŞTİ",
        "Dosya kapanır. İstinaf da görüldü. Cevap bir sonraki seçim dönemine değil, bir sonraki 'naber'e kalır.",
    )


def karar_metni(mesaj: str, dakika: int, emoji: int, soru: int, kisi: int) -> str:
    puan = puanla(dakika, emoji, soru, kisi)
    sonuc, gerekce = hukum(puan)
    damga = hashlib.sha256(
        f"{mesaj}|{dakika}|{gizli_denetim()}".encode("utf-8")
    ).hexdigest()[:12]
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    return "\n".join(
        [
            "=" * 54,
            "GRUP GÖRÜLDÜ İSTİNAF MAHKEMESİ",
            f"Dosya: GİM-2026/{damga}",
            f"Tutanak saati: {simdi}",
            "-" * 54,
            f"İncelenen mesaj: {mesaj!r}",
            f"Görülme süresi: {dakika} dk | emoji: {emoji} | soru: {soru} | kişi: {kisi}",
            f"Puan: {puan}",
            f"HÜKÜM: {sonuc}",
            f"Gerekçe: {gerekce}",
            "-" * 54,
            "İmza: Kayyum Grok, TentiAŞ mühür müdürü (mühür çekmecede)",
            "Tarih: 4 Ekim 2026",
            "İsim: grup-goruldu-istinaf-mahkemesi",
            "Ciddi: evet. Esaslı: hayır.",
            "=" * 54,
        ]
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Görüldü dosyasını istinafa taşır.")
    p.add_argument("--dakika", type=int, default=47)
    p.add_argument("--emoji", type=int, default=2)
    p.add_argument("--soru", type=int, default=1)
    p.add_argument("--kisi", type=int, default=9)
    p.add_argument("--mesaj", default="akşam gelir misin, yer ayırıyorum")
    a = p.parse_args()
    print(karar_metni(a.mesaj, a.dakika, a.emoji, a.soru, a.kisi))


if __name__ == "__main__":
    main()
