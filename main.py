import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()

janela.title("TaskGuardian")
janela.geometry("1400x900")
janela.minsize(1200,700)

titulo = ctk.CTkLabel(
	janela,
	text="TaskGuardian",
	font=("Arial", 28, "bold")
)

titulo.pack(pady=20)

menu = ctk.CTkFrame(
janela,
width=300,
corner_radius=0
)
menu.pack(side="left",fill="y")

conteudo=ctk.CTkFrame(
janela,
fg_color="#f6f8fc"

)

conteudo.pack(
side="left",
fill="both",
expand=True

)

titulo = ctk.CTkLabel(
	menu,
	text="TaskGuardian",
	font=("Arial",30,"bold"))
titulo.pack(pady=(20,5))

btn_inicio = ctk.CTkButton(
menu,
text="Página Inicial",
width=240,
height=45,
corner_radius=15
)
btn_inicio.pack(pady=10)

btn_inicio = ctk.CTkButton(
menu,
text="Desempenho",
width=240,
height=45,
corner_radius=15
)
btn_inicio.pack(pady=10)

btn_inicio = ctk.CTkButton(
menu,
text="Configurações",
width=240,
height=45,
corner_radius=15
)
btn_inicio.pack(pady=10)

#status = ctk.CTkFrame(
#conteudo,
#fg_color="#E8F9E7",
#corner_radius=20,
#height=170
#)
#status.pack(fill="x")
#status.pack_propagate(False)

status = ctk.CTkLabel(
	janela,
	text="Monitoramento de desempenho",
	font=("Arial", 16)
)

status.pack()
def criar_card(titulo):
	frame = ctk.CTkFrame(
	conteudo,
	width=250,
	height=200,
	corner_radius=20
	)
	frame.pack_propagate(False)
	label = ctk.CTkLabel(
	frame,
	text= titulo,
	font=("Arial",20,"bold")
)
	label.pack(pady=20)
	return frame
card1 = criar_card("memória")
card2 = criar_card ("CPU")
card3 = criar_card ("GPU")
card4 = criar_card ("Espaço em Disco")

card1.pack(side="left",padx=10,pady=10)
card2.pack(side="left",padx=10,pady=10)
card3.pack(side="left",padx=10,pady=10)
card4.pack(side="left",padx=10,pady=10)
janela.mainloop()
