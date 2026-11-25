"""Generate UML sequence diagrams (SVG) in the style of the original Clock-in / Clock-out diagrams."""
import sys
from xml.sax.saxutils import escape

YELLOW = "#FFC940"
GRAY = "#9a9a9a"
FONT = "Inter, DejaVu Sans, sans-serif"
ROW = 46          # vertical space per message
TOP = 210         # y where lifelines start
BAR_W = 26


class Diagram:
    def __init__(self, title, participants, width):
        self.title = title
        self.p = {k: (x, kind, label) for k, x, kind, label in participants}
        self.order = [k for k, *_ in participants]
        self.width = width
        self.y = TOP + 40
        self.items = []          # svg fragments drawn above frames
        self.frames = []         # (x1, y1, x2, y2, tag, guard)
        self.bars = []           # (participant, y1, y2, offset)
        self.open_frames = []
        self.created = {}        # participant -> y of creation box

    # ---------- primitives ----------
    def x(self, k, side=0):
        return self.p[k][0] + side * BAR_W / 2

    def text(self, x, y, s, size=15, anchor="start", weight="normal", fill="#222"):
        self.items.append(
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')

    def arrow(self, x1, x2, y, label, dashed=False):
        dash = ' stroke-dasharray="3,4"' if dashed else ""
        self.items.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{GRAY}" '
                          f'stroke-width="1.8"{dash}/>')
        d = 1 if x2 > x1 else -1
        self.items.append(f'<polygon points="{x2},{y} {x2-12*d},{y-5} {x2-12*d},{y+5}" fill="{GRAY}"/>')
        lx = min(x1, x2) + 22 if not dashed and d > 0 and abs(x2 - x1) > 600 else (x1 + x2) / 2
        anchor = "start" if lx != (x1 + x2) / 2 else "middle"
        self.text(lx, y - 9, label, anchor=anchor)

    # ---------- messages ----------
    def call(self, a, b, label, bar=None):
        """Synchronous call a -> b. bar=(rows) draws an activation on b for that many rows."""
        d = 1 if self.x(b) > self.x(a) else -1
        x1 = self.x(a, d)
        x2 = self.x(b, -d)
        self.arrow(x1, x2, self.y, label)
        if bar:
            self.bars.append((b, self.y - 8, self.y + ROW * bar - 20))
        self.y += ROW

    def ret(self, a, b, label):
        d = 1 if self.x(b) > self.x(a) else -1
        self.arrow(self.x(a, d), self.x(b, -d), self.y, label, dashed=True)
        self.y += ROW

    def self_call(self, a, label):
        x = self.x(a, 1)
        y = self.y
        self.items.append(f'<path d="M{x},{y-8} C{x+40},{y-8} {x+40},{y+12} {x+2},{y+12}" '
                          f'fill="none" stroke="{GRAY}" stroke-width="1.8"/>')
        self.items.append(f'<polygon points="{x},{y+12} {x+11},{y+7} {x+11},{y+17}" fill="{GRAY}"/>')
        self.text(x + 48, y + 8, label)
        self.y += ROW

    def create(self, a, b, label):
        """Create message: dotted arrow to an object box that appears at this height."""
        x2 = self.p[b][0]
        lab = self.p[b][2]
        w = 9 * len(lab) + 20
        self.arrow(self.x(a, 1), x2 - w / 2, self.y, label, dashed=True)
        self.items.append(f'<rect x="{x2-w/2}" y="{self.y-16}" width="{w}" height="30" '
                          f'fill="#fff" stroke="#333" stroke-width="1.4"/>')
        self.text(x2, self.y + 5, lab, size=16, anchor="middle")
        self.created[b] = self.y + 14
        self.bars.append((b, self.y + 14, self.y + ROW + 6))
        self.y += ROW

    def gap(self, h=18):
        self.y += h

    # ---------- frames ----------
    def opt(self, guard, x1, x2, tag="Opt"):
        self.gap(14)
        self.open_frames.append((x1, self.y, x2, tag, guard))
        self.y += 48

    def end(self):
        x1, y1, x2, tag, guard = self.open_frames.pop()
        self.frames.append((x1, y1, x2, self.y - 10, tag, guard))
        self.gap(10)

    def ref(self, text, x1, x2):
        """UML interaction use: a 'ref' frame pointing to another diagram."""
        self.gap(4)
        h = 58
        self.frames.append((x1, self.y - 10, x2, self.y - 10 + h, "ref", None))
        self.text((x1 + x2) / 2 + 20, self.y + 28, text, size=16, anchor="middle", weight="600")
        self.y += h + 8

    # ---------- render ----------
    def icon(self, k):
        x, kind, label = self.p[k]
        cy = 130
        s = []
        if kind == "actor":
            s.append(f'<circle cx="{x}" cy="{cy-28}" r="9" fill="none" stroke="#333" stroke-width="1.5"/>')
            s.append(f'<path d="M{x},{cy-19} L{x},{cy+8} M{x-15},{cy-8} L{x+15},{cy-8} '
                     f'M{x},{cy+8} L{x-12},{cy+30} M{x},{cy+8} L{x+12},{cy+30}" stroke="#333" '
                     f'stroke-width="1.5" fill="none"/>')
        elif kind == "boundary":
            s.append(f'<circle cx="{x+12}" cy="{cy}" r="27" fill="#fff" stroke="#222" stroke-width="2"/>')
            s.append(f'<path d="M{x-38},{cy-17} L{x-38},{cy+17} M{x-38},{cy} L{x-15},{cy}" '
                     f'stroke="#222" stroke-width="2"/>')
        elif kind == "control":
            s.append(f'<circle cx="{x}" cy="{cy}" r="27" fill="#fff" stroke="#222" stroke-width="2"/>')
            s.append(f'<path d="M{x+6},{cy-36} L{x-3},{cy-27} L{x+6},{cy-19}" stroke="#222" '
                     f'stroke-width="2" fill="none"/>')
        elif kind == "entity":
            s.append(f'<circle cx="{x}" cy="{cy}" r="27" fill="#fff" stroke="#222" stroke-width="2"/>')
            s.append(f'<line x1="{x-27}" y1="{cy+31}" x2="{x+27}" y2="{cy+31}" stroke="#222" stroke-width="2"/>')
        if kind != "created":
            s.append(f'<text x="{x}" y="{cy+56}" font-family="{FONT}" font-size="13" font-weight="600" '
                     f'fill="#222" text-anchor="middle">{escape(label)}</text>')
        return "".join(s)

    def svg(self):
        H = self.y + 60
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{H}" '
               f'viewBox="0 0 {self.width} {H}">',
               f'<rect width="100%" height="100%" fill="#fafafa"/>',
               f'<rect x="30" y="28" width="190" height="40" fill="#6e6a6a"/>',
               f'<text x="125" y="55" font-family="{FONT}" font-size="20" font-weight="700" fill="#fff" '
               f'text-anchor="middle">{escape(self.title)}</text>']
        for k in self.order:
            x, kind, _ = self.p[k]
            y0 = self.created.get(k, TOP)
            out.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{H-30}" stroke="{GRAY}" '
                       f'stroke-width="1.5" stroke-dasharray="6,6"/>')
            out.append(self.icon(k))
        for k, y1, y2 in self.bars:
            x = self.p[k][0]
            out.append(f'<rect x="{x-BAR_W/2}" y="{y1}" width="{BAR_W}" height="{y2-y1}" fill="{YELLOW}"/>')
        for x1, y1, x2, y2, tag, guard in self.frames:
            fill = "#fff" if tag == "ref" else "none"
            out.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="{fill}" '
                       f'stroke="#222" stroke-width="1.4"/>')
            tw = 52
            out.append(f'<path d="M{x1},{y1+28} L{x1+tw},{y1+28} L{x1+tw+8},{y1+20} L{x1+tw+8},{y1} " '
                       f'fill="#fff" stroke="#222" stroke-width="1.4"/>')
            out.append(f'<text x="{x1+tw/2+3}" y="{y1+19}" font-family="{FONT}" font-size="15" '
                       f'font-weight="700" fill="#111" text-anchor="middle">{tag}</text>')
            if guard:
                out.append(f'<text x="{x1+tw+18}" y="{y1+19}" font-family="{FONT}" font-size="15" '
                           f'fill="#222">{escape(guard)}</text>')
        out += self.items
        out.append("</svg>")
        return "\n".join(out)


