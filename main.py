import customtkinter as ctk
import psutil
from PIL import Image
import platform
import time
import GPUtil
#import matplotlib.pyplot as plt
#import numpy as np

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

    titulo_label = ctk.CTkLabel(
        frame,
        text=titulo,
        font=("Arial",20,"bold")
    )
    titulo_label.pack(pady=(15,5))

    valor_label = ctk.CTkLabel(
        frame,
        text="0%",
        font=("Arial",36,"bold")
    )
    valor_label.pack()

    barra = ctk.CTkProgressBar(frame,width=180)
    barra.pack(pady=15)
    barra.set(0)

    status = ctk.CTkLabel(
        frame,
        text="Aguardando leitura...",
        font=("Arial",14)
    )
    status.pack()

    return frame, valor_label, barra, status

card_memoria, memoria_label, memoria_bar, memoria_status = criar_card("Memória")
card_cpu, cpu_label, cpu_bar, cpu_status = criar_card("CPU")
card_gpu, gpu_label, gpu_bar, gpu_status = criar_card("GPU")
card_disco, disco_label, disco_bar, disco_status = criar_card("Espaço em Disco")

card_memoria.pack(side="left", padx=10, pady=10)
card_cpu.pack(side="left", padx=10, pady=10)
card_gpu.pack(side="left", padx=10, pady=10)
card_disco.pack(side="left", padx=10, pady=10)

def obterHardware():
    cpu = psutil.cpu_percent(interval=None)
    memoria = psutil.virtual_memory().percent

    if platform.system() == "Windows":
        disco = psutil.disk_usage("C:\\").percent
    else:
        disco = psutil.disk_usage("/").percent

    return cpu, memoria, disco

def obter_status(valor):

    if valor < 50:
        return "🟢 Bom"

    elif valor < 80:
        return "🟡 Médio"

    else:
        return "🔴 Crítico"
    
def atualizar():

    cpu, memoria, disco = obterHardware()

    cpu_label.configure(text=f"{cpu:.0f}%")
    cpu_bar.set(cpu/100)
    cpu_status.configure(text=obter_status(cpu))

    memoria_label.configure(text=f"{memoria:.0f}%")
    memoria_bar.set(memoria/100)
    memoria_status.configure(text=obter_status(memoria))

    disco_label.configure(text=f"{disco:.0f}%")
    disco_bar.set(disco/100)
    disco_status.configure(text=obter_status(disco))

    try:
        gpus = GPUtil.getGPUs()

        if gpus:
            uso = gpus[0].load*100

            gpu_label.configure(text=f"{uso:.0f}%")
            gpu_bar.set(uso/100)
            gpu_status.configure(text=obter_status(uso))

        else:
            gpu_label.configure(text="--")
            gpu_bar.set(0)
            gpu_status.configure(text="Sem GPU")

    except:
        gpu_label.configure(text="--")
        gpu_bar.set(0)
        gpu_status.configure(text="Não disponível")

    janela.after(1000, atualizar)

def status_cpu(cpu):

    if cpu < 50:
        return "🟢 Bom"

    elif cpu < 80:
        return "🟡 Médio"

    else:
        return "🔴 Alto uso"

def status_memoria(memoria):

    if memoria < 60:
        return "🟢 Normal"

    elif memoria < 85:
        return "🟡 Atenção"

    else:
        return "🔴 Memória quase cheia"
    
def status_disco(disco):

    if disco < 70:
        return "🟢 Espaço suficiente"

    elif disco < 90:
        return "🟡 Pouco espaço"

    else:
        return "🔴 Disco quase cheio"


    
atualizar()

janela.mainloop()
