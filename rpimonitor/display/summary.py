"""Draw summary"""

from luma.core.render import canvas

def draw_summary_text(device, font, cpu_usage, mem_usage, cpu_temp):
    """Draw the summary as text"""
    cpu_usage_text = f"{cpu_usage:.0%}"
    mem_usage_text = f"{mem_usage:.0%}"
    cpu_temp_text = f"{cpu_temp:.0f}\u2103"

    with canvas(device) as draw:
        hundred_pct_width = draw.textsize("100%", font=font)[0]
        hundred_degc_width = draw.textsize("100\u2103", font=font)[0]
        cpu_title_width = draw.textsize("CPU", font=font)[0]
        mem_title_width = draw.textsize("Mem", font=font)[0]
        temp_title_width = draw.textsize("Temp", font=font)[0]

        cpu_width = max(cpu_title_width, hundred_pct_width)
        mem_width = max(mem_title_width, hundred_pct_width)
        temp_width = max(temp_title_width, hundred_degc_width)

        cpu_usage_width = draw.textsize(cpu_usage_text, font=font)[0]
        mem_usage_width = draw.textsize(mem_usage_text, font=font)[0]
        cpu_temp_width = draw.textsize(cpu_temp_text, font=font)[0]

        cpu_title_pad = cpu_width - cpu_title_width
        cpu_usage_pad = cpu_width - cpu_usage_width
        mem_title_pad = mem_width - mem_title_width
        mem_usage_pad = mem_width - mem_usage_width
        temp_title_pad = temp_width - temp_title_width
        cpu_temp_pad = temp_width - cpu_temp_width
        
        x0, x1, x2 = 0, 45, 90
        y0, y1 = 0, 20

        draw.text((x0 + cpu_title_pad, y0), "CPU", fill="white", font=font)
        draw.text((x0 + cpu_usage_pad, y1), cpu_usage_text, fill="white", font=font)
        draw.text((x1 + mem_title_pad, y0), "Mem", fill="white", font=font)
        draw.text((x1 + mem_usage_pad, y1), mem_usage_text, fill="white", font=font)
        draw.text((x2 + temp_title_pad, y0), "Temp", fill="white", font=font)
        draw.text((x2 + cpu_temp_pad, y1), cpu_temp_text, fill="white", font=font)