PARTS = [
    ("actor", 95, "actor", ":Worker"),
    ("ui", 420, "boundary", ":ClockKioskUI"),
    ("ctl", 780, "control", ":ClockController"),
    ("worker", 1130, "entity", ":Worker"),
    ("shift", 1260, "entity", ":Shift"),
    ("sched", 1390, "entity", ":ScheduledShift"),
    ("roster", 1520, "boundary", ":LiveRosterUI"),
]
W = 1760
L, R_UI = 55, 840          # frame spanning actor..controller
R_ALL = W - 40


def clock_in():
    parts = PARTS + [("new", 1660, "created", "shift:Shift")]
    d = Diagram("Clock-in", parts, W + 20)
    start = d.y
    d.call("actor", "ui", "1: tapBadge(badgeID)")
    ctl_start = d.y
    d.call("ui", "ctl", "2: handleBadgeTap(badgeID, stationID)")
    d.call("ctl", "worker", "3: findActiveByBadge(badgeID)", bar=1.4)
    d.ret("worker", "ctl", "4: worker")

    d.opt("[worker not found]", L, R_UI)
    d.ret("ctl", "ui", '5: showError("Unknown badge")')
    d.ret("ui", "actor", '6: "Unknown badge"')
    d.end()

    d.opt("[worker found]", 740, 1310)
    d.call("ctl", "shift", "7: findOpenShift(workerID)", bar=1.4)
    d.ret("shift", "ctl", "8: openShift")
    d.end()

    d.opt("[worker found and already clocked in]", L, R_UI + 40)
    d.ref("Clock Out  (continue with 7.2)", L + 120, R_UI - 80)
    d.end()

    d.opt("[worker found and not clocked in]", 740, 1450)
    d.call("ctl", "sched", "9: findMatching(workerID, stationID, now)", bar=1.4)
    d.ret("sched", "ctl", "10: scheduledShift")
    d.end()

    d.opt("[scheduledShift found]", 740, 1110)
    d.self_call("ctl", "11: minutesLate := computeMinutesLate()")
    d.end()

    d.opt("[worker found and not clocked in]", L, R_ALL)
    d.create("ctl", "new", "12: create(workerID, stationID, now, scheduledShiftID)")
    d.ret("new", "ctl", "13: shift")
    d.call("ctl", "roster", "14: addToRoster(workerID, worker.firstName, stationID, now)", bar=1.1)
    d.gap(20)
    d.ret("ctl", "ui", "15: showWelcome(worker.firstName, minutesLate)")
    d.ret("ui", "actor", '16: "Welcome, <name>" (+ minutes late)')
    d.end()
    d.bars.insert(0, ("ui", start - 8, d.y - 30))
    d.bars.insert(0, ("ctl", ctl_start - 8, d.y - 30))
    return d


