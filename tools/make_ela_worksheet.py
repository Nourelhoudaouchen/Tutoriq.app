"""
Generate an ELA (English Language Arts) worksheet PDF.

Builds a multi-page PDF from scratch (no external libraries) using the
standard Helvetica / Helvetica-Bold / Helvetica-Oblique fonts so nothing
needs to be embedded.

Run:
    python tools/make_ela_worksheet.py

Output:
    ela_worksheet.pdf  (in the project root)
"""

from __future__ import annotations

import os
import zlib
from dataclasses import dataclass, field
from typing import List, Tuple


# ----- Page setup (US Letter) -------------------------------------------------
PAGE_W, PAGE_H = 612, 792       # points
MARGIN_L, MARGIN_R = 54, 54
MARGIN_T, MARGIN_B = 54, 54
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

# Approximate character widths for Helvetica @ 1pt, used for wrap + centering.
# Good enough for a worksheet layout.
_HELV_WIDTHS = {
    " ": 0.278, "!": 0.278, '"': 0.355, "#": 0.556, "$": 0.556, "%": 0.889,
    "&": 0.667, "'": 0.191, "(": 0.333, ")": 0.333, "*": 0.389, "+": 0.584,
    ",": 0.278, "-": 0.333, ".": 0.278, "/": 0.278,
    "0": 0.556, "1": 0.556, "2": 0.556, "3": 0.556, "4": 0.556,
    "5": 0.556, "6": 0.556, "7": 0.556, "8": 0.556, "9": 0.556,
    ":": 0.278, ";": 0.278, "<": 0.584, "=": 0.584, ">": 0.584,
    "?": 0.556, "@": 1.015,
    "A": 0.667, "B": 0.667, "C": 0.722, "D": 0.722, "E": 0.667, "F": 0.611,
    "G": 0.778, "H": 0.722, "I": 0.278, "J": 0.500, "K": 0.667, "L": 0.556,
    "M": 0.833, "N": 0.722, "O": 0.778, "P": 0.667, "Q": 0.778, "R": 0.722,
    "S": 0.667, "T": 0.611, "U": 0.722, "V": 0.667, "W": 0.944, "X": 0.667,
    "Y": 0.667, "Z": 0.611,
    "[": 0.278, "\\": 0.278, "]": 0.278, "^": 0.469, "_": 0.556, "`": 0.222,
    "a": 0.556, "b": 0.556, "c": 0.500, "d": 0.556, "e": 0.556, "f": 0.278,
    "g": 0.556, "h": 0.556, "i": 0.222, "j": 0.222, "k": 0.500, "l": 0.222,
    "m": 0.833, "n": 0.556, "o": 0.556, "p": 0.556, "q": 0.556, "r": 0.333,
    "s": 0.500, "t": 0.278, "u": 0.556, "v": 0.500, "w": 0.722, "x": 0.500,
    "y": 0.500, "z": 0.500,
    "{": 0.334, "|": 0.260, "}": 0.334, "~": 0.584,
    "\u2019": 0.191, "\u2018": 0.191, "\u201C": 0.333, "\u201D": 0.333,
    "\u2014": 1.000, "\u2013": 0.556,
}


def text_width(s: str, size: float) -> float:
    return sum(_HELV_WIDTHS.get(ch, 0.5) for ch in s) * size


