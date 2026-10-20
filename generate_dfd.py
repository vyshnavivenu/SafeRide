import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse
import math

fig, ax = plt.subplots(figsize=(12, 7.2), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 7.2)
ax.axis('off')

# Styling: Formal Black and White DFD Context Diagram
line_color = '#000000'
box_fill = '#FFFFFF'
plt.rcParams['font.sans-serif'] = 'Arial'

# 1. Central System Oval
cx, cy = 6.0, 4.5
ew, eh = 4.6, 2.7
center_ellipse = Ellipse(
    (cx, cy), ew, eh,
    facecolor=box_fill, edgecolor=line_color, linewidth=2.2, zorder=2
)
ax.add_patch(center_ellipse)

ax.text(
    cx, cy,
    "SafeRide:\nDriver Verification and\nPassenger Safety System",
    ha='center', va='center',
    fontsize=12.5, fontweight='bold', color=line_color,
    linespacing=1.35, zorder=3
)

# 2. External Entities (Rectangles with slight corner rounding for professional finish)
def draw_entity(x, y, w, h, label):
    box = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.03,rounding_size=0.06",
        facecolor=box_fill, edgecolor=line_color, linewidth=2.2, zorder=2
    )
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center', fontsize=16, fontweight='bold', color=line_color, zorder=3)

# Passenger (Left)
px, py, pw, ph = 1.4, 4.5, 2.2, 1.45
draw_entity(px, py, pw, ph, "Passenger")

# Admin (Right)
ax_pos, ay, aw, ah = 10.6, 4.5, 2.2, 1.45
draw_entity(ax_pos, ay, aw, ah, "Admin")

# Driver (Bottom)
dx, dy, dw, dh = 6.0, 1.15, 2.4, 1.35
draw_entity(dx, dy, dw, dh, "Driver")

# Function to get boundary of ellipse for straight horizontal arrows
def get_ellipse_x(y, is_left=True):
    dy_val = y - cy
    val = 1 - (dy_val / (eh / 2))**2
    if val <= 0:
        return cx
    dx_val = (ew / 2) * math.sqrt(val)
    return (cx - dx_val) if is_left else (cx + dx_val)

# Arrow helper
def draw_arrow(start, end, label, label_pos='above', offset=0.15, rotation=0):
    ax.annotate(
        '', xy=end, xytext=start,
        arrowprops=dict(
            arrowstyle="-|>",
            color=line_color,
            lw=2.0,
            mutation_scale=16
        ),
        zorder=2
    )
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    
    if label_pos == 'above':
        ax.text(mid_x, mid_y + offset, label, ha='center', va='bottom', fontsize=11.5, fontweight='bold', color=line_color)
    elif label_pos == 'below':
        ax.text(mid_x, mid_y - offset, label, ha='center', va='top', fontsize=11.5, fontweight='bold', color=line_color)
    elif label_pos == 'left':
        ax.text(mid_x - offset, mid_y, label, ha='right', va='center', rotation=rotation, fontsize=11.5, fontweight='bold', color=line_color)
    elif label_pos == 'right':
        ax.text(mid_x + offset, mid_y, label, ha='left', va='center', rotation=rotation, fontsize=11.5, fontweight='bold', color=line_color)

# 3. Passenger <-> Central Oval
p_right = px + pw/2  # 2.5
y_top = 4.88
y_bot = 4.12
x_el_top = get_ellipse_x(y_top, is_left=True)
x_el_bot = get_ellipse_x(y_bot, is_left=True)

# Passenger -> System: Request
draw_arrow((p_right, y_top), (x_el_top, y_top), "Request", label_pos='above', offset=0.14)
# System -> Passenger: Response
draw_arrow((x_el_bot, y_bot), (p_right, y_bot), "Response", label_pos='below', offset=0.14)

# 4. Admin <-> Central Oval
# User requirement: "For Admin, the Request arrow must point towards the system and the Response arrow away from it."
a_left = ax_pos - aw/2  # 9.5
x_er_top = get_ellipse_x(y_top, is_left=False)
x_er_bot = get_ellipse_x(y_bot, is_left=False)

# Admin -> System: Request (pointing towards system)
draw_arrow((a_left, y_top), (x_er_top, y_top), "Request", label_pos='above', offset=0.14)
# System -> Admin: Response (pointing away from system)
draw_arrow((x_er_bot, y_bot), (a_left, y_bot), "Response", label_pos='below', offset=0.14)

# 5. Driver <-> Central Oval
# User requirement: "For Driver, the Request arrow must point towards the system and the Response arrow away from it."
d_top = dy + dh/2  # 1.825

def get_ellipse_bottom_y(x):
    dx_val = x - cx
    val = 1 - (dx_val / (ew / 2))**2
    if val <= 0:
        return cy
    dy_val = (eh / 2) * math.sqrt(val)
    return cy - dy_val

x_left = 5.65
x_right = 6.35
y_eb_left = get_ellipse_bottom_y(x_left)
y_eb_right = get_ellipse_bottom_y(x_right)

# Driver -> System: Request (pointing towards system, upwards)
draw_arrow((x_left, d_top), (x_left, y_eb_left), "Request", label_pos='left', offset=0.15, rotation=90)
# System -> Driver: Response (pointing away from system, downwards)
draw_arrow((x_right, y_eb_right), (x_right, d_top), "Response", label_pos='right', offset=0.15, rotation=90)

plt.tight_layout()

# Save final clean PNG and SVG
png_output = "saferide_context_diagram.png"
svg_output = "saferide_context_diagram.svg"
plt.savefig(png_output, bbox_inches='tight', dpi=300, facecolor='white')
plt.savefig(svg_output, bbox_inches='tight', facecolor='white')
print(f"Successfully generated clean DFD Context Diagram: {png_output}")
