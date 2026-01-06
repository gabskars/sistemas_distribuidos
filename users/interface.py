from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from service import UserService


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


def start_user_service():
    """
    Interface RPC do Serviço de Usuários
    Responsável por expor remotamente as operações de cadastro e gerenciamento.
    Tecnologia de comunicação: RPC (XML-RPC)
    """
    user_service = UserService()

    server = SimpleXMLRPCServer(
        ("0.0.0.0", 8000),
        requestHandler=RequestHandler,
        allow_none=True
    )

    server.register_instance(user_service)

    print("[UserService] Interface RPC iniciada na porta 8000.")
    server.serve_forever()


if __name__ == "__main__":
    start_user_service()
