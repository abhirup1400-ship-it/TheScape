#!/usr/bin/env python3
"""
████████╗██╗  ██╗███████╗███████╗ ██████╗ █████╗ ██████╗ ███████╗
╚══██╔══╝██║  ██║██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝
   ██║   ███████║█████╗  ███████╗██║     ███████║██████╔╝█████╗  
   ██║   ██╔══██║██╔══╝  ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝  
   ██║   ██║  ██║███████╗███████║╚██████╗██║  ██║██║     ███████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝
A Digital Escape Room – 10 Cases, One Detective.
"""

import os
import sys
import base64
import hashlib
import codecs
import time

# ---------- ANSI Colors (work on Linux/macOS) ----------
class C:
    R = '\033[91m'
    G = '\033[92m'
    Y = '\033[93m'
    B = '\033[94m'
    M = '\033[95m'
    C = '\033[96m'
    W = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def cprint(text, color='', end='\n'):
    if os.name == 'posix':
        print(f"{color}{text}{C.END}", end=end)
    else:
        print(text, end=end)

# ---------- Virtual File System ----------
class VFS:
    def __init__(self, files):
        self.files = files

    def list_dir(self, path):
        path = path.rstrip('/') + '/'
        entries = set()
        for f in self.files:
            if f.startswith(path):
                rest = f[len(path):]
                if '/' in rest:
                    entries.add(rest.split('/')[0] + '/')
                else:
                    entries.add(rest)
        return sorted(entries)

    def read(self, path):
        return self.files.get(path)

# ---------- Case Definition ----------
class Case:
    def __init__(self, title, briefing, vfs, check_func, hints):
        self.title = title
        self.briefing = briefing
        self.vfs = vfs
        self.check = check_func
        self.hints = hints

# ---------- Player State ----------
class Player:
    def __init__(self):
        self.cwd = "/home/detective"
        self.flags = {}
        self.hint_used = [0]*10

