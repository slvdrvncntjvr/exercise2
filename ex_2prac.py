import tkinter as tk
from tkinter import ttk, messagebox

RATES = {
    "Residential": {"price": 15.00, "Metro Manila Area": 0.03, "Provincial Area": 0.02},
    "Commercial": {"price": 30.00, "Metro Manila Area": 0.06, "Provincial Area": 0.04},
    "Industrial": {"price": 45.00, "Metro Manila Area": 0.09, "Provincial Area": 0.06},
}

root = tk.Tk()
root.title("Electric Bill Calculator")
root.resizable(False, False)

area_var = tk.StringVar(value="Default")
acct_num = tk.StringVar()
cust_name = tk.StringVar()
prev_read = tk.StringVar()
curr_read = tk.StringVar()
kwh_used = tk.StringVar()
acct_type = tk.StringVar(value=" ")
elec_bill = tk.StringVar()
sys_charges = tk.StringVar()
total_bill = tk.StringVar()

pad = {"padx": 8, "pady": 4}

area_frame = tk.LabelFrame(root, text="Area", padx=6, pady=4)
area_frame.grid(row=0, column=0, columnspan=2, sticky="ew", **pad)

tk.Radiobutton(area_frame, text="Default", variable=area_var, value="Default", state="disabled").pack(side="left", padx=6)
tk.Radiobutton(area_frame, text="Metro Manila Area", variable=area_var, value="Metro Manila Area").pack(side="left", padx=6)
tk.Radiobutton(area_frame, text="Provincial Area", variable=area_var, value="Provincial Area").pack(side="left", padx=6)

def add_row(label, var, row, readonly=False):
    tk.Label(root, text=label, anchor="e", width=18).grid(row=row, column=0, **pad, sticky="e")
    if readonly:
        state = "readonly"
    else:
        state = "normal"
    e = tk.Entry(root, textvariable=var, state=state, width=30)
    e.grid(row=row, column=1, **pad, sticky="w")
    return e

add_row("Account Number:", acct_num, row=1)
add_row("Customer Name:", cust_name, row=2)
add_row("Previous Reading:", prev_read, row=3)
add_row("Current Reading:", curr_read, row=4)
add_row("KwH Used:", kwh_used, row=5, readonly=True)

tk.Label(root, text="Account Type:", anchor="e", width=18).grid(row=6, column=0, **pad, sticky="e")
combo = ttk.Combobox(root, textvariable=acct_type,
                     values=["Residential", "Commercial", "Industrial"],
                     state="readonly", width=28)
combo.grid(row=6, column=1, **pad, sticky="w")
combo.set(" ")

add_row("Electric Bill:", elec_bill, row=7, readonly=True)
add_row("System Charges:", sys_charges, row=8, readonly=True)
add_row("Total Bill:", total_bill, row=9, readonly=True)

def clear():
    area_var.set("Default")
    acct_num.set("")
    cust_name.set("")
    prev_read.set("")
    curr_read.set("")
    kwh_used.set("")
    acct_type.set(" ")
    combo.set(" ")
    elec_bill.set("")
    sys_charges.set("")
    total_bill.set("")

def compute():
    if area_var.get() == "Default":
        messagebox.showerror("Error", "Please select an Area (Metro Manila or Provincial).")
        return

    if acct_type.get().strip() == "":
        messagebox.showerror("Error", "Please select a valid Account Type.")
        return

    try:
        prev = int(prev_read.get())
        curr = int(curr_read.get())
        if prev <= 0 or curr <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Previous Reading and Current Reading must be positive integers.")
        return

    if curr <= prev:
        messagebox.showerror("Incorrect Reading", "Current Reading must be greater than Previous Reading.")
        curr_read.set("")
        return

    area = area_var.get()
    atype = acct_type.get().strip()
    rate = RATES[atype]

    kwh = curr - prev
    ebill = kwh * rate["price"]
    schg = ebill * rate[area]
    total = ebill + schg

    kwh_used.set(str(kwh))
    elec_bill.set(f"{ebill:.2f}")
    sys_charges.set(f"{schg:.2f}")
    total_bill.set(f"{total:.2f}")

btn_frame = tk.Frame(root)
btn_frame.grid(row=10, column=0, columnspan=2, pady=10)

tk.Button(btn_frame, text="CCOMPUTE", width=14, command=compute).pack(side="left", padx=10)
tk.Button(btn_frame, text="CLEAR", width=14, command=clear).pack(side="left", padx=10)

root.mainloop()