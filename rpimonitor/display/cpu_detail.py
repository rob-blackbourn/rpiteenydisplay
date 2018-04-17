"""Draw cpu details"""
from luma.core.render import canvas

def draw_cpu_detail_text(device, font, total, cores):
    """Draw the cpu detail as text"""
    total_text = f"{total:.0%}"
    core0_text = f"{cores[0]:.0%}"
    core1_text = f"{cores[1]:.0%}"
    core2_text = f"{cores[2]:.0%}"
    core3_text = f"{cores[3]:.0%}"

    with canvas(device) as draw:
        max_size = draw.textsize("100%", font=font)
        cpu_size = draw.textsize("CPU", font=font)
        total_size = draw.textsize(total_text, font=font)
        core0_size = draw.textsize(core0_text, font=font)
        core1_size = draw.textsize(core1_text, font=font)
        core2_size = draw.textsize(core2_text, font=font)
        core3_size = draw.textsize(core3_text, font=font)

        cpu_pad = int((max_size[0] - cpu_size[0]) / 2)
        total_pad = max_size[0] - total_size[0]
        core0_pad = max_size[0] - core0_size[0]
        core1_pad = max_size[0] - core1_size[0]
        core2_pad = max_size[0] - core2_size[0]
        core3_pad = max_size[0] - core3_size[0]
        
        x0, x1, x2 = 0, 50, 90
        y0, y1 = 0, 20

        draw.text((x0 + cpu_pad, y0), "CPU", fill="white", font=font)
        draw.text((x0 + total_pad, y1), total_text, fill="white", font=font)
        draw.text((x1 + core0_pad, y0), core0_text, fill="white", font=font)
        draw.text((x1 + core1_pad, y1), core1_text, fill="white", font=font)
        draw.text((x2 + core2_pad, y0), core2_text, fill="white", font=font)
        draw.text((x2 + core3_pad, y1), core3_text, fill="white", font=font)

def calc_and_draw_cpu_detail_text(device, font, prev_cpu, cpu, prev_cores, cores):
    """Calculate and draw the cpu details as text"""
    cpu_delta = (cpu - prev_cpu).usage
    cores_delta = []
    for key in cores.keys():
        cores_delta.append((cores[key] - prev_cores[key]).usage)
    draw_cpu_detail_text(device, font, cpu_delta, cores_delta)

def offset_rectangle(location, rectangle):
    return (location[0] + rectangle[0], location[1] + rectangle[1], location[0] + rectangle[2], location[1] + rectangle[3])

def draw_signal_strength_graph(device, location, value, bar_count=5, unit_size=(2,2)):
    """Draw a signal stregth graph where value varies from 0 to 1"""
    border_thickness = 1
    padding = 1
    total_height = unit_size[1] * bar_count + 2 * border_thickness
    total_width = (unit_size[0] + 2 * border_thickness) * bar_count + (bar_count - 1) * padding
    with canvas(device) as draw:
        for bar in range(bar_count):
            min_bar_value, max_bar_value = bar / bar_count, (bar + 1) / bar_count
            if value >= max_bar_value:
                bar_value = 1
            elif value <= min_bar_value:
                bar_value = 0
            else:
                bar_value = (value - min_bar_value) * bar_count

            total_bar_height = (bar + 1) * unit_size[1] + 2 * border_thickness
            left = bar * (2 * border_thickness + unit_size[0]) + bar * padding
            right = left + 2 * border_thickness + unit_size[0] - 1
            bar_top = total_height - total_bar_height
            bar_rectangle = (left, bar_top, right, total_height)
            if bar_value == 0:
                r = offset_rectangle(location, bar_rectangle)
                draw.rectangle(r, fill='black', outline='white')                
            elif bar_value == 1:
                r = offset_rectangle(location, bar_rectangle)
                draw.rectangle(r, fill='white', outline='white')
            else:
                r = offset_rectangle(location, bar_rectangle)
                draw.rectangle(r, fill='black', outline='white')
                filled_bar_height = int(round(bar_value * (bar + 1) * unit_size[1]))
                filled_top = total_height - (2 * border_thickness + filled_bar_height)
                filled_rectangle = (left, filled_top, right, total_height)
                r = offset_rectangle(location, filled_rectangle)
                draw.rectangle(r, fill='white', outline=None)



