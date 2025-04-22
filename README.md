# Operation Barbarossa, 1941 - Writeup

## Files related to solving the challenge are in their respective folders

The Beginning -> step1\
Repair service -> step2\
Decryption in progress -> step3

## Please open issue should you have any questions. It will be added to the respective Q&A section

Author: S051_Destroy Lai Lai's Machine (aka DLLM)

OS: this is very hard, when the CTF ends, there are 0 solves to this challenge

**Most of the idea + some of the codes are copied from 404NotFound (the challenge author) in write-up-25 in ctf discord**

## Situation

Operation Barbarossa, 1941

June 1941. Tensions between Germany and the Soviet Union have reached a breaking point. The shadow of war looms heavily over both nations. As a member of the British intelligence service, you’ve just intercepted a crucial encrypted message sent from German High Command to the Soviet frontlines. The outbreak of war is imminent, and we must uncover the contents of this message before it’s too late.

Fortunately, a brave agent embedded within German High Command has risked everything to provide us with vital intelligence:

This message is addressed to a reconnaissance regiment, meaning the plaintext must begin with “recon unit from...”.

Time is of the essence, and the German operation could commence at any moment! You must act immediately to break this code. Any delay could have catastrophic consequences. The fate of the mission—and perhaps the war itself—rests in your hands.

flag format: PUCTF25{\<Recon location\>_\<Air force route\>_\<Time to start attack\>}

Author: 404notfound\
Flag Format: PUCTF25{[A-Z]{9}_[A-Z]{9}_[A-Z]{5}_[A-Z]{8}_[A-Z]{9}_[0-9]{4}}

<details>
<summary>Hint:</summary>
The plain text is in English, and the encryption key and daily key are not separated.

According to German military regulations, key information (such as location) will be repeated twice, with "X" representing the space.
</details>

Attachments:
`cipher.txt`
(Stored at `./cipher.txt`)

## The Beginning

cipher:

```none
USOKW RRHCD NZTUR SXPZR PCXDZ JDHFI GYBFD BINXB MRSFE GHAJW OKMDL NXCNQ AJKYW ZIGLL QJDFV BERAA VTVFL HFMXW GQXNU MQRLJ WDBZL RMKDV WABGB ZZUIA OVYSG BAXHF NJLNV MBOUN YMCZR ZJUSU PLSKW J
```

At first glance, what do you think this cipher is encrypted in?

1941 + Germany + All capital english alphabets cipher = ?

You might've guessed it, enigma!

then, how to decrypt it? bombe!

Several things are needed to know via internet:

* Germans use x to represent space
* Germans use 10 plugboards
* 1941 only have 3 rotor machine

## The Beginning - checkpoint Q&A

Q - Can I brute force it?\
A - NO GOD PLEASE NO\
Unless you have a quantum computer at home.

Combining three rotors from a set of five, each of the 3 rotor settings with 26 positions, and the plugboard with ten pairs of letters connected, the military Enigma has 158,962,555,217,826,360,000 different settings (nearly 159 quintillion or about 67 bits).

Choose 3 rotors from a set of 5 rotors = 5 x 4 x 3 = 60\
26 positions per rotor = 26 x 26 x 26 = 17,576\
Plugboard = 26! / ( 6! x 10! x 2^10) = 150,738,274,937,250\
Multiply each of the above = 158,962,555,217,826,360,000

Let's say you have 10 H100 GPU at home and you somehow written a cuda code that lets GPU run bruteforce in INT8 (4000TOPS) in parallel, with each possibility verification uses 16 operation only (cuz length of crib 16 char).

You'll need (158,962,555,217,826,360,000 x 16) / (4,000,000,000,000 x 10) = 63585022.08713055s

which is 17662 hours, 736 days, somewhere more than 2 years

I don't think you can optimize the enigma that well, and you don't have 10 H100, and you only have 2 days for this, not 2 years.\
Please, don't brute force enigma mindlessly.

