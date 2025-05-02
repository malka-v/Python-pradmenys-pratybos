import sys
import tkinter as tk
from tkinter import ttk
from io import StringIO
import re

# Placeholder exercises
exercises = [
    ("Užduotis 1", "Parašyk kodą, kuris išvestų tavo vardo pirmą raidę sudarytą iš *.\n Nepamiršk nufotografuoti!"),
    ("Užduotis 2", "Parašyk kodą, kuris išvestų šypsenėlę sudarytą iš *.\n Nepamiršk nufotografuoti!"),
    ("Užduotis 3", "Parašyk kodą, kuris suskaičiuotų 5 ir 10 sumą", "15\n"),
    ("Užduotis 4", "Parašyk kodą, kuris apskaičiuotų skaičiaus x kvadratą. x = 5", "25\n"),
    ("Užduotis 5", "Parašyk ciklą, kuris išves skaičius nuo 1 iki 5.", "1\n2\n3\n4\n5\n"),
    ("Užduotis 6",
     "Trikampio statinių ilgiai yra a = 3, b = 4, parašyk kodą, kuris apskaičiuotų trikampio ižambinę (c = √(a^2+b^2)) bei trikampio plotą\n (S = (a*b)/2). \nAtsakymus užrašyk su jų indeksais, pvz.: c = 2, S = 10",
     "c = 5.0\nS = 6.0")
]

current_exercise = 0

def show_intro_window():
    intro_window = tk.Toplevel(root)
    intro_window.title("Python Pagrindai")
    intro_window.geometry("800x500")
    intro_window.configure(bg="#F5F5F5")

    intro_text = """
    Python Pagrindai:

    1. Kintamieji: Python kintamieji aprašomi su indeksu (raide) su vienu lygybės ženklu, pvz: x = 5

    2. Matematiniai veiksmai atliekami su jų simboliais, tačiau norint apskaičiuoti laipsnio kėlimą arba 
    šaknį, reikia naudoti funkciją pow: pow(skaičius, laipsnis), pvz: 3^2 -> pow(3, 2), √4 -> pow(4, 0.5)

    3. Teksto ir kintamųjų išvedimui reikia tekstą rašyti su kabutėmis, o kintamuosius rašyti po kablelio\n     pvz: print('C =', x)

    4. Sąlygos: Sąlygos leidžia vykdyti kodą tik tada, kai sąlyga yra teisinga.
       pvz., 'if x >= 5:', 'if 5 =< x' - jei daugiau/mažiau ARBA lygu, 'if x > 5', 'if x < 5' - jei daugiau ar mažiau
    
    5. Ciklai: Norint išvesti keleta skaičių iškart naudojami while arba for ciklai, while aprašomas su sąlyga\n 
    pvz.: 'while i < 7:'. For ciklas aprašomas diapazonu, pvz.: 'for i in range(7):'.
    
    6. Norint greitai padidinti kintamąjį cikle galima naudoti ženklą +=, pvz: 'i+=1' - prideda 1 prie i. 

    Spauskite "Pradėti", kad pereitumėte prie užduočių!
    """

    intro_label = tk.Label(intro_window, text=intro_text, font=("Arial", 12), bg="#F5F5F5", justify="left", padx=10, pady=10)
    intro_label.pack()

    start_button = ttk.Button(intro_window, text="Pradėti",
                              command=lambda: [intro_window.destroy(), start_main_program()])
    start_button.pack(pady=10)

def load_exercise():
    exercise_label.config(text=exercises[current_exercise][1])
    code_input.delete("1.0", tk.END)
    add_line_numbers()

    # Enable next button for first two exercises
    if current_exercise < 2:
        next_button.config(state=tk.NORMAL)
    else:
        next_button.config(state=tk.DISABLED)

def execute_code():
    code_str = code_input.get("1.0", tk.END).strip()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        exec(code_str, globals())
        output = sys.stdout.getvalue()
        output_text.config(fg="black")
    except Exception as e:
        output = f"Error: {e}"
        output_text.config(fg="red")

    sys.stdout = old_stdout
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)
    output_text.config(state=tk.DISABLED)

