# 🕵️ THE ESCAPE — OSINT Detective Division

A text-based digital escape room played entirely in your terminal. You are **Agent Echo**, investigating **10 OSINT-inspired cases** — from a missing journalist to a global hacker collective. Explore evidence, decode ciphers, crack hashes, and solve each case to advance.

No installation, no dependencies — just Python 3 and your terminal.

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

![The Escape gameplay screenshot](screenshots/gameplay.png)

---

## 🎮 How to Play

Clone the repo and run the game:

```bash
git clone https://github.com/abhirup1400-ship-it/TheScape.git
cd TheScape
python3 main.py 
```

That's it. No `pip install` required — the game only uses Python's standard library.

### Requirements
- Python **3.7+**
- A terminal that supports ANSI colors (any modern Linux, macOS, or Windows Terminal / WSL works best. Plain Windows `cmd` will still run the game, just without colors.)

### Commands available in-game

| Command | Description |
|---|---|
| `ls [-a]` | list files in current directory |
| `cat <file>` | view file contents |
| `cd <dir>` | change directory |
| `grep <pattern> <file>` | search for a pattern in a file |
| `base64 -d <file>` | decode base64 |
| `hex <file>` | decode hex / hexdump |
| `xor <file> <key>` | XOR decrypt with a single-character key |
| `rot13 <file>` | apply ROT13 cipher |
| `crack md5 <hash>` | brute-force a 4-digit PIN from an MD5 hash |
| `strings <file>` | extract readable text from binary data |
| `qr <file>` | read a QR code (simulated) |
| `sql <query>` | attempt SQL injection (Case 9 only) |
| `pcap <file>` | analyze a network packet capture (simulated) |
| `submit <evidence>` | manually submit key evidence |
| `solve` | present evidence and close the case |
| `hint` | get a clue (max 3 per case) |
| `progress` | view solved/unsolved cases |
| `tutorial` | read the story guide |
| `help` | show the full command list |

---

## 🗂️ The 10 Cases

1. **The Missing Journalist** — base64
2. **The Art Heist** — hex decoding
3. **The Poisoned CEO** — XOR cipher
4. **The Cyberstalker** — `strings` extraction
5. **The Cold Case** — ROT13
6. **The Diamond Smuggler** — MD5 brute-force
7. **The Hacker Collective** — QR code
8. **The Double Agent** — hidden files
9. **Corporate Espionage** — SQL injection
10. **The Mastermind** — packet capture analysis

---

## 🤝 Contributing

Pull requests are welcome! Feel free to add new cases, puzzle types, or polish the terminal UI.

## 📄 License

Released under the [MIT License](LICENSE) — free to play, modify, and share.
