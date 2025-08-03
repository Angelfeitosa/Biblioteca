import sqlite3 as sql
import tkinter as tk 
from tkinter import messagebox, simpledialog

class Livro:
    def __init__(seft, id, titulo, autor, ano, genero, emprestado):
        seft.id = id
        seft.titulo = titulo
        seft.autor = autor 
        seft.ano = ano
        seft.genero = genero
        seft.emprestado = bool(emprestado)

    def __str__(self):
        if self.emprestado:
            status = "Emprestado"
        else:
            status = "Disponível"
            
        return f'{self.titulo} - {self.autor} ({self.ano}) - {self.genero} - {status}'
    
#Banco de dados  
  
class Bibliotecadb:
    def __init__(self, db_name='biblioteca.db'):
        self.conn = sql.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS livros 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            titulo TEXT NOT NULL, 
                            autor TEXT NOT NULL, 
                            ano INTEGER, 
                            genero TEXT,
                             emprestado INTEGER DEFAULT 0) ''')
        self.conn.commit()

    def adicionar_livro(self, livros: Livro ):
        self.cursor.execute(''' INSERT INTO Livro (titulo, autor, ano, genero, emprestado)
                            VALUES()''', (livros.titulo, livros.autor, livros.ano, livros.genero, int(livros.emprestado)))
        self.conn.commit()
    
    def listar_livros(self, filtro=None):
        if filtro:
            self.cursor.execute('SELECT * FROM livros WHERE titulo LIKE?', ('%'+filtro+'%',))

        else:
            self.cursor.execute('SELECT * FROM livros')

        row = self.cursor.fetchall()
        livros = [Livro(*row)for row in row]
        return livros
    
    def atualizar_status_emprestimo(seft, livro_id, emprestado):
        seft.cursor.execute('UPDATE livros SET emprestado = ? WHERE id = ?',
                            (int(emprestado), livro_id))
        seft.conn.commit()

    def fechar(self):
        self.conn.close()

#interface gráfica

class Bibliotecaapp:
    def __init__(self, root):
        self.root = root 
        self.root.title('Biblioteca')

        self.db = Bibliotecadb()

         #entrada para busca

        self.entry_busca = tk.Entry(root, width=40)
        self.entry_busca.pack(pady=5)
        self.entry_busca.insert(0, "Digite o título para busca: ")
        self.entry_busca.bind("<FocusIn>", self.limpar_placeholder)
        self.entry_busca.bind("<Return>", self.buscar_livros)

        #botão de busca

        self.btn_buscar = tk.Button(root, text="Buscar", command=self.buscar_livros)
        self.btn_buscar.pack(pady=5)

        #Lista de livros

        self.lista_livros = tk.Listbox(root, width=80, height=15)
        self.lista_livros.pack(pady=10)

        #Botões de Acão
        
        self.btn_adicionar = tk.Button(root, text='Adicionar Livro', command=self.adicionar_livro)
        self.btn_adicionar.pack(side=tk.LEFT, padx=10)

        self.btn_emprestar = tk.Button(root, text='Emprestar Livro', command=self.emprestar_livro)
        self.btn_emprestar.pack(side = tk.LEFT, padx=10)

        self.btn_devolver = tk.Button(root, text='Devolver Livro', command=self.devolver_livro)
        self.btn_devolver.pack(side=tk.LEFT, padx=10)

        self.btn_listar = tk.Button(root, text='Listar Todos', command=self.listar_todos)
        self.btn_listar.pack(side=tk.LEFT, padx=10)

        self.listar_todos()

    def limpar_placeholder(self, event):
        if self.entry_busca.get() == 'Digite o título para buscar':
            self.entry_busca.delete(0, tk.END)

    def listar_todos(self, filtro=None):
        self.lista_livros.delete(0, tk.END)
        livros = self.db.listar_livros(filtro)
        self.livros_mostrados = livros #armazenar referência para acões
        for livro in livros:
            self.lista_livros.insert(tk.END, str(livro))

    def buscar_livros(self, event=None):
        filtro = self.entry_busca.get()
        if filtro == "Digite título para buscar":
            filtro = None
        self.listar_todos(filtro)

    def adicionar_livro(self):
        titulo = simpledialog.askstring("Título", "Digite o título do livro:")
        if not titulo:
            return
        autor = simpledialog.askstring("Autor", "Digite o autor do livro:")
        if not autor:
            return
        try:
            ano = int(simpledialog.askstring("Ano", "Digite o ano do livro:"))
        except:
            ano = None
        genero = simpledialog.askstring("Gênero", "Digite o gênero do livro:")
        if not genero:
            genero = "Desconhecido"
        novo_livro = Livro(None, titulo, autor, ano, genero, False)
        self.db.adicionar_livro(novo_livro)
        messagebox.showinfo("Sucesso", f'Livro "{titulo}" adicionado.')
        self.listar_todos()

    def pegar_livro_selecionado(self):
        selecionado = self.lista_livros.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um livro na lista.")
            return None
        index = selecionado[0]
        return self.livros_mostrados[index]
    
    def emprestar_livro(self):
        livro = self.pegar_livro_selecionado()
        if livro:
            if livro.emprestado:
                messagebox.showinfo("Info", "Esse livro já está emprestado.")
            else:
                self.db.atualizar_status_emprestimo(livro.id, True)
                messagebox.showinfo("Sucesso", f'Livro "{livro.titulo}" emprestado.')
                self.listar_todos()

    def devolver_livro(self):
        livro = self.pegar_livro_selecionado()
        if livro:
            if not livro.emprestado:
                messagebox.showinfo("Info", "Esse livro não está emprestado.")
            else:
                self.db.atualizar_status_emprestimo(livro.id, False)
                messagebox.showinfo("Sucesso", f'Livro "{livro.titulo}" devolvido.')
                self.listar_todos()

#Execução

if __name__ == "__main__":
    root = tk.Tk()
    app = Bibliotecaapp(root)
    root.mainloop()



 