# ---------- Game Engine ----------
class TheEscape:
    WATERMARK = "═" * 60 + "\n  T H E   E S C A P E   │   O S I N T   D E T E C T I V E   D I V I S I O N\n" + "═" * 60

    def __init__(self, cases):
        self.cases = cases
        self.player = Player()
        self.case_idx = 0
        self.playing = True
        self.startup()

    def startup(self):
        """Intro sequence."""
        os.system('clear' if os.name == 'posix' else 'cls')
        self._draw_watermark()
        time.sleep(0.3)
        self.show_title()
        time.sleep(0.4)
        self.show_instructions()
        time.sleep(0.5)
        input("\nPress ENTER to begin your first case...")
        self.clear_screen()
        self.enter_case()

    def _draw_watermark(self):
        print(C.M + C.BOLD + self.WATERMARK + C.END)

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        self._draw_watermark()

    def show_title(self):
        title = f"""
{C.M}████████╗██╗  ██╗███████╗{C.R}███████╗ ██████╗ █████╗ ██████╗ ███████╗
{C.M}╚══██╔══╝██║  ██║██╔════╝{C.R}██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝
{C.M}   ██║   ███████║█████╗  {C.R}███████╗██║     ███████║██████╔╝█████╗  
{C.M}   ██║   ██╔══██║██╔══╝  {C.R}╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝  
{C.M}   ██║   ██║  ██║███████╗{C.R}███████║╚██████╗██║  ██║██║     ███████╗
{C.M}   ╚═╝   ╚═╝  ╚═╝╚══════╝{C.R}╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝{C.END}
"""
        print(title)
        cprint("   A Digital Escape Room – 10 Cases, One Detective.", C.BOLD)
        print()

    def show_instructions(self):
        cprint("═" * 60, C.B)
        cprint("  HOW TO PLAY", C.BOLD + C.Y)
        cprint("═" * 60, C.B)
        cprint("  • You are Agent Echo, investigating 10 real‑world inspired cases.", C.W)
        cprint("  • Each case contains key evidence (a FLAG) hidden in its files.", C.W)
        cprint("  • Use Linux‑like commands to explore, read, and decode files.", C.W)
        cprint("  • When you find the evidence, type  solve  to close the case.", C.W)
        cprint("  • If you give up, type  hint  for a clue (max 3 per case).", C.W)
        cprint("  • Commands:  ls  cat  cd  grep  base64  hex  xor  rot13", C.C)
        cprint("               crack  strings  qr  sql  pcap  submit  solve", C.C)
        cprint("  • Type  help  for full command list,  tutorial  for story.", C.W)
        cprint("  • Type  progress  to see how far you've come.", C.W)
        cprint("═" * 60, C.B)
        print()

    def enter_case(self):
        if self.case_idx >= len(self.cases):
            self.win()
            return
        case = self.cases[self.case_idx]
        self.player.flags.clear()
        self.player.cwd = "/home/detective"
        cprint(f"\n{'='*60}", C.B)
        cprint(f"  CASE {self.case_idx+1}: {case.title}", C.BOLD + C.B)
        cprint(f"{'='*60}", C.B)
        # Typewriter effect for briefing
        for ch in case.briefing:
            sys.stdout.write(C.C + ch + C.END)
            sys.stdout.flush()
            time.sleep(0.01)
        print()
        cprint("Explore the evidence. Commands: ls, cat, cd, help, hint, solve\n", C.Y)
        self.cmd_ls([])

    def win(self):
        cprint("\n" + "="*60, C.G)
        cprint("  ALL CASES SOLVED! You're a master detective.", C.G + C.BOLD)
        cprint("="*60, C.G)
        self.playing = False

    def check_solution(self):
        case = self.cases[self.case_idx]
        if case.check(self.player):
            cprint(">>> CORRECT! Case closed. <<<", C.G + C.BOLD)
            self.case_idx += 1
            time.sleep(0.5)
            self.clear_screen()
            self.enter_case()
        else:
            cprint("Not enough evidence yet. Keep investigating.", C.R)

    # ---------- Command Handlers ----------
    def cmd_help(self):
        cprint("COMMANDS:", C.BOLD)
        cprint("  ls [-a]            list files in current directory", C.C)
        cprint("  cat <file>         view file contents", C.C)
        cprint("  cd <dir>           change directory", C.C)
        cprint("  grep <pat> <file>  search for pattern in file", C.C)
        cprint("  file <file>        show file type", C.C)
        cprint("  strings <file>     extract readable text from binary", C.C)
        cprint("  base64 -d <file>   decode base64 data", C.C)
        cprint("  hex <file>         decode hex / show hexdump", C.C)
        cprint("  xor <file> <key>   XOR decrypt with a single character key", C.C)
        cprint("  rot13 <file>       apply ROT13 cipher", C.C)
        cprint("  crack md5 <hash>   brute-force 4‑digit PIN from MD5 hash", C.C)
        cprint("  qr <file>          read QR code (simulated)", C.C)
        cprint("  sql <query>        attempt SQL injection (only in Case 9)", C.C)
        cprint("  pcap <file>        analyze network packet capture", C.C)
        cprint("  submit <evidence>  manually submit the key evidence (without FLAG:)", C.C)
        cprint("  solve              present evidence and close case", C.C)
        cprint("  hint               get a clue (max 3 per case)", C.C)
        cprint("  progress           view solved/unsolved cases", C.C)
        cprint("  clear              clear screen", C.C)
        cprint("  tutorial           read the story guide", C.C)
        cprint("  help               this menu", C.C)

    def cmd_tutorial(self):
        cprint("STORY:", C.BOLD)
        cprint("You are Agent Echo, an OSINT detective tracking down cybercriminals.", C.M)
        cprint("Each case is a virtual evidence locker. Use terminal commands to find the key evidence.", C.M)
        cprint("When you find the hidden FLAG, type 'solve' to close the case.", C.M)
        cprint("If stuck, ask for a hint (up to 3 per case).", C.M)

    def cmd_ls(self, args):
        show_hidden = '-a' in args
        vfs = self.cases[self.case_idx].vfs
        entries = vfs.list_dir(self.player.cwd)
        if not show_hidden:
            entries = [e for e in entries if not e.startswith('.')]
        if entries:
            for e in entries:
                if e.endswith('/'):
                    cprint(f"  📁 {e}", C.B)
                else:
                    cprint(f"  📄 {e}", C.G)
        else:
            cprint("  (empty)", C.Y)

    def cmd_cat(self, args):
        if not args:
            return cprint("Usage: cat <file>", C.R)
        fname = args[0]
        path = os.path.join(self.player.cwd, fname).replace('\\', '/')
        data = self.cases[self.case_idx].vfs.read(path)
        if data is None:
            cprint(f"cat: {fname}: No such file", C.R)
            return
        print(data)
        self._auto_detect(data)

    def cmd_cd(self, args):
        if not args:
            self.player.cwd = "/home/detective"
            return
        d = args[0]
        if d == '..':
            self.player.cwd = os.path.dirname(self.player.cwd) or '/'
        else:
            new = os.path.join(self.player.cwd, d).replace('\\', '/')
            vfs = self.cases[self.case_idx].vfs
            if any(f.startswith(new + '/') for f in vfs.files):
                self.player.cwd = new
            else:
                cprint(f"cd: {d}: No such directory", C.R)

    def cmd_grep(self, args):
        if len(args) < 2:
            return cprint("Usage: grep <pattern> <file>", C.R)
        pat, fname = args[0], args[1]
        path = os.path.join(self.player.cwd, fname).replace('\\', '/')
        data = self.cases[self.case_idx].vfs.read(path)
        if data is None:
            return cprint(f"grep: {fname}: No such file", C.R)
        for line in data.split('\n'):
            if pat in line:
                cprint(line, C.C)
                self._auto_detect(line)

    def cmd_base64(self, args):
        if len(args) < 2 or args[0] != '-d':
            return cprint("Usage: base64 -d <file>", C.R)
        fname = args[1]
        path = os.path.join(self.player.cwd, fname).replace('\\', '/')
        data = self.cases[self.case_idx].vfs.read(path)
        if data is None: return cprint("File not found.", C.R)
        try:
            dec = base64.b64decode(data).decode()
            cprint(dec, C.C)
            self._auto_detect(dec)
        except:
            cprint("Invalid base64 data.", C.R)

    def cmd_hex(self, args):
        if not args: return
        fname = args[0]
        path = os.path.join(self.player.cwd, fname).replace('\\', '/')
        data = self.cases[self.case_idx].vfs.read(path)
        if data is None: return
        if isinstance(data, str) and all(c in '0123456789abcdefABCDEF' for c in data):
            try:
                dec = bytes.fromhex(data).decode()
                cprint(dec, C.C)
                self._auto_detect(dec)
            except:
                cprint("Not valid hex.", C.R)
        else:
            hex_str = data.encode().hex()
            cprint(hex_str, C.C)

    def cmd_xor(self, args):
        if len(args) < 2: return cprint("Usage: xor <file> <keychar>", C.R)
        fname, key = args[0], args[1][0]
        path = os.path.join(self.player.cwd, fname).replace('\\', '/')
        data = self.cases[self.case_idx].vfs.read(path)
        if data is None: return
        res = ''.join(chr(ord(c) ^ ord(key)) for c in data)
        cprint(res, C.C)
        self._auto_detect(res)

    def cmd_rot13(self, args):
        if not args: return
        fname = args[0]
        path = os.path.join(self.player.cwd, fname).replace('\\', '/')
        data = self.cases[self.case_idx].vfs.read(path)
        if data is None: return
        res = codecs.decode(data, 'rot_13')
        cprint(res, C.C)
        self._auto_detect(res)

    def cmd_crack(self, args):
        if len(args) < 2 or args[0] != 'md5': return cprint("Usage: crack md5 <hash>", C.R)
        h = args[1]
        cprint("Brute forcing 4-digit PIN...", C.Y)
        for i in range(10000):
            pin = f"{i:04d}"
            if hashlib.md5(pin.encode()).hexdigest() == h:
                cprint(f"PIN cracked: {pin}", C.G + C.BOLD)
                self.player.flags['pin'] = pin
                return
        cprint("PIN not found (only 4 digits).", C.R)

    def cmd_strings(self, args):
        if not args: return
        fname = args[0]
        path = os.path.join(self.player.cwd, fname).replace('\\', '/')
        data = self.cases[self.case_idx].vfs.read(path)
        if data is None: return
        raw = data if isinstance(data, bytes) else data.encode()
        out = ""
        for b in raw:
            if 32 <= b < 127:
                out += chr(b)
            else:
                if len(out) >= 4:
                    print(out)
                    self._auto_detect(out)
                out = ""
        if len(out) >= 4:
            print(out)
            self._auto_detect(out)

    def cmd_qr(self, args):
        if not args: return
        cprint("Scanning QR code... (simulated)", C.Y)
        fname = args[0]
        path = os.path.join(self.player.cwd, fname).replace('\\', '/')
        data = self.cases[self.case_idx].vfs.read(path)
        if data:
            print(data)
            self._auto_detect(data)

    def cmd_sql(self, args):
        if self.case_idx != 8:
            return cprint("SQL injection not available here.", C.R)
        query = ' '.join(args)
        if "' OR 1=1 --" in query or "1=1" in query:
            cprint("Bypassed login! Secret data: FLAG: injection_master", C.G)
            self.player.flags['flag'] = "injection_master"
        else:
            cprint("Query executed, no results.", C.R)

    def cmd_pcap(self, args):
        if not args: return
        cprint("Analyzing packets...", C.Y)
        fname = args[0]
        path = os.path.join(self.player.cwd, fname).replace('\\', '/')
        data = self.cases[self.case_idx].vfs.read(path)
        if data:
            print(data)
            self._auto_detect(data)

    def cmd_submit(self, args):
        if not args: return cprint("Usage: submit <evidence>", C.R)
        self.player.flags['flag'] = ' '.join(args)
        self.check_solution()

    def cmd_hint(self):
        case = self.cases[self.case_idx]
        used = self.player.hint_used[self.case_idx]
        if used >= 3:
            cprint("No more clues for this case.", C.Y)
            return
        hint = case.hints[used]
        self.player.hint_used[self.case_idx] += 1
        cprint(f"Clue #{used+1}: {hint}", C.M)

    def cmd_progress(self):
        print()
        for i, case in enumerate(self.cases):
            status = "[✓]" if i < self.case_idx else "[ ]"
            color = C.G if i < self.case_idx else C.W
            cprint(f"  {status} Case {i+1}: {case.title}", color)
        print()

    def _auto_detect(self, text):
        if isinstance(text, str) and "FLAG:" in text:
            flag = text.split("FLAG:")[1].strip()
            self.player.flags['flag'] = flag
            cprint("*** Key evidence found! Type 'solve' to close the case. ***", C.Y + C.BOLD)

    def run(self):
        while self.playing:
            try:
                prompt = f"{C.B}[🔍 TheEscape]{C.END} {C.C}Case {self.case_idx+1}{C.END} {C.W}{self.player.cwd}{C.END}> "
                cmd = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye, detective.")
                break
            if not cmd:
                continue
            parts = cmd.split()
            c = parts[0].lower()
            args = parts[1:]

            if c == 'help': self.cmd_help()
            elif c == 'tutorial': self.cmd_tutorial()
            elif c == 'clear':
                self.clear_screen()
                case = self.cases[self.case_idx]
                cprint(f"\n{'='*60}", C.B)
                cprint(f"  CASE {self.case_idx+1}: {case.title}", C.BOLD + C.B)
                cprint(f"{'='*60}", C.B)
                cprint(case.briefing, C.C)
                cprint("Explore the evidence.\n", C.Y)
            elif c == 'ls': self.cmd_ls(args)
            elif c == 'cat': self.cmd_cat(args)
            elif c == 'cd': self.cmd_cd(args)
            elif c == 'grep': self.cmd_grep(args)
            elif c == 'base64': self.cmd_base64(args)
            elif c == 'hex': self.cmd_hex(args)
            elif c == 'xor': self.cmd_xor(args)
            elif c == 'rot13': self.cmd_rot13(args)
            elif c == 'crack': self.cmd_crack(args)
            elif c == 'strings': self.cmd_strings(args)
            elif c == 'qr': self.cmd_qr(args)
            elif c == 'sql': self.cmd_sql(args)
            elif c == 'pcap': self.cmd_pcap(args)
            elif c == 'submit': self.cmd_submit(args)
            elif c == 'solve': self.check_solution()
            elif c == 'hint': self.cmd_hint()
            elif c == 'progress': self.cmd_progress()
            else:
                cprint(f"Unknown command '{c}'. Type 'help'.", C.R)