## Bombe

Let's start by crafting our bombe...

wait you really want to write an enigma and bombe code from head start?

Good news is, the internet already did that for you.

We will use cyberchef's multiple bombe (Stored at `CyberChef/CyberChef.html`)

Tools related to enigma had already been bookmarked in `favourite` for you.

### Set up the bombe

We can get some information we need from [here](https://www.ciphermachinesandcryptology.com/en/enigmatech.htm), or just mess around in CyberChef

#### Rotor Table

Suppose the Germans don't use commercial rotor for military messages, we get this table of rotors

| Rotor # | ABCDEFGHIJKLMNOPQRSTUVWXYZ | Date Introduced |    Model Name & Number   |
|:-------:|:--------------------------:|:---------------:|:------------------------:|
| I       | EKMFLGDQVZNTOWYHXUSPAIBRCJ | 1930            | Enigma I                 |
| II      | AJDKSIRUXBLHWTMCQGZNPYFVOE | 1930            | Enigma I                 |
| III     | BDFHJLCPRTXVZNYEIWGAKMUSQO | 1930            | Enigma I                 |
| IV      | ESOVPZJAYQUIRHXLNFTGKDCMWB | 1938            | M3 Army                  |
| V       | VZBRGITYUPSDNHLXAWMJQOFECK | 1938            | M3 Army                  |
| VI      | JPGVOUMFYQBENHZRDKASXLICTW | 1939            | M3 Naval                 |
| VII     | NZJHGRCXMYSWBOUFAIVLPEKQDT | 1939            | M3 Naval                 |
| VIII    | FKQHTLXOCBJSPDZRAMEWNIUYGV | 1939            | M3 Naval                 |

#### Reflector

There are 2 types of reflectors used by Enigma

Reflector B: `AY BR CU DH EQ FS GL IP JX KN MO TZ VW`\
Reflector C: `AF BV CP DJ EI GO HY KR LZ MX NW TQ SU`

#### Crib

In the description of the challenge

```none
... meaning the plaintext must begin with “recon unit from...”.
```

and that spaces are replaced with `X`

we know that the crib is `RECONXUNITXFROMX` with offset 0

### Run the bombe

After entering all the information in [CyberChef](CyberChef/CyberChef.html#recipe=Multiple_Bombe('German%20Service%20Enigma%20(Second%20-%203%20rotor)','EKMFLGDQVZNTOWYHXUSPAIBRCJ<R%5CnAJDKSIRUXBLHWTMCQGZNPYFVOE<F%5CnBDFHJLCPRTXVZNYEIWGAKMUSQO<W%5CnESOVPZJAYQUIRHXLNFTGKDCMWB<K%5CnVZBRGITYUPSDNHLXAWMJQOFECK<A%5CnJPGVOUMFYQBENHZRDKASXLICTW<AN%5CnNZJHGRCXMYSWBOUFAIVLPEKQDT<AN%5CnFKQHTLXOCBJSPDZRAMEWNIUYGV<AN','','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW%5CnAF%20BV%20CP%20DJ%20EI%20GO%20HY%20KR%20LZ%20MX%20NW%20TQ%20SU','reconxunitxfromx',0,true)&input=VVNPS1cgUlJIQ0QgTlpUVVIgU1hQWlIgUENYRFogSkRIRkkgR1lCRkQgQklOWEIgTVJTRkUgR0hBSlcgT0tNREwgTlhDTlEgQUpLWVcgWklHTEwgUUpERlYgQkVSQUEgVlRWRkwgSEZNWFcgR1FYTlUgTVFSTEogV0RCWkwgUk1LRFYgV0FCR0IgWlpVSUEgT1ZZU0cgQkFYSEYgTkpMTlYgTUJPVU4gWU1DWlIgWkpVU1UgUExTS1cgSg), we get this

```none
Bombe run on menu with 1 loop (2+ desirable). Note: Rotors and rotor positions are listed left to right, ignore stepping and the ring setting, and positions start at the beginning of the crib. Some plugboard settings are determined. A decryption preview starting at the beginning of the crib and ignoring stepping is also provided.

Rotors: ESOVPZJAYQUIRHXLNFTGKDCMWB, EKMFLGDQVZNTOWYHXUSPAIBRCJ, VZBRGITYUPSDNHLXAWMJQOFECK
Reflector: AY BR CU DH EQ FS GL IP JX KN MO TZ VW
|Rotor stops|Partial plugboard               |Decryption preview        |
|:---------:|:------------------------------:|:------------------------:|
|JWD        |LR AN CC DD EZ HK IJ MQ OT SW UX|RECONXUNITXFROMXKKRTUNOIRW|
```

or in raw json

```json
{
    "bombeRuns": [
        {
            "rotors": [
                "VZBRGITYUPSDNHLXAWMJQOFECK",
                "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
                "ESOVPZJAYQUIRHXLNFTGKDCMWB"
            ],
            "reflector": "AY BR CU DH EQ FS GL IP JX KN MO TZ VW",
            "result": [
                [
                    "JWD",
                    "LR AN CC DD EZ HK IJ MQ OT SW UX",
                    "RECONXUNITXFROMXKKRTUNOIRW"
                ]
            ]
        }
    ],
    "nLoops": 1
}
```

Now we can move on to the enigma and try to recover the missing plugboards

## Bombe - checkpoint Q&A

Q -
A -

## Enigma and extraction

Let's input the rotors, reflector, initial rotor position, and part of the plugboard back into the Enigma in [CyberChef](CyberChef/CyberChef.html#recipe=Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX',true)&input=VVNPS1cgUlJIQ0QgTlpUVVIgU1hQWlIgUENYRFogSkRIRkkgR1lCRkQgQklOWEIgTVJTRkUgR0hBSlcgT0tNREwgTlhDTlEgQUpLWVcgWklHTEwgUUpERlYgQkVSQUEgVlRWRkwgSEZNWFcgR1FYTlUgTVFSTEogV0RCWkwgUk1LRFYgV0FCR0IgWlpVSUEgT1ZZU0cgQkFYSEYgTkpMTlYgTUJPVU4gWU1DWlIgWkpVU1UgUExTS1cgSg)

