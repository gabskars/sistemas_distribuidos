class UserService:
    def __init__(self):
        self.usuarios = {}
        self.proximo_id = 1

    def criar_usuario(self, nome, perfil):
        usuario = {
            "id": self.proximo_id,
            "nome": nome,
            "perfil": perfil,
            "ativo": True
        }
        self.usuarios[self.proximo_id] = usuario
        self.proximo_id += 1
        return usuario

    def listar_usuarios(self):
        return list(self.usuarios.values())

    def buscar_usuario(self, user_id):
        user_id = int(user_id)
        if user_id in self.usuarios:
            return self.usuarios[user_id]
        return {"erro": "Usuário não encontrado"}

    def atualizar_usuario(self, user_id, nome, perfil, ativo):
        user_id = int(user_id)
        if user_id not in self.usuarios:
            return {"erro": "Usuário não encontrado"}

        self.usuarios[user_id]["nome"] = nome
        self.usuarios[user_id]["perfil"] = perfil
        self.usuarios[user_id]["ativo"] = ativo
        return self.usuarios[user_id]

    def remover_usuario(self, user_id):
        user_id = int(user_id)
        if user_id in self.usuarios:
            self.usuarios[user_id]["ativo"] = False
            return {"status": "Usuário desativado"}
        return {"erro": "Usuário não encontrado"}
