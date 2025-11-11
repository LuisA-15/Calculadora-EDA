import tkinter as tk
from tkinter import ttk, messagebox
from core.microkernel import Microkernel
from core.event_bus import EventBus


bus = EventBus()
mk = Microkernel(bus)
mk.discover_and_load()

root = tk.Tk()
root.title("Event-Driven Calculator")
root.geometry("420x260")

frm = ttk.Frame(root, padding=12)
frm.pack(fill=tk.BOTH, expand=True)

ops = mk.available()
spec = {name: mk._registry[name].arity() for name in ops}
op_var = tk.StringVar(value=ops[0] if ops else "")
result_var = tk.StringVar()

inputs_frame = ttk.Frame(frm)
entries = []


def render_inputs(*_):
    for w in entries:
        w.destroy()
    entries.clear()
    arity = spec.get(op_var.get(), 2)
    for i in range(arity):
        e = ttk.Entry(inputs_frame)
        e.grid(row=0, column=i, padx=4, sticky=tk.EW)
        inputs_frame.columnconfigure(i, weight=1)
        entries.append(e)


def on_calc():
    try:
        nums = [float(e.get()) for e in entries]
        bus.publish("calculate", {"operator": op_var.get(), "args": nums})
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Subscribe to events from kernel
bus.subscribe("result", lambda d: result_var.set(f"Resultado: {d['result']}"))
bus.subscribe("error", lambda d: messagebox.showerror("Error", d["message"]))


# Layout
ttk.Label(frm, text="Operación").grid(row=0, column=0, sticky=tk.W)
op_menu = ttk.Combobox(frm, textvariable=op_var, values=ops, state="readonly")
op_menu.grid(row=0, column=1, sticky=tk.EW)
inputs_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=8)
calc_btn = ttk.Button(frm, text="Calcular", command=on_calc)
calc_btn.grid(row=2, column=0, pady=8, sticky=tk.W)
res_lbl = ttk.Label(frm, textvariable=result_var, foreground="#1a5e1a")
res_lbl.grid(row=2, column=1, sticky=tk.E)

op_menu.bind("<<ComboboxSelected>>", render_inputs)
render_inputs()

root.mainloop()
