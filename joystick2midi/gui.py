import customtkinter as ctk

class JoystickToMidiGUI:
    def __init__(self, root, cc_presets, callback_cc_cambiado):
        self.root = root
        self.cc_presets = cc_presets
        self.callback_cc_cambiado = callback_cc_cambiado

        self.cc_izq = 4
        self.cc_der = 1

        self.modo_izq_var = ctk.StringVar(value="boton")
        self.modo_der_var = ctk.StringVar(value="expresion")

        self.setup_ui()

    def setup_ui(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.title("Joystick To Midi")
        self.root.geometry("700x550")

        modo_label_font = ("Arial", 14, "bold")

        ctk.CTkLabel(self.root, text="Joystick To Midi", font=("Arial", 28, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(self.root, text="PEDALES", font=modo_label_font).pack(pady=(0, 10))

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Izquierda
        frame_izq = ctk.CTkFrame(main_frame, width=250, height=300)
        frame_izq.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        frame_izq.pack_propagate(False)

        ctk.CTkLabel(frame_izq, text="IZQUIERDA", font=modo_label_font).pack(pady=(10, 5))

        modo_frame_izq = ctk.CTkFrame(frame_izq, fg_color="transparent")
        modo_frame_izq.pack(pady=5)

        ctk.CTkRadioButton(modo_frame_izq, text="Botón", variable=self.modo_izq_var,
                           value="boton", command=self.actualizar_estilos).pack(side="left", padx=5)
        ctk.CTkRadioButton(modo_frame_izq, text="Pedal", variable=self.modo_izq_var,
                           value="expresion", command=self.actualizar_estilos).pack(side="left", padx=5)

        self.lbl_estado_izq = ctk.CTkLabel(frame_izq, text="", font=("Arial", 12))
        self.lbl_estado_izq.pack(pady=(5, 0))

        self.cc_frame_izq = ctk.CTkFrame(frame_izq)
        for nombre, valor in self.cc_presets.items():
            ctk.CTkButton(self.cc_frame_izq, text=nombre, width=150,
                          command=lambda v=valor: self.set_cc("izq", v)).pack(pady=2)

        # Derecha
        frame_der = ctk.CTkFrame(main_frame, width=250, height=300)
        frame_der.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        frame_der.pack_propagate(False)

        ctk.CTkLabel(frame_der, text="DERECHA", font=modo_label_font).pack(pady=(10, 5))

        modo_frame_der = ctk.CTkFrame(frame_der, fg_color="transparent")
        modo_frame_der.pack(pady=5)

        ctk.CTkRadioButton(modo_frame_der, text="Botón", variable=self.modo_der_var,
                           value="boton", command=self.actualizar_estilos).pack(side="left", padx=5)
        ctk.CTkRadioButton(modo_frame_der, text="Pedal", variable=self.modo_der_var,
                           value="expresion", command=self.actualizar_estilos).pack(side="left", padx=5)

        self.lbl_estado_der = ctk.CTkLabel(frame_der, text="", font=("Arial", 12))
        self.lbl_estado_der.pack(pady=(5, 0))

        self.cc_frame_der = ctk.CTkFrame(frame_der)
        for nombre, valor in self.cc_presets.items():
            v_real = valor if nombre != "Midi" else 1
            ctk.CTkButton(self.cc_frame_der, text=nombre, width=150,
                          command=lambda v=v_real: self.set_cc("der", v)).pack(pady=2)

        # Resumen
        self.resumen_label = ctk.CTkLabel(self.root, text="", font=("Arial", 12, "italic"))
        self.resumen_label.pack(pady=(10, 15))

        self.actualizar_estilos()

    def set_cc(self, lado, valor):
        if lado == "izq":
            self.cc_izq = valor
        else:
            self.cc_der = valor
        self.actualizar_estilos()
        self.callback_cc_cambiado(lado, valor)

    def actualizar_estilos(self):
        if self.modo_izq_var.get() == "boton":
            self.cc_frame_izq.pack_forget()
        else:
            self.cc_frame_izq.pack(pady=5)

        if self.modo_der_var.get() == "boton":
            self.cc_frame_der.pack_forget()
        else:
            self.cc_frame_der.pack(pady=5)

        self.lbl_estado_izq.configure(
            text=f"Modo: {'Pedal' if self.modo_izq_var.get() == 'expresion' else 'Botón'}"
                 + (f" | CC: {self.cc_izq}" if self.modo_izq_var.get() == "expresion" else "")
        )
        self.lbl_estado_der.configure(
            text=f"Modo: {'Pedal' if self.modo_der_var.get() == 'expresion' else 'Botón'}"
                 + (f" | CC: {self.cc_der}" if self.modo_der_var.get() == "expresion" else "")
        )

        resumen_texto = (
            f"Lado Izquierdo: {self.modo_izq_var.get().capitalize()}"
            + (f" (CC {self.cc_izq})" if self.modo_izq_var.get() == "expresion" else "") + "   |   "
            f"Lado Derecho: {self.modo_der_var.get().capitalize()}"
            + (f" (CC {self.cc_der})" if self.modo_der_var.get() == "expresion" else "")
        )
        self.resumen_label.configure(text=resumen_texto)
