from tkinter import Toplevel, Label
import tkinter as tk

def hoverTextWidgetEvent(eventTarget, widgetText, widgetBG, widgetTextFG, widgetFont, widgetFontsize, widgetTextJustify, widgetBorderWidth, widgetBorderColor):

    # Event assignment
    def runEvent(): 
        def on_enter(event):
            x = event.widget.winfo_pointerx()
            y = event.widget.winfo_pointery()
            create_tooltip(x, y)

        def on_leave(event):
            destroy_tooltip()

        def create_tooltip(x, y):
            global tooltip
            tooltip = Toplevel(eventTarget)
            tooltip.geometry('+{}+{}'.format(x, y))
            tooltip.wm_attributes('-topmost', True)
            tooltip.wm_attributes('-disabled', True) #IMPORTANT : This make program not regconize the tooltip as a window
            tooltip.overrideredirect(True)
            tooltip.configure(bg=widgetBorderColor, borderwidth=1)
            label = Label(tooltip, text=widgetText, justify=widgetTextJustify, bg=widgetBG, fg=widgetTextFG, font=(widgetFont, int(widgetFontsize)),borderwidth=widgetBorderWidth)
            label.pack(anchor='center')
            tooltip.attributes("-alpha", 0.0)
            fade_in(tooltip)

        def destroy_tooltip():
            global tooltip
            fade_out(tooltip)

        def fade_in(widget):
            alpha = widget.attributes("-alpha")
            if alpha < 1:
                alpha += 0.1
                widget.attributes("-alpha", alpha)
                widget.after(10, fade_in, widget)

        def fade_out(widget):
            alpha = widget.attributes("-alpha")
            if alpha > 0:
                alpha -= 0.1
                widget.attributes("-alpha", alpha)
                widget.after(10, fade_out, widget)
                widget.after(100, lambda: widget.destroy())
    
        eventTarget.bind('<Enter>', on_enter)
        eventTarget.bind('<Leave>', on_leave)
    
    # Event execution
    if type(eventTarget) == list:
        for eventTarget in eventTarget:
            runEvent()
    else:
        runEvent()
