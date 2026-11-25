"""Hand-laid ShiftDeck use case diagram (landscape) in the PlantUML visual style."""
from xml.sax.saxutils import escape

F = "Inter, DejaVu Sans, sans-serif"
W, H = 1420, 1110
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="100%" height="100%" fill="#ffffff"/>',
       '<defs><marker id="open" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto">'
       '<path d="M0,0 L10,5 L0,10" fill="none" stroke="#333" stroke-width="1.4"/></marker>'
       '<marker id="tri" viewBox="0 0 12 12" refX="12" refY="6" markerWidth="14" markerHeight="14" orient="auto">'
       '<path d="M0,0 L12,6 L0,12 z" fill="#fff" stroke="#333" stroke-width="1.2"/></marker></defs>']
lines, shapes = [], []

UC = {}  # id -> (cx, cy, rx, ry)


def box(x1, y1, x2, y2, title, size=15):
    shapes.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="6" fill="none" stroke="#333" stroke-width="1.3"/>')
    shapes.append(f'<text x="{(x1+x2)/2}" y="{y1+20}" font-family="{F}" font-size="{size}" font-weight="700" text-anchor="middle" fill="#111">{escape(title)}</text>')


def uc(i, cx, cy, label, rx=92):
    parts = label.split("\n")
    ry = 22 if len(parts) == 1 else 27
    UC[i] = (cx, cy, rx, ry)
    shapes.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#F2F2F2" stroke="#333" stroke-width="1.2"/>')
    y0 = cy + 5 - (len(parts) - 1) * 8.5
    for k, p in enumerate(parts):
        shapes.append(f'<text x="{cx}" y="{y0 + k*17}" font-family="{F}" font-size="14" text-anchor="middle" fill="#111">{escape(p)}</text>')


ACT = {}


def actor(i, x, y, label):
    ACT[i] = (x, y)
    s = (f'<circle cx="{x}" cy="{y-30}" r="9" fill="#F2F2F2" stroke="#333" stroke-width="1.3"/>'
         f'<path d="M{x},{y-21} L{x},{y+4} M{x-15},{y-11} L{x+15},{y-11} M{x},{y+4} L{x-12},{y+26} M{x},{y+4} L{x+12},{y+26}" stroke="#333" stroke-width="1.3" fill="none"/>'
         f'<text x="{x}" y="{y+46}" font-family="{F}" font-size="15" text-anchor="middle" fill="#111">{escape(label)}</text>')
    shapes.append(s)


def edge_pt(i, tx, ty):
    import math
    cx, cy, rx, ry = UC[i]
    dx, dy = tx - cx, ty - cy
    t = 1 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + dx * t, cy + dy * t


def assoc(a, u):
    ax, ay = ACT[a]
    cx, cy, rx, ry = UC[u]
    side = 1 if cx > ax else -1
    ax2 = ax + 20 * side
    ex, ey = cx - side * rx, cy
    lines.append(f'<line x1="{ax2}" y1="{ay-8}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#333" stroke-width="1.2"/>')


def dep(a, b, label, lx=0, ly=0):
    bx, by = UC[b][0], UC[b][1]
    ax, ay = UC[a][0], UC[a][1]
    x1, y1 = edge_pt(a, bx, by)
    x2, y2 = edge_pt(b, ax, ay)
    lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#333" stroke-width="1.2" stroke-dasharray="6,5" marker-end="url(#open)"/>')
    shapes.append(f'<text x="{(x1+x2)/2+lx}" y="{(y1+y2)/2-6+ly}" font-family="{F}" font-size="13" text-anchor="middle" fill="#111">&#171;{label}&#187;</text>')


# system and groups
box(200, 30, 1210, 975, "ShiftDeck", 16)
box(225, 65, 690, 440, "Clocking")
box(725, 65, 1185, 440, "Supervision and monitoring")
box(225, 465, 690, 895, "Worker self-service")
box(725, 465, 1185, 895, "Scheduling and admin")

# Clocking
uc("CI", 330, 170, "UC-02 Clock In", rx=98)
uc("CO", 465, 365, "UC-03 Clock Out", rx=98)
uc("RWI", 565, 105, "UC-05 Record Walk-In", rx=112)
uc("VB", 580, 250, "UC-04 Verify Badge", rx=104)
# Worker self-service
for k, (i, lab) in enumerate([("VMS", "UC-06 View My Schedule"), ("COS", "UC-07 Claim Open Shift"), ("RSS", "UC-08 Request Shift Swap"),
                               ("RSR", "UC-09 Respond to\nSwap Request"), ("RTO", "UC-11 Request Time Off"), ("SA", "UC-13 Set Availability")]):
    uc(i, 457, 520 + k * 70, lab, rx=112)
# Supervision
for k, (i, lab) in enumerate([("FCO", "UC-15 Force Clock-Out"), ("ASR", "UC-10 Approve\nSwap Request"), ("DTOR", "UC-12 Decide Time-Off\nRequest"),
                               ("VLR", "UC-14 View Live Roster"), ("VT", "UC-21 View Timesheet"), ("ET", "UC-20 Export Timesheet")]):
    uc(i, 1010, 108 + k * 60, lab, rx=112)
# Scheduling
for k, (i, lab) in enumerate([("EDT", "UC-16 Edit Demand\nTemplate"), ("GWS", "UC-17 Generate Weekly\nSchedule"), ("SHC", "UC-23 Set Hour Caps"),
                               ("MUA", "UC-22 Manage User\nAccounts"), ("PS", "UC-19 Publish Schedule")]):
    uc(i, 1062, 515 + k * 80, lab, rx=112)
uc("ASD", 832, 665, "UC-18 Adjust Schedule\nDraft", rx=100)
uc("LI", 705, 935, "UC-01 Log In", rx=82)

# actors
actor("Worker", 95, 690, "Worker")
actor("Supervisor", 1310, 215, "Supervisor")
actor("Manager", 1310, 680, "Manager")
actor("Email", 1365, 905, "Email System")
actor("Employee", 705, 1045, "Employee")

for u in ["CI", "CO", "VMS", "COS", "RSS", "RSR", "RTO", "SA"]:
    assoc("Worker", u)
for u in ["FCO", "ASR", "DTOR", "VLR", "VT"]:
    assoc("Supervisor", u)
for u in ["VLR", "VT", "ET", "EDT", "GWS", "SHC", "MUA", "PS"]:
    assoc("Manager", u)
# Publish -> Email System
ex, ey = edge_pt("PS", 1345, 890)
lines.append(f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="1345" y2="890" stroke="#333" stroke-width="1.2"/>')
# Employee -- Log In
lines.append('<line x1="705" y1="1005" x2="705" y2="957" stroke="#333" stroke-width="1.2"/>')

dep("CI", "VB", "include", 0, -4)
dep("CO", "VB", "include", 32, 6)
dep("RWI", "CI", "extend", 0, -4)
dep("ASD", "GWS", "extend", -40, 0)

# generalizations (routed around the system box) to Employee
lines.append('<polyline points="95,720 95,1037 683,1037" fill="none" stroke="#333" stroke-width="1.2" marker-end="url(#tri)"/>')
lines.append('<polyline points="1310,710 1310,1037 727,1037" fill="none" stroke="#333" stroke-width="1.2" marker-end="url(#tri)"/>')
lines.append('<polyline points="1330,205 1395,205 1395,1037 1310,1037" fill="none" stroke="#333" stroke-width="1.2"/>')

out += lines + shapes + ["</svg>"]
import sys
open(sys.argv[1] if len(sys.argv) > 1 else "use-cases.svg", "w").write("\n".join(out))
