from enigma.machine import EnigmaMachine
from itertools import combinations
import string

known_plugs = ['LR', 'AN', 'EZ', 'HK', 'IJ', 'MQ', 'OT', 'SW', 'UX']
used_letters = {c for pair in known_plugs for c in pair}
remaining_letters = [c for c in string.ascii_uppercase if c not in used_letters]


def main():
    plug_candidates = [' '.join(known_plugs + [p1 + p2]) for p1, p2 in combinations(remaining_letters, 2)]
    results = []
    cipher = "USOKW RRHCD NZTUR SXPZR PCXDZ JDHFI GYBFD BINXB MRSFE GHAJW OKMDL NXCNQ AJKYW ZIGLL QJDFV BERAA VTVFL HFMXW GQXNU MQRLJ WDBZL RMKDV WABGB ZZUIA OVYSG BAXHF NJLNV MBOUN YMCZR ZJUSU PLSKW J"

    for candidate in plug_candidates:
        machine = EnigmaMachine.from_key_sheet(
            rotors='IV I V',
            reflector='B',
            ring_settings='1 1 1',
            plugboard_settings=candidate
        )
        machine.set_display('JWD')
        plain = machine.process_text(cipher.replace(" ", ""))
        if "RECONXUNITXFROMX" in plain:
            results.append({
                "plugs": candidate,
                "plaintext": plain.replace('X', ' ')
            })
    for result in results:
        print(f"plugboards: {result['plugs']}, plain text：{result['plaintext']}")


if __name__ == "__main__":
    main()