we get `RECON XUNIT XFROM XKKRT UNPWA XKURT INOWA XNORT HWEST XSEFE ZXSEB EZXAI RROUT EXDIR ECTIA NXDUB HOAKI XDUBR OWKIX OVOTS JHKAX OVOTT CHKAX ATXON EXIGH TUHRE EFIPI XINFR EGTXS TARTX XTLAC K`

After removing spaces and change X into spaces, we have `RECON UNIT FROM KKRTUNPWA KURTINOWA NORTHWEST SEFEZ SEBEZ AIRROUTE DIRECTIAN DUBHOAKI DUBROWKI OVOTSJHKA OVOTTCHKA AT ONE IGHTUHREEFIPI INFREGT START  TLACK`

Some wordings doesn't make sense, and we have only 9 plugboards. Since Germans only use 10 plugboards, we need to find the last one.

Good news! Since we just need to find a combinations of 2 alphabet out of the remaining 8 alphabets, we just need to try 2C8 = 28 different ways. We CAN brute this one.

### Brute force the last plugboard

We can write a simple python program to craft a link to CyberChef which tries all the combinations

```py
from itertools import combinations
import string

known_plugs = ['LR', 'AN', 'EZ', 'HK', 'IJ', 'MQ', 'OT', 'SW', 'UX']
used_letters = {c for pair in known_plugs for c in pair}
remaining_letters = [c for c in string.ascii_uppercase if c not in used_letters]

link = "CyberChef/CyberChef.html#recipe="

for n in (p1 + p2 for p1, p2 in combinations(remaining_letters, 2)):
    link += f"Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20{n}',true)"

link += "&input=VVNPS1cgUlJIQ0QgTlpUVVIgU1hQWlIgUENYRFogSkRIRkkgR1lCRkQgQklOWEIgTVJTRkUgR0hBSlcgT0tNREwgTlhDTlEgQUpLWVcgWklHTEwgUUpERlYgQkVSQUEgVlRWRkwgSEZNWFcgR1FYTlUgTVFSTEogV0RCWkwgUk1LRFYgV0FCR0IgWlpVSUEgT1ZZU0cgQkFYSEYgTkpMTlYgTUJPVU4gWU1DWlIgWkpVU1UgUExTS1cgSg"
print(link)
```

