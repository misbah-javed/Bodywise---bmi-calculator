
import customtkinter as ctk
import tkinter as tk
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BMICalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BodyWise | BMI Calculator")
        self.geometry("720x680")
        self.minsize(650, 620)

        self.configure(fg_color="#101522")

        ctk.CTkLabel(
            self,
            text="BodyWise",
            font=("Helvetica", 30, "bold"),
            text_color="#64DDB2"
        ).pack(pady=(22, 2))

        ctk.CTkLabel(
            self,
            text="YOUR PERSONAL BMI CALCULATOR",
            font=("Helvetica", 11),
            text_color="#9BA8BE"
        ).pack(pady=(0, 18))

        form = ctk.CTkFrame(
            self, fg_color="#1A2233", corner_radius=18
        )
        form.pack(fill="x", padx=35, pady=5)

        self.age = self.add_field(form, "Age (years)", "18", 0)
        self.weight = self.add_field(form, "Weight (kg)", "55", 1)
        self.height = self.add_field(form, "Height (cm)", "165", 2)

        self.sex = ctk.CTkOptionMenu(
            form,
            values=["Female", "Male"],
            height=36,
            fg_color="#29354A",
            button_color="#347D77",
            button_hover_color="#28645F"
        )
        self.sex.grid(row=3, column=1, padx=20, pady=8, sticky="ew")

        ctk.CTkLabel(
            form, text="Sex (for age-based assessment)",
            text_color="#D5DCEC"
        ).grid(row=3, column=0, padx=20, pady=8, sticky="w")

        form.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            self,
            text="Calculate BMI",
            height=44,
            corner_radius=12,
            font=("Helvetica", 15, "bold"),
            fg_color="#36A98D",
            hover_color="#27856F",
            command=self.calculate
        ).pack(fill="x", padx=35, pady=15)

        self.gauge = tk.Canvas(
            self, width=250, height=150,
            bg="#101522", highlightthickness=0
        )
        self.gauge.pack()

        self.result = ctk.CTkLabel(
            self, text="--.--",
            font=("Helvetica", 34, "bold"),
            text_color="#FFFFFF"
        )
        self.result.pack()

        self.category = ctk.CTkLabel(
            self, text="Enter your details to begin",
            font=("Helvetica", 17, "bold"),
            text_color="#64DDB2"
        )
        self.category.pack(pady=5)

        self.note = ctk.CTkLabel(
            self,
            text="BMI is a screening measure, not a diagnosis.",
            font=("Helvetica", 12),
            text_color="#AAB5C8",
            wraplength=600,
            justify="center"
        )
        self.note.pack(padx=30, pady=(2, 18))

        self.draw_gauge(0)

    def add_field(self, parent, label, default, row):
        ctk.CTkLabel(
            parent, text=label, text_color="#D5DCEC"
        ).grid(row=row, column=0, padx=20, pady=8, sticky="w")

        entry = ctk.CTkEntry(
            parent, height=36, placeholder_text=label,
            fg_color="#29354A", border_color="#394861"
        )
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=20, pady=8, sticky="ew")
        return entry

    def draw_gauge(self, bmi):
        self.gauge.delete("all")

        cx, cy, radius = 125, 125, 88
        self.gauge.create_arc(
            cx-radius, cy-radius, cx+radius, cy+radius,
            start=0, extent=180, style="arc",
            outline="#354156", width=15
        )

        if bmi > 0:
            # Display a visual indicator on a 10–40 BMI scale.
            value = max(10, min(40, bmi))
            extent = 180 * (value - 10) / 30
            self.gauge.create_arc(
                cx-radius, cy-radius, cx+radius, cy+radius,
                start=180, extent=-extent, style="arc",
                outline="#64DDB2", width=15
            )

        self.gauge.create_text(
            cx, 24, text="BMI SCALE",
            fill="#AAB5C8", font=("Helvetica", 10)
        )

    def calculate(self):
        try:
            age = float(self.age.get())
            weight = float(self.weight.get())
            height_cm = float(self.height.get())

            if not (0 < age <= 120):
                raise ValueError("Age must be between 1 and 120 years.")
            if weight <= 0 or height_cm <= 0:
                raise ValueError("Weight and height must be positive.")
            if weight > 500 or height_cm > 300:
                raise ValueError("Please check your weight and height.")

            height_m = height_cm / 100
            bmi = weight / (height_m ** 2)

        except ValueError as error:
            self.result.configure(text="--.--")
            self.category.configure(
                text="Please check your entries",
                text_color="#FF8D8D"
            )
            self.note.configure(text=str(error))
            self.draw_gauge(0)
            return

        self.result.configure(text=f"{bmi:.2f}")
        self.draw_gauge(bmi)

        if age >= 20:
            if bmi < 18.5:
                label, color = "Underweight", "#70B7FF"
            elif bmi < 25:
                label, color = "Healthy weight range", "#64DDB2"
            elif bmi < 30:
                label, color = "Overweight range", "#FFD166"
            else:
                label, color = "Obesity range", "#FF8D8D"

            self.category.configure(text=label, text_color=color)
            self.note.configure(
                text="Adult BMI screening categories. "
                     "BMI alone cannot determine your health."
            )
        elif age >= 2:
            self.category.configure(
                text="Child/teen BMI assessment needed",
                text_color="#FFD166"
            )
            self.note.configure(
                text=f"BMI: {bmi:.2f} kg/m². For ages 2–19, "
                     "interpretation depends on age and sex-specific "
                     "BMI percentiles. This offline version does not "
                     "estimate those percentiles."
            )
        else:
            self.category.configure(
                text="Infant growth assessment needed",
                text_color="#FFD166"
            )
            self.note.configure(
                text="BMI is not interpreted using these categories "
                     "for children under 2. Consult a pediatric "
                     "health professional for growth assessment."
            )


if __name__ == "__main__":
    app = BMICalculator()
    app.mainloop()
