"""A small collection of validated math utilities in one desktop app."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, ttk

from operations import (
    apply_percentage,
    binary_to_decimal,
    decimal_to_binary,
    finite_average,
    imaginary_power,
    simplify_square_root,
)


class MathToolkitApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Math Utility Toolkit")
        self.root.geometry("720x500")
        self.root.minsize(620, 440)
        self.values: list[float] = []

        container = ttk.Frame(root, padding=16)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="Math Utility Toolkit", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(container, text="Small exercises consolidated into one tested application.").pack(anchor="w", pady=(0, 14))

        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)
        self._converter_tab(notebook)
        self._root_tab(notebook)
        self._average_tab(notebook)
        self._imaginary_tab(notebook)
        self._percentage_tab(notebook)

    def _tab(self, notebook: ttk.Notebook, title: str) -> ttk.Frame:
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text=title)
        frame.columnconfigure(1, weight=1)
        return frame

    def _result(self, frame: ttk.Frame, row: int) -> tk.StringVar:
        variable = tk.StringVar(value="Result will appear here.")
        ttk.Label(frame, textvariable=variable, font=("Segoe UI", 14, "bold"), wraplength=540).grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=(18, 0)
        )
        return variable

    def _converter_tab(self, notebook: ttk.Notebook) -> None:
        frame = self._tab(notebook, "Base converter")
        ttk.Label(frame, text="Value").grid(row=0, column=0, sticky="w", pady=6)
        entry = ttk.Entry(frame)
        entry.grid(row=0, column=1, sticky="ew", padx=8, pady=6)
        mode = tk.StringVar(value="decimal")
        ttk.Radiobutton(frame, text="Decimal → binary", variable=mode, value="decimal").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(frame, text="Binary → decimal", variable=mode, value="binary").grid(row=2, column=1, sticky="w")
        result = self._result(frame, 4)

        def convert() -> None:
            try:
                if mode.get() == "decimal":
                    result.set(decimal_to_binary(int(entry.get().strip())))
                else:
                    result.set(str(binary_to_decimal(entry.get())))
            except (TypeError, ValueError) as exc:
                result.set(f"Error: {exc}")

        ttk.Button(frame, text="Convert", command=convert).grid(row=3, column=1, sticky="w", pady=10)

    def _root_tab(self, notebook: ttk.Notebook) -> None:
        frame = self._tab(notebook, "Square root")
        ttk.Label(frame, text="Non-negative integer").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(frame)
        entry.grid(row=0, column=1, sticky="ew", padx=8)
        result = self._result(frame, 2)

        def calculate() -> None:
            try:
                number = int(entry.get().strip())
                simplified = simplify_square_root(number)
                result.set(f"√{number} = {simplified}")
            except (TypeError, ValueError) as exc:
                result.set(f"Error: {exc}")

        ttk.Button(frame, text="Simplify", command=calculate).grid(row=1, column=1, sticky="w", pady=10)

    def _average_tab(self, notebook: ttk.Notebook) -> None:
        frame = self._tab(notebook, "Average")
        entry = ttk.Entry(frame)
        entry.grid(row=0, column=0, columnspan=2, sticky="ew")
        values_var = tk.StringVar(value="No values added.")
        ttk.Label(frame, textvariable=values_var, wraplength=540).grid(row=2, column=0, columnspan=3, sticky="w", pady=12)
        result = self._result(frame, 4)

        def refresh() -> None:
            values_var.set(", ".join(f"{value:g}" for value in self.values) if self.values else "No values added.")

        def add() -> None:
            try:
                value = float(entry.get().strip())
                if not math.isfinite(value):
                    raise ValueError("number must be finite")
                self.values.append(value)
                entry.delete(0, "end")
                refresh()
                result.set(f"Added {value:g}.")
            except ValueError as exc:
                result.set(f"Error: {exc}")

        def remove_last() -> None:
            if self.values:
                self.values.pop()
            refresh()

        def calculate() -> None:
            try:
                result.set(f"Average: {finite_average(self.values):g}")
            except ValueError as exc:
                result.set(f"Error: {exc}")

        buttons = ttk.Frame(frame)
        buttons.grid(row=1, column=0, columnspan=3, sticky="w", pady=8)
        ttk.Button(buttons, text="Add", command=add).pack(side="left")
        ttk.Button(buttons, text="Remove last", command=remove_last).pack(side="left", padx=6)
        ttk.Button(buttons, text="Clear", command=lambda: (self.values.clear(), refresh())).pack(side="left")
        ttk.Button(frame, text="Calculate average", command=calculate).grid(row=3, column=0, sticky="w")

    def _imaginary_tab(self, notebook: ttk.Notebook) -> None:
        frame = self._tab(notebook, "Powers of i")
        ttk.Label(frame, text="Integer exponent").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(frame)
        entry.grid(row=0, column=1, sticky="ew", padx=8)
        result = self._result(frame, 2)

        def calculate() -> None:
            try:
                exponent = int(entry.get().strip())
                result.set(f"i^{exponent} = {imaginary_power(exponent)}")
            except ValueError:
                result.set("Error: exponent must be an integer")

        ttk.Button(frame, text="Calculate", command=calculate).grid(row=1, column=1, sticky="w", pady=10)

    def _percentage_tab(self, notebook: ttk.Notebook) -> None:
        frame = self._tab(notebook, "Percentage")
        ttk.Label(frame, text="Base amount").grid(row=0, column=0, sticky="w", pady=6)
        base = ttk.Entry(frame)
        base.grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Label(frame, text="Percentage to add").grid(row=1, column=0, sticky="w", pady=6)
        percentage = ttk.Entry(frame)
        percentage.grid(row=1, column=1, sticky="ew", padx=8)
        result = self._result(frame, 3)

        def calculate() -> None:
            try:
                final = apply_percentage(float(base.get()), float(percentage.get()))
                result.set(f"Final amount: {final:,.2f}")
            except ValueError as exc:
                result.set(f"Error: {exc}")

        ttk.Button(frame, text="Calculate", command=calculate).grid(row=2, column=1, sticky="w", pady=10)


def main() -> None:
    root = tk.Tk()
    MathToolkitApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
