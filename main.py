import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()

janela.title("Tesk Guardian")
janela.geometry("900x600")

titulo = ctk.CTkLabel(
	janela,
	text="Tesk Guardian",
	font=("Arial", 28, "bold")
)

titulo.pack(pady=20)

status = ctk.CTkLabel(
	janela,
	text="Monitoramento de desempenho",
	font=("Arial", 16)
)

status.pack()

janela.mainloop()