def check_answer():
    global current_exercise

    # Skip checking for first two exercises
    if current_exercise < 2:
        feedback_label.config(text="✅ Galite tęsti!", fg="green")
        next_button.config(state=tk.NORMAL)
        return

    code_str = code_input.get("1.0", tk.END).strip()
    expected_output = exercises[current_exercise][2].strip()

    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        local_env = {}
        exec(code_str, {}, local_env)
        output = sys.stdout.getvalue().strip()

        # --- Exercise 4: Loop (1 to 5) ---
        if current_exercise == 4:
            if "for" not in code_str and "while" not in code_str:
                output = "Error: Prašome naudoti ciklą (for/while)."
            else:
                # Normalize output: keep only digits per line
                output_lines = [line.strip() for line in output.splitlines() if line.strip()]
                expected_lines = [str(i) for i in range(1, 6)]

                if output_lines == expected_lines:
                    feedback_label.config(text="✅ Teisingai!", fg="green")
                    next_button.config(state=tk.NORMAL)
                    sys.stdout = old_stdout
                    return
                else:
                    output = "Error: Rezultatai neteisingi. Turėtų būti skaičiai nuo 1 iki 5."

        # --- Exercise 5: Triangle ---
        elif current_exercise == 4:
            c_match = re.search(r"c\s*=\s*([0-9.]+)", output, re.IGNORECASE)
            s_match = re.search(r"s\s*=\s*([0-9.]+)", output, re.IGNORECASE)

            if c_match and s_match:
                c_val = float(c_match.group(1))
                s_val = float(s_match.group(1))
                if abs(c_val - 5.0) < 0.01 and abs(s_val - 6.0) < 0.01:
                    feedback_label.config(text="✅ Teisingai!", fg="green")
                    next_button.config(state=tk.NORMAL)
                    sys.stdout = old_stdout
                    return
                else:
                    output = "Error: Netikslūs atsakymai (c arba S neteisingi)."
            else:
                output = "Error: Nerasta 'c =' arba 'S =' atsakyme."

        # --- All other exercises ---
        else:
            output_clean = " ".join(output.split())
            expected_clean = " ".join(expected_output.split())
            if output_clean == expected_clean:
                feedback_label.config(text="✅ Teisingai!", fg="green")
                next_button.config(state=tk.NORMAL)
                sys.stdout = old_stdout
                return
            else:
                output = "Error: Neteisingas atsakymas."

    except Exception as e:
        output = f"Error: {e}"

    sys.stdout = old_stdout
    feedback_label.config(text="❌ Pabandyk dar kartą!", fg="red")

def next_exercise():
    global current_exercise
    if current_exercise < len(exercises) - 1:
        current_exercise += 1
        load_exercise()
        next_button.config(state=tk.DISABLED)

def add_line_numbers(event=None):
    code_lines.config(state=tk.NORMAL)
    code_lines.delete("1.0", tk.END)
    lines = code_input.get("1.0", tk.END).count("\n") + 1
    code_lines.insert(tk.END, "\n".join(str(i) for i in range(1, lines + 1)))
    code_lines.config(state=tk.DISABLED)

def start_main_program():
    root.deiconify()
    load_exercise()

def auto_indent(event):
    cursor_index = code_input.index(tk.INSERT)
    line_start = f"{cursor_index.split('.')[0]}.0"
    line_text = code_input.get(line_start, cursor_index)

    indent = ""
    for char in line_text:
        if char == " ":
            indent += " "
        else:
            break

    if line_text.strip().endswith(":"):
        indent += "    "  # Add 4 spaces

    code_input.insert(tk.INSERT, f"\n{indent}")
    return "break"

def smart_backspace(event):
    cursor_index = code_input.index(tk.INSERT)
    line_start = f"{cursor_index.split('.')[0]}.0"
    line_text = code_input.get(line_start, cursor_index)

    # If we're at an indentation level, remove 4 spaces
    if line_text.endswith("    "):
        code_input.delete(f"{cursor_index} -4c", cursor_index)
        return "break"  # Prevents normal backspace behavior

root = tk.Tk()
root.title("Python Užduotys")
root.withdraw()
root.resizable(True, True)  # Allow both width and height resizing
root.minsize(800, 600)  # Set minimum window size

exercise_label = tk.Label(root, font=("Arial", 12), wraplength=500, bg="#F5F5F5")
exercise_label.pack(padx=10, pady=5)

frame = tk.Frame(root)
frame.pack()

code_lines = tk.Text(frame, width=4, height=10, font=("Courier", 12), bg="#D3D3D3", state=tk.DISABLED)
code_lines.pack(side=tk.LEFT, fill=tk.Y)

code_input = tk.Text(frame, height=10, width=66, font=("Courier", 12), bg="#EAEAEA")
code_input.pack(side=tk.RIGHT, padx=10, pady=5)
code_input.bind("<KeyRelease>", add_line_numbers)
code_input.bind("<Return>", auto_indent)
code_input.bind("<BackSpace>", smart_backspace)
add_line_numbers()

button_frame = tk.Frame(root, bg="#F5F5F5")
button_frame.pack(pady=5)

run_button = ttk.Button(button_frame, text="Run", command=execute_code)
run_button.pack(side="left", padx=5)

check_button = ttk.Button(button_frame, text="Patikrinti", command=check_answer)
check_button.pack(side="left", padx=5)

next_button = ttk.Button(button_frame, text="→", command=next_exercise, state=tk.DISABLED)
next_button.pack(side="left", padx=5)

# This is the only output_text widget needed - modified to be larger and resizable
output_text = tk.Text(root, height=15, width=80, font=("Courier", 12), bg="#FFF5E1", state=tk.DISABLED)
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

feedback_label = tk.Label(root, text="", font=("Arial", 12), bg="#F5F5F5")
feedback_label.pack(pady=5)

show_intro_window()
root.mainloop()