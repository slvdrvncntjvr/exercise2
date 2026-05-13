import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

RATE_PER_HOUR = {
    "Rank 1": 100,
    "Rank 2": 200,
    "Rank 3": 300,
}

script_dir = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.title("Employee Payroll Calculator")
root.resizable(False, False)

name = tk.StringVar()
hours = tk.StringVar()
rank = tk.StringVar(value=" ")
gross = tk.StringVar()
deductions = tk.StringVar()
net = tk.StringVar()
loan = tk.StringVar(value="Without Loan")

gsis = tk.BooleanVar()
philhealth = tk.BooleanVar()
wtax = tk.BooleanVar()
pagibig = tk.BooleanVar()

pad = {"padx": 8, "pady": 4}

def add_row(label, var, row, readonly=False):
    tk.Label(root, text=label, anchor="e", width=20).grid(row=row, column=0, **pad, sticky="e")
    if readonly:
        state = "readonly"
    else:
        state = "normal"
    e = tk.Entry(root, textvariable=var, state=state, width=30)
    e.grid(row=row, column=1, **pad, sticky="w")
    return e

add_row("Employee Name:", name, row=0)
add_row("No. of Hours Worked:", hours, row=1)

tk.Label(root, text="Employee Rank:", anchor="e", width=20).grid(row=2, column=0, **pad, sticky="e")
rank_combo = ttk.Combobox(root, textvariable=rank,
                          values=["Rank 1", "Rank 2", "Rank 3"],
                          state="readonly", width=28)
rank_combo.grid(row=2, column=1, **pad, sticky="w")
rank_combo.set(" ")

add_row("Gross Salary:", gross, row=3, readonly=True)

# deductions
ded_frame = tk.LabelFrame(root, text="Deductions", padx=6, pady=4)
ded_frame.grid(row=4, column=0, columnspan=2, sticky="ew", **pad)

tk.Checkbutton(ded_frame, text="GSIS Contribution  P1000", variable=gsis).grid(row=0, column=0, sticky="w", padx=10)
tk.Checkbutton(ded_frame, text="PHILHEALTH  P200", variable=philhealth).grid(row=0, column=1, sticky="w", padx=10)
tk.Checkbutton(ded_frame, text="Withholding Tax  10%", variable=wtax).grid(row=1, column=0, sticky="w", padx=10)
tk.Checkbutton(ded_frame, text="PAG-IBIG  P300", variable=pagibig).grid(row=1, column=1, sticky="w", padx=10)

add_row("Total Deductions:", deductions, row=5, readonly=True)

# loan
loan_frame = tk.LabelFrame(root, text="Loan Details", padx=6, pady=4)
loan_frame.grid(row=6, column=0, columnspan=2, sticky="ew", **pad)

tk.Radiobutton(loan_frame, text="Without Loan", variable=loan, value="Without Loan").pack(side="left", padx=10)
tk.Radiobutton(loan_frame, text="With Loan", variable=loan, value="With Loan").pack(side="left", padx=10)

add_row("Net Pay:", net, row=7, readonly=True)

# load images
eat_img = Image.open(os.path.join(script_dir, "eat.jpg")).resize((200, 200))
tong_img = Image.open(os.path.join(script_dir, "tong.jpg")).resize((300, 200))

def show_spinning_loader(callback):
    overlay = tk.Toplevel(root)
    overlay.title("Computing...")
    overlay.resizable(False, False)
    overlay.grab_set()

    canvas = tk.Canvas(overlay, width=220, height=240)
    canvas.pack()

    angle = [0]
    photo = [None]

    def spin():
        rotated = eat_img.rotate(angle[0], resample=Image.BICUBIC, expand=False)
        photo[0] = ImageTk.PhotoImage(rotated)
        canvas.delete("all")
        canvas.create_image(110, 110, image=photo[0])
        canvas.create_text(110, 225, text="Computing...", font=("Arial", 10))
        angle[0] = (angle[0] - 15) % 360
        if angle[0] != 0 and hasattr(overlay, "spinning"):
            overlay.after(30, spin)
        else:
            overlay.destroy()
            callback()

    overlay.spinning = True
    # spin for about 1.5 seconds (360 degrees at 15 deg per 30ms)
    overlay.after(1500, lambda: delattr(overlay, "spinning"))
    spin()

def show_clear_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Are you sure?")
    dialog.resizable(False, False)
    dialog.grab_set()

    tong_photo = ImageTk.PhotoImage(tong_img)
    dialog.tong_photo = tong_photo

    tk.Label(dialog, text="Are you sure?", font=("Arial", 12, "bold")).pack(pady=(10, 5))

    img_frame = tk.Frame(dialog)
    img_frame.pack(pady=5)

    # no on the left side, image in center, yes on the right (mouth/tongue side)
    tk.Button(img_frame, text="No", width=6, font=("Arial", 10),
              command=dialog.destroy).grid(row=0, column=0, padx=10, pady=10)
    tk.Label(img_frame, image=tong_photo).grid(row=0, column=1)
    tk.Button(img_frame, text="Yes", width=6, font=("Arial", 10),
              command=lambda: [do_clear(), dialog.destroy()]).grid(row=0, column=2, padx=10, pady=10)

def do_clear():
    name.set("")
    hours.set("")
    rank.set(" ")
    rank_combo.set(" ")
    gross.set("")
    deductions.set("")
    net.set("")
    loan.set("Without Loan")
    gsis.set(False)
    philhealth.set(False)
    wtax.set(False)
    pagibig.set(False)

def clear():
    show_clear_dialog()

def compute():
    try:
        hrs = int(hours.get())
        if hrs <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "No. of Hours Worked must be a positive integer.")
        return

    if rank.get().strip() == "":
        messagebox.showerror("Error", "Please select a valid Employee Rank.")
        return

    def show_results():
        rate = RATE_PER_HOUR[rank.get()]
        gross_val = hrs * rate

        ded = 0
        if gsis.get():
            ded += 1000
        if philhealth.get():
            ded += 200
        if wtax.get():
            ded += gross_val * 0.10
        if pagibig.get():
            ded += 300

        net_val = gross_val - ded
        if loan.get() == "With Loan":
            net_val = net_val / 2

        gross.set(f"{gross_val:.2f}")
        deductions.set(f"{ded:.2f}")
        net.set(f"{net_val:.2f}")

    show_spinning_loader(show_results)

btn_frame = tk.Frame(root)
btn_frame.grid(row=8, column=0, columnspan=2, pady=10)

tk.Button(btn_frame, text="btn-COMPUTE", width=14, command=compute).pack(side="left", padx=10)
tk.Button(btn_frame, text="btn-CLEAR", width=14, command=clear).pack(side="left", padx=10)

root.mainloop()