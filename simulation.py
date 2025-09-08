import random, math

class Book:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
            
    def __repr__(self):
            return f"Book(title: {self.title})"
        
class File:
    def __init__(self, id, book_id, num_part, total_parts, part):
         self.id = id
         self.book_id = book_id
         self.num_part = num_part
         self.total_parts = total_parts
         self.content = part
    
    def __repr__(self):
            return f"File(id: {self.id}, book_id: {self.book_id}, content: {self.content}), parte: {self.num_part}"
        
class Nodo:
    def __init__(self, id_nodo):
        self.id = id_nodo
        self.files = set() 
        self.connections = set()

    def __repr__(self):
        return f"Nodo(ID: {self.id})"
    
    def search_files(self, book_id):
        files = set()
        for file in self.files:
            if file.book_id == book_id:
                files.add(file)
        return files
    
class BookManager:
    def __init__(self):
         self.books = set()
         
    def create_book(self, book):
        self.books.add(book)
    
class P2p_simulation:
    
    def __init__(self, num_nodes, connections_by_node):
        self.book_manager = BookManager()        
        self.nodes = [Nodo(i) for i in range(num_nodes)]
        self.connect_nodes(connections_by_node)
        
    def connect_nodes(self, connections_by_node):
        for i in range(len(self.nodes)):
            print(i)
            if i < len(self.nodes)-1:
                self.nodes[i].connections.add(self.nodes[i+1].id)
                self.nodes[i+1].connections.add(self.nodes[i].id)
                
            
        #for node in self.nodes:
        #    possible_connections = list(set(n.id for n in self.nodes) - {node.id})
        #    chosen_connections = random.sample(possible_connections, min(connections_by_node, len(possible_connections)))
        #    node.connections.update(chosen_connections)
        #    for id_conection in chosen_connections:
        #        self.nodes[id_conection].connections.add(node.id)
                
    def create_book(self, book, number_parts):
        self.book_manager.create_book(book)
        
        n = len(book.content) // number_parts
        parts = [book.content[i*n : (i+1)*n] for i in range(number_parts-1)]
        parts.append(book.content[(number_parts-1)*n:]) 
        self.distribute_parts(number_parts, book, parts)
        print("Libro creado correctamente")

        
    def distribute_parts(self, number_parts, book, parts):
        if number_parts < len(self.nodes):
            chosen_nodes = random.sample(self.nodes, number_parts)
            num_part = 0
            for node in chosen_nodes:
                node.files.add(File(math.trunc(random.random()*100000), book.id, num_part, number_parts, parts.pop(0)))
                num_part += 1
        elif number_parts == len(self.nodes):
            num_part = 0
            for node in self.nodes:
                node.files.add(File(math.trunc(random.random()*100000), book.id, num_part, number_parts, parts.pop(0)))
                num_part += 1
        
    def search_book(self, book_id, node_id):
        visited = {node_id}
        node = self.search_node(node_id)
        found_parts = set()
        total_parts = 0
        if node:
            search_quewe = list(node.connections)
            
            node_parts = node.search_files(book_id)
            if node_parts:
                total_parts = next(iter(node_parts)).total_parts
                found_parts.update(node_parts)
            
            print(f"Conexiones: {node.connections}")
            
            while search_quewe:
                current_id = search_quewe.pop(0)
                print(current_id)
                current_node = self.search_node(current_id)
                
                if current_node.id in visited:
                    continue
                    
                visited.add(current_node.id)
                
                node_parts = current_node.search_files(book_id)
                if node_parts:
                    total_parts = next(iter(node_parts)).total_parts
                    found_parts.update(node_parts)
                
                for connection in current_node.connections:
                    if connection not in visited:
                        search_quewe.append(connection)
            
            if len(found_parts) == total_parts:
                print("Libro encontrado en su totalidad")
                for part in found_parts:
                    print(part)
            elif len(found_parts) == 0:
                print("Libro no encontrado")
            else:
                print("Libro no encontrado en su totalidad")                     
                for part in found_parts:
                    print(part)
            
        else:
            return False
        
    def search_node(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return False
    
class Presenter:
    def run(self):
        self.id_books = 0
        num_nodes = input("Ingrese la cantidad de nodos que se manejará:\n")
        self.p2p_simulation = P2p_simulation(int(num_nodes), 0)
        self.show_menu()
        
    def show_menu(self):
        option = 0
        exit_option = "3"
        while option != exit_option:
            option = input("Ingrese la opción que desea realizar:\n" + 
                            "1. Registrar un libro\n"+
                            "2. Buscar un libro\n"+
                            "3. Salir\n")
           
            if option == "1":
                self.register_book()
            elif option == "2":
                self.search_book()
            elif option == exit_option:
                print("¡Vuelva pronto!")
            else:
                print("Opción inválida")
    
    def register_book(self):
        title_book = input("Ingrese el nombre del libro:\n")
        content_book = input("Ingrese el contenido del libro:\n")
        num_parts = int(input("Ingrese la cantidad de partes en la que desea dividir el libro: \n"))
        
        self.p2p_simulation.create_book(Book(self.id_books, title_book, content_book), num_parts)
        print(f"el libro fue creado con el id {self.id_books}\n")
        self.id_books += 1
        
    def search_book(self):
            id_book = int(input("Ingrese el id del libro que está buscando:\n"))
            id_node = int(input("Ingrese el id del nodo desde el cual desea iniciar la búsqueda:\n"))
            self.p2p_simulation.search_book(id_book, id_node)
    
presenter = Presenter()
presenter.run()         
        
#text = "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quasi eum, nam, consequuntur alias debitis illum repellat sequi aperiam odio tempore tempora officia ea similique? Modi, nobis repellat reiciendis voluptas dolorum voluptate. Maxime amet autem ipsa reiciendis quos aperiam cupiditate corporis, ab dolores ducimus magnam esse distinctio reprehenderit atque? Dignissimos ipsam dicta earum libero, sequi ex nisi eius ducimus aliquam praesentium laboriosam optio. Maiores, delectus assumenda fuga eum labore ipsum adipisci ad incidunt tenetur repellat quo exercitationem. Explicabo pariatur cum culpa quae sequi doloribus labore, fugit amet nobis, a eum necessitatibus reiciendis! Hic, culpa! Mollitia temporibus laborum labore, atque fugit culpa?"
#
#test = P2p_simulation(5, 2)
#test.create_book(Book(1, "El libro de la selva", text), 3)
#test.search_book(1, 2)

