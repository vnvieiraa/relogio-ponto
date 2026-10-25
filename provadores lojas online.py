import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

# Repositório: https://github.com/vnvieiraa/relogio-ponto


class ProvadorVirtual:
    def __init__(self, root):
        self.root = root
        self.root.title("Provador Virtual | Loja Online")
        self.root.geometry("1000x750")
        self.root.configure(bg="#171717")

        self.camera = None
        self.roupa = None
        self.ultima_imagem = None
        self.executando = True

        tk.Label(
            root,
            text="PROVADOR VIRTUAL",
            font=("Arial", 22, "bold"),
            bg="#171717",
            fg="#ff69b4"
        ).pack(pady=12)

        self.preview = tk.Label(root, bg="#252525")
        self.preview.pack(pady=8)

        botoes = tk.Frame(root, bg="#171717")
        botoes.pack(pady=8)

        tk.Button(
            botoes, text="Carregar roupa PNG",
            command=self.carregar_roupa,
            bg="#ff69b4", fg="black",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=5)

        tk.Button(
            botoes, text="Salvar foto",
            command=self.salvar_foto,
            bg="#ffffff", fg="black",
            font=("Arial", 11)
        ).pack(side="left", padx=5)

        tk.Button(
            botoes, text="Fechar câmera",
            command=self.fechar_camera,
            bg="#444444", fg="white",
            font=("Arial", 11)
        ).pack(side="left", padx=5)

        self.escala = tk.IntVar(value=45)
        self.pos_x = tk.IntVar(value=50)
        self.pos_y = tk.IntVar(value=30)

        self.criar_controle(
            "Tamanho da roupa", self.escala, 10, 100
        )
        self.criar_controle(
            "Posição horizontal", self.pos_x, 0, 100
        )
        self.criar_controle(
            "Posição vertical", self.pos_y, 0, 100
        )

        self.status = tk.Label(
            root,
            text="Carregue uma roupa PNG para começar.",
            bg="#171717",
            fg="white"
        )
        self.status.pack(pady=8)

        self.iniciar_camera()
        self.atualizar_camera()

        self.root.protocol("WM_DELETE_WINDOW", self.encerrar)

    def criar_controle(self, titulo, variavel, minimo, maximo):
        tk.Label(
            self.root, text=titulo,
            bg="#171717", fg="white"
        ).pack()

        tk.Scale(
            self.root,
            from_=minimo,
            to=maximo,
            orient="horizontal",
            variable=variavel,
            length=400,
            bg="#171717",
            fg="white",
            highlightthickness=0
        ).pack()

    def iniciar_camera(self):
        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            self.camera.release()
            self.camera = None
            messagebox.showwarning(
                "Câmera",
                "Não foi possível abrir a câmera. "
                "Verifique a conexão e as permissões."
            )

    def carregar_roupa(self):
        caminho = filedialog.askopenfilename(
            title="Selecione uma roupa PNG transparente",
            filetypes=[("Imagens PNG", "*.png")]
        )

        if not caminho:
            return

        imagem = cv2.imread(caminho, cv2.IMREAD_UNCHANGED)

        if imagem is None:
            messagebox.showerror(
                "Erro", "Não foi possível abrir a imagem."
            )
            return

        if imagem.ndim != 3 or imagem.shape[2] != 4:
            messagebox.showerror(
                "Imagem inválida",
                "Selecione um PNG com canal alfa "
                "(fundo transparente)."
            )
            return

        # OpenCV BGRA -> RGBA
        self.roupa = cv2.cvtColor(
            imagem, cv2.COLOR_BGRA2RGBA
        )

        self.status.config(
            text="Roupa carregada! Ajuste tamanho e posição."
        )

    def compor_roupa(self, frame):
        imagem = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        if self.roupa is None:
            return imagem

        altura, largura = imagem.shape[:2]

        largura_roupa = max(
            1, int(largura * self.escala.get() / 100)
        )

        proporcao = (
            self.roupa.shape[0] / self.roupa.shape[1]
        )
        altura_roupa = max(1, int(largura_roupa * proporcao))

        roupa = cv2.resize(
            self.roupa,
            (largura_roupa, altura_roupa),
            interpolation=cv2.INTER_AREA
        )

        # Posição ajustável
        x = int(
            (largura - largura_roupa)
            * self.pos_x.get() / 100
        )
        y = int(
            (altura - altura_roupa)
            * self.pos_y.get() / 100
        )

        # Recortar a roupa quando ultrapassar a imagem
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(largura, x + largura_roupa)
        y2 = min(altura, y + altura_roupa)

        if x1 >= x2 or y1 >= y2:
            return imagem

        roupa_x1 = x1 - x
        roupa_y1 = y1 - y
        roupa_x2 = roupa_x1 + (x2 - x1)
        roupa_y2 = roupa_y1 + (y2 - y1)

        recorte = roupa[
            roupa_y1:roupa_y2,
            roupa_x1:roupa_x2
        ]

        regiao = imagem[y1:y2, x1:x2].astype(np.float32)
        cor = recorte[:, :, :3].astype(np.float32)

        # Transparência do PNG
        alfa = recorte[:, :, 3:4].astype(np.float32) / 255

        imagem[y1:y2, x1:x2] = (
            cor * alfa + regiao * (1 - alfa)
        ).astype(np.uint8)

        return imagem

    def atualizar_camera(self):
        if self.camera is not None and self.camera.isOpened():
            sucesso, frame = self.camera.read()

            if sucesso:
                frame = cv2.flip(frame, 1)
                resultado = self.compor_roupa(frame)

                self.ultima_imagem = resultado.copy()

                # Redimensionar a visualização
                foto = Image.fromarray(resultado)
                foto.thumbnail((850, 430))

                foto_tk = ImageTk.PhotoImage(foto)
                self.preview.configure(image=foto_tk)
                self.preview.image = foto_tk

        if self.executando:
            self.root.after(30, self.atualizar_camera)

    def salvar_foto(self):
        if self.ultima_imagem is None:
            messagebox.showwarning(
                "Aviso", "Nenhuma imagem disponível."
            )
            return

        caminho = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagem PNG", "*.png")],
            initialfile="provador_virtual.png"
        )

        if caminho:
            imagem_bgr = cv2.cvtColor(
                self.ultima_imagem, cv2.COLOR_RGBA2BGRA
            )
            # Salva a visualização composta em PNG
            imagem_rgb = cv2.cvtColor(
                self.ultima_imagem, cv2.COLOR_RGBA2RGB
            )
            sucesso = cv2.imwrite(
                caminho,
                cv2.cvtColor(imagem_rgb, cv2.COLOR_RGB2BGR)
            )

            if sucesso:
                messagebox.showinfo(
                    "Sucesso", "Foto salva com sucesso!"
                )

    def fechar_camera(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.preview.configure(
            image="",
            text="Câmera fechada",
            fg="white"
        )

    def encerrar(self):
        self.executando = False

        if self.camera is not None:
            self.camera.release()

        self.root.destroy()


if __name__ == "__main__":
    janela = tk.Tk()
    app = ProvadorVirtual(janela)
    janela.mainloop()
