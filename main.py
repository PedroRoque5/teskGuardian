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

logo = ctk.CTkImage(
    light_image=Image.open("assets/images/logo.png"),
    dark_image=Image.open("assets/images/logo.png"),
    size=(80, 80)
)

logo_label = ctk.CTkLabel(
    menu,
    image=logo,
    text=""
)

logo_label.pack(pady=(20,5))

btn_inicio = ctk.CTkButton(
menu,
text="🏠 Página Inicial",
width=240,
height=45,
corner_radius=15
)

btn_inicio.pack(pady=10)

btn_inicio = ctk.CTkButton(
menu,
text="📈 Desempenho",
width=240,
height=45,
corner_radius=15
)
btn_inicio.pack(pady=10)

btn_inicio = ctk.CTkButton(
menu,
text="⚙ Configurações",
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

cabecalho = ctk.CTkFrame(
    conteudo,
    height=190,
    corner_radius=15,
    fg_color="white"
)

cabecalho.pack(fill="x", padx=20, pady=(20,10))
cabecalho.pack_propagate(False)

so = platform.system() + " " + platform.release()
cpu_nome = platform.processor()
ram_total = round(psutil.virtual_memory().total / (1024**3), 1)
arquitetura = platform.architecture()[0]
hostname = platform.node()

titulo_sistema = ctk.CTkLabel(
    cabecalho,
    text="Informações do Sistema",
    font=("Arial",28,"bold")
)

titulo_sistema.pack(anchor="w", padx=20, pady=(10,5))

info = ctk.CTkLabel(
    cabecalho,
    justify="left",
    anchor="w",
    font=("Arial",15),
    text=f"""
    💻 Computador: {hostname}
    🖥 Sistema Operacional: {so}
    ⚙ Processador: {cpu_nome}
    🧠 Memória RAM Instalada: {ram_total} GB
    📦 Arquitetura: {arquitetura}
    """
)

info.pack(anchor="w", padx=20)

cards_frame = ctk.CTkFrame(
    conteudo,
    fg_color="transparent"
)

cards_frame.pack(pady=30)

titulo_processos = ctk.CTkLabel(
    conteudo,
    text="Gerenciador de Tarefas",
    font=("Arial", 22, "bold")
)

titulo_processos.pack(anchor="w", padx=20, pady=(30,10))

tabela = ctk.CTkTextbox(
    conteudo,
    width=1100,
    height=250,
    font=("Consolas", 14)
)

tabela.pack(fill="x", padx=20, pady=(0,20))

def listar_processos():

    tabela.delete("1.0", "end")

    tabela.insert(
        "end",
        f"{'Processo':30}{'PID':10}{'CPU%':10}{'RAM(MB)':10}\n"
    )

    tabela.insert(
        "end",
        "-" * 70 + "\n"
    )

    processos = []

    for proc in psutil.process_iter(
        ['pid', 'name', 'memory_info']
    ):

        try:

            cpu = proc.cpu_percent()

            memoria = proc.info['memory_info'].rss / (1024*1024)

            processos.append((
                cpu,
                proc.info['name'],
                proc.info['pid'],
                memoria
            ))

        except:

            pass

    processos.sort(reverse=True)

    for cpu, nome, pid, memoria in processos[:15]:

        tabela.insert(
            "end",
            f"{nome[:28]:30}{pid:<10}{cpu:<10.0f}{memoria:<10.0f}\n"
        )

def criar_card(titulo):
    frame = ctk.CTkFrame(
        cards_frame,
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

card_memoria, memoria_label, memoria_bar, memoria_status = criar_card("💾 Memória")
card_cpu, cpu_label, cpu_bar, cpu_status = criar_card("🖥️ CPU")
card_gpu, gpu_label, gpu_bar, gpu_status = criar_card("🎮 GPU")
card_disco, disco_label, disco_bar, disco_status = criar_card("📁 Disco")

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

    listar_processos()

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
    
atualizar()

janela.mainloop()
