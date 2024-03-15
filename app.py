import customtkinter as ctk
from tkinter import * 
import sqlite3
from tkinter import messagebox

class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect("Sistema_cadastros.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado")
        
    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado")
        
    def cria_tabela(self):
        self.conecta_db()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );              
        """)
        self.conn.commit()
        print("Tabela Criada com sucesso!")
        self.desconecta_db()
        
    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha = self.confirma_senha_entry.get()
        
       
        self.conecta_db()
        
        self.cursor.execute("""
            INSERT INTO Usuarios(Username, Email, Senha, Confirma_Senha)
            VALUES(?, ?, ?, ?)""",(self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha))
       
        try:
            if(self.username_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro =="" or self.confirma_senha ==""):
                messagebox.showerror(title="Sistema de login", message="ERROR!!!\n Porfavor Preencha todos os campos!")
            elif (len(self.username_cadastro) < 4):
                messagebox.showwarning(title="Sistema de login", message="O nome de usuário deve ser  de pelo menos 4 caracteres.")
            
            elif(self.senha_cadastro != self.confirma_senha):
                messagebox.showerror(title="Sistema de login", message="ERROR!!!\n As senhas colocadas não são iguais, Por favor verifique ")
           
            elif (len(self.senha_cadastro) < 4):
                messagebox.showwarning(title="Sistema de login", message="a senha  deve ser  de pelo menos 4 caracteres.")
           
            else:
                self.conn.commit()
                messagebox.showinfo(title="Sistema de login", message=f"Parabens {self.username_cadastro}\n Os seus dados foram cadastrados com sucesso!")
                self.desconecta_db()
                self.limpa_entry_cadastro()
            
        except:
            messagebox.showerror(title="Sistema de login", message=" Erro no processamento do seu cadastro\n Por favor, tente novamente ")
            self.desconecta_db()
            
    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()
    
        
        self.conecta_db()
        
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""",(self.username_login, self.senha_login))
        
        self.verifica_dados = self.cursor.fetchone()
        
        try:
            if (self.username_login == "" or self.senha_login == ""):
                messagebox.showwarning(title="Sistema de login", message="Por favor, preencha todos os campos!")
            elif (self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                messagebox.showinfo(title="Sistema de login", message=f"Parabens {self.username_login}\n Login feito com sucesso!")
                self.desconecta_db()
                self. limpa_entry_login()
        except:
            messagebox.showerror(title="Sistema de login", message="ERROR!!\n Dados não encontrados no sistema, por favor verifique ou cadastre - se no nosso sistema")       

            self.desconecta_db()

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracao_da_janela_inicial()
        self.tela_de_login()
        self.cria_tabela()
        
    
        
        
    def configuracao_da_janela_inicial(self):
        self.geometry("760x440")
        self.title("Sistema de Login")
        self.resizable(False, False)
        
        
    def tela_de_login(self):
        
    
        self.img =  PhotoImage(file="logi.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=5)
        
        #Titulo da nossa plataforma
        self.title = ctk.CTkLabel(self, text="Faça o seu login ou cadastra-se\n na nossa plataforma para acessar\nos nossos serviços!", font=("century Gothic bold", 14))
        self.title.grid(row=0, column=0, pady=10, padx=10)        
        
        
        #Criação da Frame do formulário
        
        self.frame_login = ctk.CTkFrame(self, width=360, height=380)
        self.frame_login.place(x=387, y=10)
        
        #Colocando width dentro do Formulario
        
        
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu Login", font=("century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=340, placeholder_text="seu nome de usuário..", font=("century Gothic bold", 16), corner_radius=15)
        self.username_login_entry.grid(row=1, column=0, pady =10, padx = 10)
        
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=340, placeholder_text="sua senha..", font=("century Gothic bold", 16), corner_radius=15, show="*")
        self.senha_login_entry.grid(row=2, column=0, pady =10, padx = 10)
        
        self.ver_senha = ctk.CTkCheckBox(self.frame_login, width=340, text="Clique para ver a senha", font=("century Gothic bold", 14), corner_radius=20, fg_color="#444", hover_color="purple")
        self.ver_senha.grid(row=3, column=0, pady=10, padx=10)
        
        self.btn_login = ctk.CTkButton(self.frame_login, fg_color="#444", hover_color="green", width=340, text="Fazer Login".upper(), font=("century Gothic bold", 16), corner_radius=15, command= self.verifica_login)
        self.btn_login.grid(row=4, column=0, pady=10, padx=10)
        
        self.span = ctk.CTkLabel(self.frame_login, text=" Se não tens conta, clique no botão abaixo para fazer o\n cadastro no nosso sistema!", font=("century Gothic", 10))
        self.span.grid(row=5, column=0, pady=10, padx=10)
        
        self.btn_cadastro=ctk.CTkButton(self.frame_login, width=340, fg_color="#444", hover_color="green",text="Fazer Cadastro".upper(), font=("century Gothic bold", 15), corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, padx=10)
        
        
        
        
    def tela_de_cadastro(self):
        
        self.frame_login.place_forget()
        
        
        #FRAME DE FORMULÁRIO DE CADASTRO
        self.frame_cadastro = ctk.CTkFrame(self, width=360, height=380)
        self.frame_cadastro.place(x=387, y=10)
        
         
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça o seu cadastro", font=("century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=340, placeholder_text="seu nome de usuário..", font=("century Gothic bold", 16), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, pady =5, padx = 10)
        
        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=340, placeholder_text="E-mail de usuário..", font=("century Gothic bold", 16), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, pady =5, padx = 10)
        
        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=340, placeholder_text="Senha de Usuário..", font=("century Gothic bold", 16), corner_radius=15, show="*")
        self.senha_cadastro_entry.grid(row=3, column=0, pady =5, padx = 10)
        
        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=340, placeholder_text="Confirme a senha de usuário..", font=("century Gothic bold", 16), corner_radius=15, show="*")
        self.confirma_senha_entry.grid(row=4, column=0, pady =5, padx = 10)
        
        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha", font=("century Gothic bold", 14), corner_radius=20, fg_color="#444", hover_color="purple")
        self.ver_senha.grid(row=5, column=0, pady=5)
        
        
        self.btn_cadastrar_user=ctk.CTkButton(self.frame_cadastro, fg_color="#444", hover_color="green", text="Fazer Cadastro".upper(), width=300, font=("century Gothic bold", 15), corner_radius=15, command = self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, pady=5, padx=10)

        self.btn_login_back=ctk.CTkButton(self.frame_cadastro, width= 300, text="Fazer Login".upper(), font=("century Gothic bold", 15), corner_radius=15, hover_color="#333", fg_color="#444", command=self.tela_de_login)
        self.btn_login_back.grid(row=7, column=0, pady=10, padx=10)
    
        
        
    def limpa_entry_cadastro(self): 
        self.username_cadastro_entry.delete(0, END)  
        self.email_cadastro_entry.delete(0, END)      
        self.senha_cadastro_entry.delete(0, END)  
        self.confirma_senha_entry.delete(0, END)
        
    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)
                    
    

if __name__ == "__main__":
    app = App()
    app.mainloop()