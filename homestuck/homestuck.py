import copy

from redbot.core import checks, Config
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify, inline
from discord.utils import escape_markdown as md_escape

class Homestuck(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.characters = CHARACTERS

    def get_preset(self, query):
        query = query.lower()
        for preset in self.characters:
            if preset == query or query in self.characters[preset]['aliases']:
                return copy.deepcopy(self.characters[preset])
        else:
            raise ValueError("Preset not found.")



CHARACTERS = {
    "ALPHA TROLLS:\naradia" : {
        "aliases": ["aradia", "aradia megido"],
        "color"  : 0xa10000,
        "quirks" : [
            ("o","0"),
            ("O","0"),
            ("'",""),
        ],
        "rquirks": [
        ]
    },

    "tavros" : {
        "aliases": ["tavros nitram"],
        "color"  : 0xa15000,
        "quirks" : [
        ],
        "rquirks": [
            (r'.', '$U'),
            (r'\b\w', '$L'),
            (r'(^|[^}])([:;][\(\)DP])', r'\1}\2'),
            (r'(^|\s|})[:;]O', r'$L'),
        ]
    },

    "sollux" : {
        "aliases": ["sollux captor"],
        "color"  : 0xa1a100,
        "quirks" : [
            ('i','ii'),
            ('s','2'),
            ('I','II'),
            ('S','2'),
        ],
        "rquirks": [
            (r'\btoo?\b', 'two'),
            (r'\bTOO?\b', 'TWO'),
            (r'\bto(gether|day|niight|morrow)\b', r'two\1'),
            (r'\bTO(GETHER|DAY|NIIGHT|MORROW)\b', r'TWO\1'),
        ]
    },

    "karkat" : {
        "aliases": ["karkat vantas"],
        "color"  : 0x626262,
        "quirks" : [
        ],
        "rquirks": [
            (r'.', '$U'),
        ]
    },

    "nepeta" : {
        "aliases": ["nepeta leijon"],
        "color"  : 0x416600,
        "quirks" : [
            ("'", ''),
        ],
        "rquirks": [
            (r'^', ':33 < '),
            (r'(ee|EE)', '33'),
            (r'\b\w', '$L'),
            (r':3(\s|$)', ':33'),
        ]
    },

    "kanaya" : {
        "aliases": ["kanaya maryam"],
        "color"  : 0x008141,
        "quirks" : [
            ("'", ''),
        ],
        "rquirks": [
            (r'\b\w', '$U'),
        ]
    },

    "terezi" : {
        "aliases": ["terezi pyrope"],
        "color"  : 0x008282,
        "quirks" : [
        ],
        "rquirks": [
            (r'.', '$U'),
            (r'A', '4'),
            (r'I', '1'),
            (r'E', '3'),
        ]
    },

    "vriska" : {
        "aliases": ["vriska serket"],
        "color"  : 0x005682,
        "quirks" : [
            ('(m)', '♏')
        ],
        "rquirks": [
            (r'(b|B)', '8'),
            (r'([^:;]):([\(\)DPO])', '\1::::\2'),
        ]
    },

    "equius" : {
        "aliases": ["equius zahaak"],
        "color"  : 0x000056,
        "quirks" : [
        ],
        "rquirks": [
            (r'^', 'D --> '),
            (r'(?i)x', '%'),
            (r'(?i)loo', '100'),
            (r'(?i)ool', '001'),
            (r'(?i)\bstrong', '$U'),
        ]
    },

    "gamzee" : {
        "aliases": ["gamzee makara"],
        "color"  : 0x2b0057,
        "quirks" : [
        ],
        "rquirks": [
            (r'.*', '$A'),
            (r':Od', ':oD'),
            (r'dO:', 'Do:'),
            (r'(:O|O:)', '$L'),
        ]
    },

    "eridan" : {
        "aliases": ["eridan ampora"],
        "color"  : 0x6a006a,
        "quirks" : [
            ("'", ""),
            ('v', 'vv'),
            ('w', 'ww'),
            ('V', 'VV'),
            ('W', 'WW'),
        ],
        "rquirks": [
            (r'(?i)(in)g\b', '\1'),
        ]
    },

    "feferi" : {
        "aliases": ["feferi peixes"],
        "color"  : 0x77003c,
        "quirks" : [
            ('E', '-E'),
        ],
        "rquirks": [
            (r'(?i)h', ')('),
        ]
    },



    "\nBETA TROLLS:\ndamara" : {
        "aliases": ["damara", "damara megido"],
        "color"  : 0xa10000,
        "quirks" : [
        ],
        "rquirks": [
            (r'.', '$U'),
        ]
    },

    "rufioh" : {
        "aliases": ["rufioh nitram"],
        "color"  : 0xa15000,
        "quirks" : [
            (r'fuck', 'f*ck'),
            (r'damn', 'd*mn'),
            (r'shit', 'sh*t')
        ],
        "rquirks": [
            (r'(?i)i', '1'),
            (r'(?i)\ba(ss)\b', r'*\2'),
            (r'(?i)\b(cr)i(pple)\b', r'\1*\2'),
            (r'(?i)\b(h)e(ll)\b', r'\1*\2'),
            (r'(?i)\b(m)u(tant)\b', r'\1*\2'),
        ]
    },

    "mituna" : {
        "aliases": ["mituna captor"],
        "color"  : 0xa1a100,
        "quirks" : [
        ],
        "rquirks": [
            (r'.', '$U'),
            (r'O', '0'),
            (r'I', '1'),
            (r'E', '3'),
            (r'A', '4'),
            (r'S', '5'),
            (r'T', '7'),
            (r'B', '8'),
        ]
    },

    "kankri" : {
        "aliases": ["kankri vantas"],
        "color"  : 0xff0000,
        "quirks" : [
        ],
        "rquirks": [
            (r'(?i)b', '6'),
            (r'(?i)o', '9'),
        ]
    },

    "meulin" : {
        "aliases": ["meulin leijon"],
        "color"  : 0x416600,
        "quirks" : [
        ],
        "rquirks": [
            (r'.', '$U'),
            (r'^', '(^･ω･^) < '),
            (r'EE', '33'),
        ]
    },

    "porrim" : {
        "aliases": ["porrim maryam"],
        "color"  : 0x008141,
        "quirks" : [
            ("o", "o+"),
            ("0", "0+"),
        ],
        "rquirks": [
            (r'(?i)\bplus\b', '+'),
        ]
    },

    "latula" : {
        "aliases": ["latula pyrope"],
        "color"  : 0x008282,
        "quirks" : [
            ("'", ""),
        ],
        "rquirks": [
            (r'(?i)a', '4'),
            (r'(?i)i', '1'),
            (r'(?i)e', '3'),
            (r'(^|\s|>)[:;8x][dop]', '$U')
        ]
    },

    "aranea" : {
        "aliases": ["aranea serket"],
        "color"  : 0x005682,
        "quirks" : [
            ('(m)', '♏')
        ],
        "rquirks": [
            (r'(b|B)', '8'),
        ]
    },

    "horrus" : {
        "aliases": ["horrus zahaak"],
        "color"  : 0x000056,
        "quirks" : [
        ],
        "rquirks": [
            (r'^', '8=D < '),
            (r'(?i)x', '%'),
            (r'(?i)loo', '100'),
            (r'(?i)ool', '001'),
        ]
    },

    "kurloz" : {
        "aliases": ["kurloz makara"],
        "color"  : 0x2b0057,
        "quirks" : [
        ],
        "rquirks": [
            (r'^', 'SIGNS: < '),
            (r'$', ' >'),
            (r'.', '$U'),
        ]
    },

    "cronus" : {
        "aliases": ["cronus ampora"],
        "color"  : 0x6a006a,
        "quirks" : [
            ('B', '8'),
            ("'", ''),
        ],
        "rquirks": [
            (r'(w|v)', 'rand[wv|vw]'),
            (r'(W|V)', 'rand[WV|VW]'),
        ]
    },

    "meenah" : {
        "aliases": ["meenah peixes"],
        "color"  : 0x77003c,
        "quirks" : [
            ('E', '-E'),
            ('H', ')('),
            ("'", ''),
        ],
        "rquirks": [
        ]
    },


    "\nHIVESWAP:\nxefros" : {
        "aliases": ["xefros", "xefros tritoe"],
        "color"  : 0x680811,
        "quirks" : [
        ],
        "rquirks": [
            ('.', '$L'),
            ('(x|cross|ten|trans)', 'X'),
        ]
    },

    "trizza" : {
        "aliases": ["trizza tethis"],
        "color"  : 0xae015c,
        "quirks" : [
            ('w', 'ψ'),
        ],
        "rquirks": [
        ]
    },

    "diemen" : {
        "aliases": ["diemen xicali"],
        "color"  : 0x6f210e,
        "quirks" : [
        ],
        "rquirks": [
            (r'^', '(|'),
            (r'$', '|)'),
        ]
    },

    "ardata" : {
        "aliases": ["ardata carmia"],
        "color"  : 0x005682,
        "quirks" : [
        ],
        "rquirks": [
            (r'(?i)(i)', r'\1\1\1'),
        ]
    },

    "cirava" : {
        "aliases": ["cirava hermod"],
        "color"  : 0xa2a200,
        "quirks" : [
        ],
        "rquirks": [
        ]
    },

    "amisia" : {
        "aliases": ["amisia erdehn"],
        "color"  : 0x000058,
        "quirks" : [
        ],
        "rquirks": [
            (r'(?i)(u)', r'\1\1'),
        ]
    },

    "skylla" : {
        "aliases": ["skylla koriga"],
        "color"  : 0xa25200,
        "quirks" : [
        ],
        "rquirks": [
            (r'(?i)(y)', r'\1y'),
        ]
    },

    "bronya" : {
        "aliases": ["bronya ursama"],
        "color"  : 0x008342,
        "quirks" : [
        ],
        "rquirks": [
        ]
    },

    "tagora" : {
        "aliases": ["tagora gorjek"],
        "color"  : 0x008282,
        "quirks" : [
        ],
        "rquirks": [
            (r'$', md_escape('\n*_________')),
        ]
    },

    "vikare" : {
        "aliases": ["vikare ratite"],
        "color"  : 0xa15000,
        "quirks" : [
        ],
        "rquirks": [
            (r'(^|$)', r'\\~'),
        ]
    },

    "polypa" : {
        "aliases": ["polypa goezee"],
        "color"  : 0x426800,
        "quirks" : [
        ],
        "rquirks": [
            (r'[,.!?]', r' \* '),
            (r'$', r' *|'),
            (r'\*\s*\*|$', r' *|'),
        ]
    },

    "zebruh" : {
        "aliases": ["zebruh codakk"],
        "color"  : 0x0021cb,
        "quirks" : [
        ],
        "rquirks": [
        ]
    },

    "elwurd" : {
        "aliases": ["?????? elwurd", "??????"],
        "color"  : 0x005682,
        "quirks" : [
        ],
        "rquirks": [
            (r'.', r'$L'),
            (r'l', r'L'),
        ]
    },

    "kuprum" : {
        "aliases": ["kuprum maxlol"],
        "color"  : 0xa2a200,
        "quirks" : [
        ],
        "rquirks": [
            (r'^', '>'),
            (r'([^.])\.', '\\1\n>'),
        ]
    },

    "folykl" : {
        "aliases": ["folykl darane"],
        "color"  : 0xa2a200,
        "quirks" : [
        ],
        "rquirks": [
            (r' ', 'rand[ |  |   |    ]'),
        ]
    },
}
