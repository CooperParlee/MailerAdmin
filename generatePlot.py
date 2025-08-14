import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
import io
import base64

def generatePlot(name, axes_labels, data, color_line, color_grad):
    x = data[0]
    y = data[1]

    # Generate Standard Plot
    fig, ax = plt.subplots(figsize=(6,4))
    
    plt.title(name)
    plt.xlabel(axes_labels[0])
    plt.ylabel(axes_labels[1])

    base_date = "2025-01-01"
    date_obj = [datetime.strptime(f"{base_date} {t}", '%Y-%m-%d %H:%M') for t in x]
    x_dates = mdates.date2num(date_obj)
    #Generate Gradient Underneath
    
    gradient = np.linspace(1, 0, 256).reshape(-1, 1)
    ax.imshow(gradient, 
              extent=[x_dates[0], x_dates[-1], 0, max(y)],
              origin='upper',
              aspect='auto',
              cmap=cm.get_cmap(color_grad),
              alpha=0.7)
    
    ax.fill_between(date_obj, y, max(y), color='white')

    ax.plot(date_obj, y, color=color_line, linewidth=2)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()

    if len(data) > 2:
        y2 = data[2]
        ax.plot(date_obj, y2, color=color_line)

    return fig

def generateBase64 (fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    img_64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close(fig)

    return img_64