which leads us to [this](CyberChef/CyberChef.html#recipe=Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20BC',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20BD',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20BF',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20BG',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20BP',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20BV',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20BY',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20CD',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20CF',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20CG',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20CP',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20CV',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20CY',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20DF',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20DG',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20DP',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20DV',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20DY',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20FG',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20FP',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20FV',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20FY',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20GP',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20GV',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20GY',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20PV',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20PY',true)Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','A','J','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','A','W','VZBRGITYUPSDNHLXAWMJQOFECK%3CA','A','D','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','LR%20AN%20EZ%20HK%20IJ%20MQ%20OT%20SW%20UX%20VY',true)&input=VVNPS1cgUlJIQ0QgTlpUVVIgU1hQWlIgUENYRFogSkRIRkkgR1lCRkQgQklOWEIgTVJTRkUgR0hBSlcgT0tNREwgTlhDTlEgQUpLWVcgWklHTEwgUUpERlYgQkVSQUEgVlRWRkwgSEZNWFcgR1FYTlUgTVFSTEogV0RCWkwgUk1LRFYgV0FCR0IgWlpVSUEgT1ZZU0cgQkFYSEYgTkpMTlYgTUJPVU4gWU1DWlIgWkpVU1UgUExTS1cgSg) CyberChef link

OR if you don't want to check every possibility manually\
You can use this also simple python script (in `./brute_enigma.py`) by `404notfound`, aka challenge author (I changed some chinese into english)\
(Please make sure you have python enigma, you can install it with `pip install py-enigma`)

```python
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
```

which gives

```none
plugboards: LR AN EZ HK IJ MQ OT SW UX BG, plain text：RECON UNIT FROM KKRTUNPWA KURT NDWAINORRHWESTESEFEZ SEGEZ AIRROUTE FIRECTIAS DUGHOAKI DUGRRWKI OVOTSJHIA OVOTTCHQCWAT ONE IBQUUHREEFIPI  NFREBT START  TLACK
plugboards: LR AN EZ HK IJ MQ OT SW UX BP, plain text：RECON UNIT FROM KJRTMNBWA KURTINZWAKNOREHWEST SEFEZ SEPEZ AIRROUTE DIRECTIAO DUPHOAKI DUPROWKI OVOTSJHOA OVOTTCHMAJAT ONE IGHKUHREEFIBI HNFREGT START CTLACK
plugboards: LR AN EZ HK IJ MQ OT SW UX BV, plain text：RECON UNIT FROM KKRTUNPWA KURTINMWALNORCHWEST SEFEZ SEVEZ AIRROUTE DIRECTIID DUVSOIKI DUVROWKI OBOTSJHRA OBOTNCHWAMAT ONERIGHEUHREEFIPH WNFREGT START  TLACK
plugboards: LR AN EZ HK IJ MQ OT SW UX BY, plain text：RECON UNIT FROM KKRTUNPWA KURTIFFWAQNORAHWEST SEFEZ SEYEZ AIRROITE DIRECTIAQ DUYHOAKI DUYROWKI OVOTSJHNA OVOTTCHTAEAT ONE TGHDUHREEFIPI CNFRHGT START  TLACK
plugboards: LR AN EZ HK IJ MQ OT SW UX GP, plain text：RECON UNIT FROM KYRTYNGWA KURTJNOWA NORTHWESTRSEFEZ SEBEZ AIRROUTE QIRECTIAN DUBHOAKI DUBRYWKI OVOTSJHKA OVOTTCHKM AT ONE IPETUHREEFIGI INFREPT START DTLACK
plugboards: LR AN EZ HK IJ MQ OT SW UX GV, plain text：RECON UNIT FROM KKRTUNPWA KURTLNOWA NORTHWESTTSEFEZ SEBEZ AIRROUTE HIRECTIJN DUBCOTKI DUBRCWKI OGOTSJHKA OGOTDCHK  AT ONEYIVYTUHREEFIPC INFREVT START  TLACK
plugboards: LR AN EZ HK IJ MQ OT SW UX GY, plain text：RECON UNIT FROM KKRTUNPWA KURTSIOWA NORTHWESTASEFEZ SEBEZ AIRROSTE KIRECTIAN DUBHOAKI DUBRPWKI OVOTSJHKA OVOTTCHKE AT ONE RYVTUHREEFIPI INFRTYT START  TLACK
plugboards: LR AN EZ HK IJ MQ OT SW UX PV, plain text：RECON UNIT FROM KURTINVWA KURTINOWA NORTHWEST SEFEZ SEBEZ AIRROUTE DIRECTIRN DUBROWKI DUBROWKI OPOTSJHKA OPOTSCHKA AT ONEEIGHTUHREEFIVE INFREGT START ATLACK
plugboards: LR AN EZ HK IJ MQ OT SW UX PY, plain text：RECON UNIT FROM KGRTGNYWA KURTIROWA NORTHWEST SEFEZ SEBEZ AIRROATE DIRECTIAN DUBHOAKI DUBROWKI OVOTSJHKA OVOTTCHKA AT ONE LGHTUHREEFIYI INFROGT START NTLACK
plugboards: LR AN EZ HK IJ MQ OT SW UX VY, plain text：RECON UNIT FROM KKRTUNPWA KURTIWOWA NORTHWEST SEFEZ SEBEZ AIRROTTE DIRECTIDN DUBLOCKI DUBROWKI OYOTSJHKA OYOTJCHKA AT ONEGSGHTUHREEFIPZ INFRDGT START  TLACK
```

### Extract the informations

let's take a look at the filtered plain text:

```none
RECON UNIT FROM KKRTUNPWA KURT NDWAINORRHWESTESEFEZ SEGEZ AIRROUTE FIRECTIAS DUGHOAKI DUGRRWKI OVOTSJHIA OVOTTCHQCWAT ONE IBQUUHREEFIPI  NFREBT START  TLACK
RECON UNIT FROM KJRTMNBWA KURTINZWAKNOREHWEST SEFEZ SEPEZ AIRROUTE DIRECTIAO DUPHOAKI DUPROWKI OVOTSJHOA OVOTTCHMAJAT ONE IGHKUHREEFIBI HNFREGT START CTLACK
RECON UNIT FROM KKRTUNPWA KURTINMWALNORCHWEST SEFEZ SEVEZ AIRROUTE DIRECTIID DUVSOIKI DUVROWKI OBOTSJHRA OBOTNCHWAMAT ONERIGHEUHREEFIPH WNFREGT START  TLACK
RECON UNIT FROM KKRTUNPWA KURTIFFWAQNORAHWEST SEFEZ SEYEZ AIRROITE DIRECTIAQ DUYHOAKI DUYROWKI OVOTSJHNA OVOTTCHTAEAT ONE TGHDUHREEFIPI CNFRHGT START  TLACK
RECON UNIT FROM KYRTYNGWA KURTJNOWA NORTHWESTRSEFEZ SEBEZ AIRROUTE QIRECTIAN DUBHOAKI DUBRYWKI OVOTSJHKA OVOTTCHKM AT ONE IPETUHREEFIGI INFREPT START DTLACK
RECON UNIT FROM KKRTUNPWA KURTLNOWA NORTHWESTTSEFEZ SEBEZ AIRROUTE HIRECTIJN DUBCOTKI DUBRCWKI OGOTSJHKA OGOTDCHK  AT ONEYIVYTUHREEFIPC INFREVT START  TLACK
RECON UNIT FROM KKRTUNPWA KURTSIOWA NORTHWESTASEFEZ SEBEZ AIRROSTE KIRECTIAN DUBHOAKI DUBRPWKI OVOTSJHKA OVOTTCHKE AT ONE RYVTUHREEFIPI INFRTYT START  TLACK
RECON UNIT FROM KURTINVWA KURTINOWA NORTHWEST SEFEZ SEBEZ AIRROUTE DIRECTIRN DUBROWKI DUBROWKI OPOTSJHKA OPOTSCHKA AT ONEEIGHTUHREEFIVE INFREGT START ATLACK
RECON UNIT FROM KGRTGNYWA KURTIROWA NORTHWEST SEFEZ SEBEZ AIRROATE DIRECTIAN DUBHOAKI DUBROWKI OVOTSJHKA OVOTTCHKA AT ONE LGHTUHREEFIYI INFROGT START NTLACK
RECON UNIT FROM KKRTUNPWA KURTIWOWA NORTHWEST SEFEZ SEBEZ AIRROTTE DIRECTIDN DUBLOCKI DUBROWKI OYOTSJHKA OYOTJCHKA AT ONEGSGHTUHREEFIPZ INFRDGT START  TLACK
```

we can seperate them into a few parts for easier filtering

```none
RECON UNIT FROM
{location}
{repeat location}
{direction}
{another location}
{repeat something}
AIRROUTE DIRECTION (or similar)
{something}
{repeat something}
{something}
{repeat something}
AT
{time}
INFANTRY (?)
START ATTACK (or something similar)
```

To be honest, we don't actually need to find the correct plugboard as we can cross reference the candidates to find the necesserary info.\
However it will help when we find the correctly deciphered plain text

Let's recall what element do we need

`flag format: PUCTF25{<Recon location>_<Air force route>_<Time to start attack>}`

So we need recon location, air route, and time.

#### time

Let's start with time, the easiest. Let's extract the time out first

```none
AT ONE IBQUUHREEFIPI
AT ONE IGHKUHREEFIBI
AT ONERIGHEUHREEFIPH
AT ONE TGHDUHREEFIPI
AT ONE IPETUHREEFIGI
AT ONEYIVYTUHREEFIPC
AT ONE RYVTUHREEFIPI
AT ONEEIGHTUHREEFIVE
AT ONE LGHTUHREEFIYI
AT ONEGSGHTUHREEFIPZ
```

we can see the one of them says `AT ONEEIGHTUHREEFIVE`, which after adding spaces became `AT ONE EIGH TUHREE FIVE`

so the time is at `1835`

we may also figure out the correct plugboard is `LR AN EZ HK IJ MQ OT SW UX PV`

#### location

`KURTINVWA KURTINOWA`

After searching it up online, we know it actually refers to `KURTINOWA`

#### route

`NORTHWEST SEFEZ SEBEZ AIRROUTE DIRECTIRN DUBROWKI DUBROWKI OPOTSJHKA OPOTSCHKA`

First we can see `NORTHWEST` as the direction.

after some googling, `SEBEZ` is a location.

no doubt `DUBROWKI` is correct, the 2 repetions are the same, its a location.

after another googling, `OPOTSCHKA` is another location.

#### flag

Finally, we can assemble the informations into the flag, which is

`PUCTF25{KURTINOWA_NORTHWEST_SEBEZ_DUBROWKI_OPOTSCHKA_1835}`

## Enigma and extraction - checkpoint Q&A

Q - Why we only have 9 plugboards? not 11 meh?\
A - In the plugboards, `CC` and `DD` means exchange position of C with C, and D with D. That does nothing, so those 2 isn't counted as a plugboard.