# ---------- Build 10 Cases (OSINT inspired) ----------
def build_cases():
    cases = []

    # Case 1: Missing Journalist – base64
    vfs1 = VFS({
        "/home/detective/email.txt": "From: unknown@darkmail.com\nAttachment: report.txt\n\nContent: I have the documents. See attached.",
        "/home/detective/report.txt": base64.b64encode(b"FLAG: whistleblower_2024").decode()
    })
    cases.append(Case(
        "Case 1 - The Missing Journalist",
        "A journalist vanished after sending this email. The attachment may hold the clue.",
        vfs1,
        lambda p: p.flags.get('flag') == 'whistleblower_2024',
        ["Read the email first.", "Use base64 -d on the attachment.", "The decoded text contains the flag."]
    ))

    # Case 2: Art Heist – hex
    vfs2 = VFS({
        "/home/detective/invoice.txt": "Purchased painting 'Starry Night' for $10M.\nTransaction ID: 464c41473a206c6f6f7665725f6f6666696365",
        "/home/detective/hint.txt": "The transaction ID looks odd. It might be hex encoded."
    })
    cases.append(Case(
        "Case 2 - The Art Heist",
        "A stolen painting was sold on the black market. The invoice contains a suspicious code.",
        vfs2,
        lambda p: p.flags.get('flag') == 'loover_office',
        ["Look at invoice.txt.", "Decode the hex string with 'hex invoice.txt'.", "The decoded message is the location."]
    ))

    # Case 3: Poisoned CEO – XOR
    key = 'X'
    xor_data = ''.join(chr(ord(c) ^ ord(key)) for c in "FLAG: revenge_is_sweet")
    vfs3 = VFS({
        "/home/detective/note.txt": xor_data,
        "/home/detective/key.txt": "I always use the same single letter key: X"
    })
    cases.append(Case(
        "Case 3 - The Poisoned CEO",
        "A handwritten note found in the CEO's office is garbled. It may be XOR encrypted.",
        vfs3,
        lambda p: p.flags.get('flag') == 'revenge_is_sweet',
        ["Read key.txt to learn the XOR key.", "Use 'xor note.txt X' to decrypt.", "The flag will be revealed."]
    ))

    # Case 4: Cyberstalker – strings
    fake_img = b'\x89PNG\r\n' + b'FLAG: stalker_identified' + b'\x00\xff'
    vfs4 = VFS({
        "/home/detective/photo.png": fake_img,
        "/home/detective/hint.txt": "The stalker sent this photo. Run strings to see if any hidden text is embedded."
    })
    cases.append(Case(
        "Case 4 - The Cyberstalker",
        "A photo sent by the stalker may contain hidden information.",
        vfs4,
        lambda p: p.flags.get('flag') == 'stalker_identified',
        ["Use 'strings photo.png'.", "Read the output carefully.", "The flag is in the extracted text."]
    ))

    # Case 5: Cold Case – ROT13
    rot = codecs.encode("FLAG: old_secrets", 'rot_13')
    vfs5 = VFS({
        "/home/detective/diary.txt": rot,
        "/home/detective/hint.txt": "The diary entries look shifted. Maybe ROT13?"
    })
    cases.append(Case(
        "Case 5 - The Cold Case",
        "An old diary found in a cold case. The entries are in a simple cipher.",
        vfs5,
        lambda p: p.flags.get('flag') == 'old_secrets',
        ["Use 'rot13 diary.txt' to decode.", "The flag appears automatically."]
    ))

    # Case 6: Diamond Smuggler – MD5 crack
    pin = "4829"
    hash_val = hashlib.md5(pin.encode()).hexdigest()
    vfs6 = VFS({
        "/home/detective/locker_hash.txt": hash_val,
        "/home/detective/hint.txt": "The smuggler used a 4‑digit PIN to lock the shipment. Crack the MD5 hash."
    })
    cases.append(Case(
        "Case 6 - The Diamond Smuggler",
        "A hash found on a locker receipt. Crack it to find the PIN and the location.",
        vfs6,
        lambda p: p.flags.get('pin') == pin,
        ["Use 'crack md5 <hash>' to brute-force.", "The PIN is 4829, that is the evidence.", "Then use 'submit 4829' or 'solve'."]
    ))

    # Case 7: Hacker Collective – QR
    vfs7 = VFS({
        "/home/detective/qr.png": "FLAG: ransomware_group",
        "/home/detective/hint.txt": "Scan the QR code found on the ransom note."
    })
    cases.append(Case(
        "Case 7 - The Hacker Collective",
        "A QR code was left by the attackers. It might lead to their identity.",
        vfs7,
        lambda p: p.flags.get('flag') == 'ransomware_group',
        ["Use 'qr qr.png' to decode.", "The flag is displayed."]
    ))

    # Case 8: Double Agent – hidden file
    vfs8 = VFS({
        "/home/detective/.secret_intel": "FLAG: double_cross",
        "/home/detective/hint.txt": "There might be a hidden file in this directory."
    })
    cases.append(Case(
        "Case 8 - The Double Agent",
        "An agent left hidden intelligence. Use 'ls -a' to find it.",
        vfs8,
        lambda p: p.flags.get('flag') == 'double_cross',
        ["List all files with 'ls -a'.", "Read the hidden file.", "The flag is inside."]
    ))

    # Case 9: Corporate Espionage – SQL injection
    vfs9 = VFS({
        "/home/detective/login.html": "<form>Username: <input name='user'><br>Password: <input name='pass'></form>",
        "/home/detective/hint.txt": "The login is vulnerable to SQL injection. Try to bypass it."
    })
    cases.append(Case(
        "Case 9 - Corporate Espionage",
        "A leaked internal login page. Inject SQL to gain access to secret data.",
        vfs9,
        lambda p: p.flags.get('flag') == 'injection_master',
        ["Use 'sql' command with an injection payload.", "Try: sql ' OR 1=1 --", "The flag will be revealed."]
    ))

    # Case 10: Mastermind – pcap
    vfs10 = VFS({
        "/home/detective/traffic.pcap": "Packet 1: SYN ... Packet 5: FLAG: mastermind_exposed",
        "/home/detective/hint.txt": "Analyze the network capture to find the final clue."
    })
    cases.append(Case(
        "Case 10 - The Mastermind",
        "Intercepted network traffic may contain the identity of the mastermind.",
        vfs10,
        lambda p: p.flags.get('flag') == 'mastermind_exposed',
        ["Use 'pcap traffic.pcap' to analyze.", "Read the output.", "The flag is in the packets."]
    ))

    return cases

if __name__ == "__main__":
    game = TheEscape(build_cases())
    game.run()