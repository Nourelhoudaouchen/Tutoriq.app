# Contributing to Tutoriq

Thank you for helping make Tutoriq better for learners around the world! 🎉

## Ways to Contribute

### 📖 Add vocabulary words
Open `index.html` and find the `WORDS` array in the `<script>` section. Each word object looks like this:

```js
{ en:'perseverance', ph:'/pəˌsɪˈvɪərəns/', pos:'noun',
  def:'Continued effort to do or achieve something despite difficulty or failure.',
  ex:'"Her perseverance through years of study finally paid off."',
  fr:'persévérance', ar:'المثابرة' },
```

Fields:
| Field | Meaning |
|-------|---------|
| `en`  | English word |
| `ph`  | IPA phonetic transcription |
| `pos` | Part of speech (`noun`, `verb`, `adjective`, etc.) |
| `def` | Clear, plain-English definition |
| `ex`  | Example sentence in quotes |
| `fr`  | French translation |
| `ar`  | Arabic translation |

Please make sure your word is:
- **Useful for learners** (academic, professional, or exam vocabulary)
- **Correctly defined** (check a dictionary like Merriam-Webster or Oxford)
- **Properly translated** (native speakers' review is welcome)

### 🎯 Add quiz questions
Find the `QUESTIONS` array and add an entry:

```js
{ cat:'Vocabulary', q:'What does "eloquent" mean?',
  opts:['silent', 'angry', 'fluent and persuasive', 'confused'], ans:2,
  exp:'"Eloquent" describes someone who expresses ideas clearly and persuasively.' },
```

Fields:
| Field  | Meaning |
|--------|---------|
| `cat`  | Category: `Vocabulary`, `Grammar`, `IELTS Tip`, `French`, `Arabic` |
| `q`    | The question text |
| `opts` | Array of 4 answer strings |
| `ans`  | Zero-based index of the correct answer |
| `exp`  | Brief explanation shown after answering |

### 🌍 Add or improve translations
If you are a native Arabic or French speaker and spot a mistranslation or can suggest a more natural phrasing, please open an issue or PR.

### 🎨 Improve the UI/UX
The entire site is a single `index.html` file (HTML + CSS + JS). Feel free to improve styling, accessibility, or add new features. Please keep the zero-dependency philosophy — no build tools, no npm.

## How to Submit a Pull Request

1. **Fork** this repository.
2. **Clone** your fork: `git clone https://github.com/<your-username>/Tutoriq.app.git`
3. Make your changes in a new branch: `git checkout -b add-vocabulary-words`
4. Test your changes by opening `index.html` in a browser.
5. **Commit** and **push** to your fork.
6. Open a **Pull Request** against `main`. Describe what you changed and why.

## Code Style

- The project is intentionally dependency-free. Do not introduce npm, bundlers, or frameworks.
- JavaScript should be compatible with modern browsers (no transpilation needed).
- Keep CSS in the `<style>` block and JS in the `<script>` block at the bottom of `index.html`.
- Use descriptive variable names and add brief comments where the logic is non-obvious.

## Reporting Bugs or Suggestions

Open a [GitHub Issue](https://github.com/Nourelhoudaouchen/Tutoriq.app/issues) describing:
- What you expected to happen
- What actually happened
- Steps to reproduce (if a bug)
- Your browser and OS (if relevant)

## Code of Conduct

Be kind and respectful to all contributors. Tutoriq is for everyone who wants to learn.