def clock_out():
    parts = [p if p[0] != "shift" else ("shift", 1260, "entity", "openShift:Shift") for p in PARTS]
    d = Diagram("Clock out", parts, W)
    start = d.y
    d.call("actor", "ui", "1: tapBadge(badgeID)")
    ctl_start = d.y
    d.call("ui", "ctl", "2: handleBadgeTap(badgeID, stationID)")
    d.call("ctl", "worker", "3: findActiveByBadge(badgeID)", bar=1.4)
    d.ret("worker", "ctl", "4: worker")

    d.opt("[worker not found]", L, R_UI)
    d.ret("ctl", "ui", '5: showError("Unknown badge")')
    d.ret("ui", "actor", '6: "Unknown badge"')
    d.end()

    d.opt("[worker found]", 740, 1330)
    d.call("ctl", "shift", "7: findOpenShift(workerID)", bar=1.4)
    d.ret("shift", "ctl", "8: openShift")
    d.end()

    d.opt("[worker found and not clocked in]", L, R_UI + 40)
    d.ref("Clock In  (continue with 7.1)", L + 120, R_UI - 80)
    d.end()

    d.opt("[clocked in]", L, R_ALL)
    d.call("ctl", "shift", "9: close(now)", bar=1.4)
    d.ret("shift", "ctl", "10: duration")
    d.call("ctl", "roster", "11: removeFromRoster(workerID)", bar=1.1)
    d.gap(10)
    d.ret("ctl", "ui", "12: showClockOut(worker.firstName, duration)")
    d.ret("ui", "actor", '13: "Shift length: <h> h <m> min"')
    d.end()

    d.opt("[linked to scheduled shift]", 740, 1460)
    d.call("ctl", "sched", "14: getTimes(scheduledShiftID)", bar=1.4)
    d.ret("sched", "ctl", "15: times")
    d.call("ctl", "shift", "16: setFlag(status)", bar=1.0)
    d.end()
    d.bars.insert(0, ("ui", start - 8, d.y - 30))
    d.bars.insert(0, ("ctl", ctl_start - 8, d.y - 30))
    return d


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../img"
    open(f"{out}/sequence-clock-in.svg", "w").write(clock_in().svg())
    open(f"{out}/sequence-clock-out.svg", "w").write(clock_out().svg())