def wrap_text(text: str, size: float, max_w: float) -> List[str]:
    """Greedy word-wrap to fit within max_w points."""
    out: List[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            out.append("")
            continue
        words = paragraph.split(" ")
        line = ""
        for w in words:
            trial = w if not line else f"{line} {w}"
            if text_width(trial, size) <= max_w:
                line = trial
            else:
                if line:
                    out.append(line)
                line = w
        if line:
            out.append(line)
    return out


# ----- PDF stream helpers -----------------------------------------------------

def _pdf_escape(s: str) -> str:
    # Escape special PDF string chars and encode to WinAnsiEncoding.
    s = (
        s.replace("\\", "\\\\")
         .replace("(", "\\(")
         .replace(")", "\\)")
         .replace("\u2019", "'")
         .replace("\u2018", "'")
         .replace("\u201C", '"')
         .replace("\u201D", '"')
         .replace("\u2014", "-")
         .replace("\u2013", "-")
    )
    return s


@dataclass
class Page:
    ops: List[str] = field(default_factory=list)

    def add(self, op: str) -> None:
        self.ops.append(op)


@dataclass
class PDFBuilder:
    pages: List[Page] = field(default_factory=list)

    # drawing state
    cur: Page = field(default_factory=Page)
    y: float = PAGE_H - MARGIN_T

    def new_page(self) -> None:
        self.pages.append(self.cur)
        self.cur = Page()
        self.y = PAGE_H - MARGIN_T

    def finish(self) -> None:
        self.pages.append(self.cur)

    # --- drawing primitives --------------------------------------------------
    def ensure_space(self, needed: float) -> None:
        if self.y - needed < MARGIN_B:
            self.new_page()

    def text(self, s: str, size: float = 11, font: str = "F1",
             x: float = MARGIN_L, indent: float = 0) -> None:
        self.ensure_space(size + 2)
        tx = x + indent
        self.cur.add(
            f"BT /{font} {size} Tf {tx} {self.y - size} Td "
            f"({_pdf_escape(s)}) Tj ET"
        )
        self.y -= size + 4

    def heading(self, s: str, size: float = 16, gap_before: float = 6,
                gap_after: float = 4) -> None:
        self.y -= gap_before
        self.ensure_space(size + gap_after)
        self.cur.add(
            f"BT /F2 {size} Tf {MARGIN_L} {self.y - size} Td "
            f"({_pdf_escape(s)}) Tj ET"
        )
        self.y -= size + gap_after

    def subheading(self, s: str, size: float = 12) -> None:
        self.y -= 4
        self.ensure_space(size + 4)
        self.cur.add(
            f"BT /F2 {size} Tf {MARGIN_L} {self.y - size} Td "
            f"({_pdf_escape(s)}) Tj ET"
        )
        self.y -= size + 4

    def paragraph(self, s: str, size: float = 11, font: str = "F1",
                  indent: float = 0, max_w: float = None) -> None:
        if max_w is None:
            max_w = CONTENT_W - indent
        for line in wrap_text(s, size, max_w):
            self.text(line, size=size, font=font, indent=indent)

    def italic_paragraph(self, s: str, size: float = 11, indent: float = 0):
        self.paragraph(s, size=size, font="F3", indent=indent)

    def hr(self) -> None:
        self.y -= 4
        self.ensure_space(6)
        self.cur.add(
            f"q 0.7 0.7 0.7 RG 0.5 w "
            f"{MARGIN_L} {self.y} m {PAGE_W - MARGIN_R} {self.y} l S Q"
        )
        self.y -= 6

    def answer_lines(self, n: int, gap: float = 18) -> None:
        for _ in range(n):
            self.ensure_space(gap)
            self.y -= gap
            self.cur.add(
                f"q 0.55 0.55 0.55 RG 0.5 w "
                f"{MARGIN_L + 12} {self.y} m "
                f"{PAGE_W - MARGIN_R} {self.y} l S Q"
            )
        self.y -= 4

    def title_block(self, title: str, subtitle: str) -> None:
        # Big centered title
        size = 22
        w = text_width(title, size)
        x = (PAGE_W - w) / 2
        self.cur.add(
            f"BT /F2 {size} Tf {x} {self.y - size} Td "
            f"({_pdf_escape(title)}) Tj ET"
        )
        self.y -= size + 4

        size = 12
        w = text_width(subtitle, size)
        x = (PAGE_W - w) / 2
        self.cur.add(
            f"BT /F3 {size} Tf {x} {self.y - size} Td "
            f"({_pdf_escape(subtitle)}) Tj ET"
        )
        self.y -= size + 10
        self.hr()

    def name_date_row(self) -> None:
        # Two fields: Name _____________   Date ________   Class ________
        self.ensure_space(24)
        size = 11
        # Name label + line
        self.cur.add(
            f"BT /F2 {size} Tf {MARGIN_L} {self.y - size} Td (Name:) Tj ET"
        )
        self.cur.add(
            f"q 0.55 0.55 0.55 RG 0.5 w "
            f"{MARGIN_L + 40} {self.y - size + 1} m "
            f"{MARGIN_L + 260} {self.y - size + 1} l S Q"
        )
        # Date label + line
        self.cur.add(
            f"BT /F2 {size} Tf {MARGIN_L + 280} {self.y - size} Td (Date:) Tj ET"
        )
        self.cur.add(
            f"q 0.55 0.55 0.55 RG 0.5 w "
            f"{MARGIN_L + 320} {self.y - size + 1} m "
            f"{MARGIN_L + 420} {self.y - size + 1} l S Q"
        )
        # Class label + line
        self.cur.add(
            f"BT /F2 {size} Tf {MARGIN_L + 440} {self.y - size} Td (Class:) Tj ET"
        )
        self.cur.add(
            f"q 0.55 0.55 0.55 RG 0.5 w "
            f"{MARGIN_L + 480} {self.y - size + 1} m "
            f"{PAGE_W - MARGIN_R} {self.y - size + 1} l S Q"
        )
        self.y -= size + 14


# ----- Content ----------------------------------------------------------------

PASSAGE = (
    "Maya had always believed the old lighthouse at the edge of her town was "
    "abandoned. Every evening she watched it from her bedroom window, its "
    "windows dark, its paint peeling, its door sealed shut by decades of rust "
    "and neglect. So when, on the night of the storm, a single steady light "
    "blinked to life at the top of the tower, Maya sat up in bed and stared.\n"
    "The next morning, she walked the muddy path to the cliff. The lighthouse "
    "loomed above her, silent again, as though she had imagined it. But there, "
    "tucked beneath the door, was a small notebook wrapped in plastic. Inside, "
    "in careful handwriting, someone had written: \u201CIf you found this, the "
    "keeper has been waiting a long time for company. Come back tomorrow at "
    "sunset.\u201D\n"
    "Maya closed the notebook. Her heart beat quickly, but not with fear. For "
    "the first time in months, she felt curious about something \u2014 truly, "
    "wildly curious."
)

COMPREHENSION_QS = [
    "Where does the story take place, and why is the setting important?",
    "What evidence from the passage shows that Maya thought the lighthouse was abandoned?",
    "How does Maya's feeling change from the beginning of the passage to the end? Use a quote to support your answer.",
    "Predict: what do you think Maya will find when she returns at sunset? Use at least one detail from the text.",
]

VOCAB = [
    ("abandoned",   "left empty or unused; deserted"),
    ("neglect",     "failure to take care of something"),
    ("loomed",      "appeared large, tall, or threatening"),
    ("curious",     "eager to learn or know something"),
    ("keeper",      "a person who looks after or guards something"),
]

VOCAB_SENTENCES = [
    "After years of ________, the old barn was full of dust and broken tools.",
    "The tall trees ________ above the hikers as they walked through the forest.",
    "A zoo ________ knows the name and habits of every animal in their care.",
    "The ________ warehouse had not been used by anyone for nearly a decade.",
    "Alex was so ________ about the experiment that she stayed after class to ask questions.",
]

GRAMMAR_POS = [
    "The small dog barked loudly at the mail carrier.",
    "Yesterday, our teacher carefully explained the difficult problem.",
    "The bright, cheerful students sang a beautiful song.",
]

GRAMMAR_PUNCTUATION = [
    "where did you put my book asked jordan",
    "we visited london paris and rome last summer",
    "although it was raining we still went to the park",
    "mrs garcia my science teacher grew up in mexico city",
]

WRITING_PROMPT = (
    "Imagine you are Maya. Write a one-paragraph journal entry (5\u20137 "
    "sentences) describing what happens when you return to the lighthouse at "
    "sunset. Include at least two sensory details (what you see, hear, smell, "
    "feel, or taste) and one line of dialogue."
)


def build_worksheet() -> PDFBuilder:
    pdf = PDFBuilder()

    # --- Header --------------------------------------------------------------
    pdf.title_block("ELA Practice Worksheet",
                    "Reading \u2022 Vocabulary \u2022 Grammar \u2022 Writing")
    pdf.name_date_row()
    pdf.italic_paragraph(
        "Instructions: Read the passage carefully, then complete each section. "
        "Write in complete sentences where asked. Use the back of the page if "
        "you need more room."
    )

    # --- Part 1: Reading passage --------------------------------------------
    pdf.heading("Part 1: Reading Comprehension")
    pdf.subheading("Passage: \u201CThe Light in the Tower\u201D")
    pdf.paragraph(PASSAGE, size=11)

    pdf.subheading("Answer the questions below in complete sentences.")
    for i, q in enumerate(COMPREHENSION_QS, 1):
        pdf.paragraph(f"{i}. {q}", size=11)
        pdf.answer_lines(3)

    # --- Part 2: Vocabulary --------------------------------------------------
    pdf.heading("Part 2: Vocabulary")
    pdf.italic_paragraph(
        "A. Match each word to its meaning by writing the correct letter on "
        "the line."
    )
    # Two columns: words (left) and meanings (right, shuffled labels A-E)
    shuffled = [
        ("A", VOCAB[2][1]),  # loomed
        ("B", VOCAB[0][1]),  # abandoned
        ("C", VOCAB[4][1]),  # keeper
        ("D", VOCAB[1][1]),  # neglect
        ("E", VOCAB[3][1]),  # curious
    ]
    pdf.ensure_space(16 * len(VOCAB) + 8)
    top_y = pdf.y
    # Left column: word + blank
    for i, (word, _) in enumerate(VOCAB, 1):
        line_y = top_y - (i - 1) * 18
        pdf.cur.add(
            f"BT /F1 11 Tf {MARGIN_L} {line_y - 11} Td "
            f"({i}. {_pdf_escape(word)}) Tj ET"
        )
        pdf.cur.add(
            f"q 0.55 0.55 0.55 RG 0.5 w "
            f"{MARGIN_L + 110} {line_y - 10} m "
            f"{MARGIN_L + 150} {line_y - 10} l S Q"
        )
    # Right column: lettered meanings
    for i, (letter, meaning) in enumerate(shuffled):
        line_y = top_y - i * 18
        # Wrap the meaning to right column width (approx)
        txt = f"{letter}. {meaning}"
        lines = wrap_text(txt, 11, CONTENT_W - 210)
        for k, ln in enumerate(lines[:2]):
            pdf.cur.add(
                f"BT /F1 11 Tf {MARGIN_L + 200} {line_y - 11 - k * 12} Td "
                f"({_pdf_escape(ln)}) Tj ET"
            )
    pdf.y = top_y - len(VOCAB) * 18 - 6

    pdf.italic_paragraph(
        "B. Fill in the blank with the best word from Part A. "
        "(Use each word only once.)"
    )
    for i, s in enumerate(VOCAB_SENTENCES, 1):
        pdf.paragraph(f"{i}. {s}", size=11)
        pdf.y -= 4

    # --- Part 3: Grammar -----------------------------------------------------
    pdf.heading("Part 3: Grammar & Mechanics")
    pdf.italic_paragraph(
        "A. Underline the nouns, circle the verbs, and draw a box around the "
        "adjectives in each sentence."
    )
    for i, s in enumerate(GRAMMAR_POS, 1):
        pdf.paragraph(f"{i}. {s}", size=11)
        pdf.y -= 6

    pdf.italic_paragraph(
        "B. Rewrite each sentence with correct capitalization and punctuation."
    )
    for i, s in enumerate(GRAMMAR_PUNCTUATION, 1):
        pdf.paragraph(f"{i}. {s}", size=11)
        pdf.answer_lines(1)

    # --- Part 4: Writing prompt ---------------------------------------------
    pdf.heading("Part 4: Writing Prompt")
    pdf.paragraph(WRITING_PROMPT, size=11)
    pdf.y -= 4
    # A generous set of writing lines, flowing across pages as needed.
    remaining = 12
    while remaining > 0:
        pdf.answer_lines(1)
        remaining -= 1

    # --- Footer / answer key note -------------------------------------------
    pdf.hr()
    pdf.italic_paragraph(
        "Teacher note: An answer key is on the final page. Remove before "
        "distributing to students.",
        size=9,
    )

    # --- Answer key ----------------------------------------------------------
    pdf.new_page()
    pdf.heading("Answer Key (Teacher Copy)", size=18)
    pdf.subheading("Part 1: Reading Comprehension (sample responses)")
    pdf.paragraph(
        "1. The story takes place in Maya's town, near an old lighthouse on a "
        "cliff. The setting matters because the lighthouse is the mysterious "
        "place that sparks the plot."
    )
    pdf.paragraph(
        "2. The windows were dark, the paint was peeling, and the door was "
        "\u201Csealed shut by decades of rust and neglect.\u201D"
    )
    pdf.paragraph(
        "3. Maya begins passive and bored (\u201Cjust watching\u201D from her "
        "window). By the end she feels \u201Ctruly, wildly curious,\u201D "
        "showing she has become engaged and excited."
    )
    pdf.paragraph(
        "4. Accept any reasonable prediction supported by textual evidence "
        "(e.g., the notebook, the lit tower, the mention of a \u201Ckeeper\u201D)."
    )

    pdf.subheading("Part 2A: Matching")
    pdf.paragraph("1. abandoned \u2014 B     2. neglect \u2014 D     "
                  "3. loomed \u2014 A     4. curious \u2014 E     "
                  "5. keeper \u2014 C")
    pdf.subheading("Part 2B: Fill-in")
    pdf.paragraph(
        "1. neglect     2. loomed     3. keeper     4. abandoned     5. curious"
    )

    pdf.subheading("Part 3A: Parts of speech (key words)")
    pdf.paragraph("1. Nouns: dog, mail carrier. Verb: barked. "
                  "Adjective: small.")
    pdf.paragraph("2. Noun: teacher, problem. Verb: explained. "
                  "Adjective: difficult (adverbs: yesterday, carefully).")
    pdf.paragraph("3. Nouns: students, song. Verb: sang. "
                  "Adjectives: bright, cheerful, beautiful.")

    pdf.subheading("Part 3B: Corrected sentences")
    pdf.paragraph('1. "Where did you put my book?" asked Jordan.')
    pdf.paragraph("2. We visited London, Paris, and Rome last summer.")
    pdf.paragraph("3. Although it was raining, we still went to the park.")
    pdf.paragraph("4. Mrs. Garcia, my science teacher, grew up in Mexico City.")

    pdf.subheading("Part 4: Writing Prompt")
    pdf.paragraph(
        "Accept any on-topic paragraph that (a) is written from Maya's "
        "first-person perspective, (b) includes at least two sensory details, "
        "and (c) contains at least one line of dialogue punctuated correctly."
    )

    pdf.finish()
    return pdf


# ----- Low-level PDF writer ---------------------------------------------------

def build_pdf_bytes(pdf: PDFBuilder) -> bytes:
    # Object layout:
    # 1 Catalog
    # 2 Pages
    # 3..3+N-1 Page objects
    # next: content streams for each page
    # next: three Font objects

    n_pages = len(pdf.pages)
    page_obj_ids = list(range(3, 3 + n_pages))
    content_obj_ids = list(range(3 + n_pages, 3 + 2 * n_pages))
    font1_id = 3 + 2 * n_pages
    font2_id = font1_id + 1
    font3_id = font1_id + 2

    objects: List[Tuple[int, bytes]] = []

    # 1 Catalog
    objects.append(
        (1, b"<< /Type /Catalog /Pages 2 0 R >>")
    )
    # 2 Pages
    kids = " ".join(f"{pid} 0 R" for pid in page_obj_ids).encode()
    objects.append((
        2,
        b"<< /Type /Pages /Count " + str(n_pages).encode()
        + b" /Kids [" + kids + b"] >>",
    ))

    # Page objects
    for pid, cid in zip(page_obj_ids, content_obj_ids):
        pobj = (
            b"<< /Type /Page /Parent 2 0 R "
            b"/MediaBox [0 0 " + str(PAGE_W).encode() + b" " + str(PAGE_H).encode() + b"] "
            b"/Resources << /Font << "
            b"/F1 " + str(font1_id).encode() + b" 0 R "
            b"/F2 " + str(font2_id).encode() + b" 0 R "
            b"/F3 " + str(font3_id).encode() + b" 0 R "
            b">> >> "
            b"/Contents " + str(cid).encode() + b" 0 R >>"
        )
        objects.append((pid, pobj))

    # Content streams
    for page, cid in zip(pdf.pages, content_obj_ids):
        stream_text = "\n".join(page.ops).encode("latin-1", errors="replace")
        compressed = zlib.compress(stream_text)
        obj = (
            b"<< /Length " + str(len(compressed)).encode()
            + b" /Filter /FlateDecode >>\nstream\n"
            + compressed + b"\nendstream"
        )
        objects.append((cid, obj))

    # Fonts
    objects.append((font1_id,
                    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
                    b"/Encoding /WinAnsiEncoding >>"))
    objects.append((font2_id,
                    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
                    b"/Encoding /WinAnsiEncoding >>"))
    objects.append((font3_id,
                    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique "
                    b"/Encoding /WinAnsiEncoding >>"))

    # Assemble
    out = bytearray()
    out += b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"

    # Offsets (sorted by id)
    objects.sort(key=lambda x: x[0])
    offsets = {0: 0}
    for oid, body in objects:
        offsets[oid] = len(out)
        out += f"{oid} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_pos = len(out)
    max_id = max(offsets)
    out += f"xref\n0 {max_id + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for oid in range(1, max_id + 1):
        off = offsets.get(oid, 0)
        out += f"{off:010d} 00000 n \n".encode()

    out += (
        b"trailer\n<< /Size " + str(max_id + 1).encode()
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_pos).encode() + b"\n%%EOF\n"
    )

    return bytes(out)


def main() -> None:
    pdf = build_worksheet()
    data = build_pdf_bytes(pdf)

    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "ela_worksheet.pdf",
    )
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"Wrote {out_path} ({len(data):,} bytes, {len(pdf.pages)} pages)")


if __name__ == "__main__":
    main()
