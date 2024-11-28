# Importando os módulos
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import time
import pywhatkit as kit


# Criando a janela do aplicativo
root = tk.Tk()
root.title("Sendex")
root.geometry("800x800")
root.resizable(False, False)
root.iconbitmap("icone.ico")
root.configure(background='#F8F8FF')

# Carregando imagens do aplicativo
carregar_imagem_abrir = tk.PhotoImage(file='Abrir.png')
carregar_imagem_passo1 = tk.PhotoImage(file="Passo1.png")
carregar_imagem_passo2 = tk.PhotoImage(file="Passo2.png")
carregar_imagem_proximo = tk.PhotoImage(file='Proximo.png')
enviar_arquivo = tk.PhotoImage(file='Enviar.png')
imagem = tk.PhotoImage(file='Imagem.png')
local_imagem = ""

# Criando a primeira imagem do aplicativo
imagem_passo1 = tk.Canvas(root, width="800", height="230")
imagem_passo1.grid(pady=10, ipady=5, padx=2)
imagem_passo1.create_image(200, 160, image=carregar_imagem_passo1)
imagem_passo1.configure(background='#F8F8FF', highlightthickness=0)

# Criando botões passo 1
botao_abrir = tk.Button(root, image=carregar_imagem_abrir, width='150', height='100', command=lambda: Passo1())
botao_abrir.place(x="600", y="80")
botao_abrir.configure(background='#F8F8FF', border=0, cursor='hand2', activebackground='#F8F8FF')
botao2 = tk.Button(root, image=carregar_imagem_proximo, width=250, height=150, command=lambda: Passo2())
botao2.place(x="530", y="670")
botao2.configure(background='#F8F8FF', border=0, cursor='hand2', activebackground='#F8F8FF')

# Centralizando o Aplicativo
def center(win):
    win.update_idletasks()

    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width

    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width

    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2

    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    win.deiconify()

# Configurando passo 1
def Passo1():
    # Configurando o seletor das planilhas
    global arquivo_csv
    tipos_planilha = [('Planilhas', '*.csv')]
    arquivo_csv = filedialog.askopenfilename(filetypes=tipos_planilha, title='Selecione uma planilha')
    global read_csv
    read_csv = pd.read_csv(arquivo_csv)
    
    # Criando a Treeview para exibir a planilha
    global df
    df = ttk.Treeview(root)
    df.grid(ipadx=250, ipady=50, padx=45, pady=40)
    df["columns"] = ['Telefones']
    df['show'] = 'headings'
    for column in df['columns']:
        df.heading(column, text=column)

    df_linhas = read_csv.to_numpy().tolist()
    for linha in df_linhas:
        df.insert('', 'end', values=linha)

# Configurando passo 2
def Passo2():
    df.grid_remove()
    botao2.destroy()
    botao_abrir.destroy()
    imagem_passo1.destroy()

    imagem_passo2 = tk.Canvas(root, width="800", height="230")
    imagem_passo2.grid(pady=5, ipady=5, padx=2)
    imagem_passo2.create_image(200, 120, image=carregar_imagem_passo2)
    imagem_passo2.configure(background='#F8F8FF', highlightthickness=0)

    botao_enviar = tk.Button(root, image=enviar_arquivo, width=200, height=100, command=enviar_mensagens_texto)
    botao_enviar.place(x=580, y=700)
    botao_enviar.configure(background='#F8F8FF', border=0, cursor='hand2', activebackground='#F8F8FF')

    botao_imagem = tk.Button(root, image=imagem, width=230, height=60, cursor="hand2", background='#F8F8FF', activebackground='#F8F8FF', command=imagem_up)
    botao_imagem.place(x=560, y=50)
    botao_imagem.configure(border=0)

    global Caixadetexto
    Caixadetexto = tk.Text(root, background='#FFDEAD', height=15, yscrollcommand=root, autoseparators=False)
    Caixadetexto.grid(pady=10, padx=7, ipady=50, ipadx=70)

def imagem_up():
    tipos_imagem = [('Imagens', '*.jpg'), ('Imagens', '*.png'), ('Imagens', '*.jpeg')]
    global local_imagem
    local_imagem = filedialog.askopenfilename(filetypes=tipos_imagem, title="Selecione uma imagem")

    if not local_imagem:
        return

    imagem_upload = tk.Label(root, text=local_imagem, background='#FFDEAD', anchor='w')
    imagem_upload.place(x=10, y=610, width=500, height=25)



# Configurando o envio
def enviar_mensagens_texto():
    mensagem = Caixadetexto.get("1.0", tk.END).strip()

    if local_imagem and mensagem:
        # Enviar imagem e mensagem
        for _, linha in read_csv.iterrows():
            numero = str(linha['Mobile Phone'])
            if numero:
                kit.sendwhats_image(f"+{numero}", local_imagem, mensagem)
                time.sleep(2)  

    elif local_imagem:
        # Enviar apenas imagem
        for _, linha in read_csv.iterrows():
            numero = str(linha['Mobile Phone'])
            if numero:
                kit.sendwhats_image(f"+{numero}", local_imagem, "")
                time.sleep(2)  

    elif mensagem:
        # Enviar apenas mensagem
        for _, linha in read_csv.iterrows():
            numero = str(linha['Mobile Phone'])
            if numero:
                kit.sendwhatmsg_instantly(f"+{numero}", mensagem)
                time.sleep(2)  

    elif not mensagem:
        # Aviso caso não tenha imagem/mensagem
    
        messagebox.showinfo("Erro","Digite um texto ou selecione uma imagem para prosseguir.")
        return           


    root.quit()                
        

center(root)
root.mainloop()