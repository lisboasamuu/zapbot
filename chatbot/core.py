# A interação inicial do bot vai ser através do terminal, sendo assim importamos o sistema operacional para este primeiro caso.
import json
import os
from datetime import datetime

class ChatBot:
    '''definimos o funcionamento padrão do bot'''
    def __init__(self):
        self.respostas = self.carregar_respostas()
        self.contexto = {}
        self.ultimo_fluxo = None

    def carregar_respostas(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'data', 'respostas.json')
        #obtem nosso database json lendo com o comando read e com ele aberto, volta uma favariavel f de file
        with open(path, 'r', encoding= 'utf-8') as f:
            return json.load(f)
        
    def normalizar_texto(self, texto):
        return texto.lower().strip()
    
    def detectar_intencoes(self, mensagem):
        msg = self.normalizar_texto(mensagem)
        #procurar se algum elemento da msg está dentro do nosso json
        if any(saudacao in msg for saudacao in self.respostas['saudacoes']):
            return 'saudação'
        if any(keyword in msg for keyword in self.respostas['suporte_keywords']):
            return 'suporte'
        if any(consultas in msg for consultas in self.respostas['consultas_keywords']):
            return 'consultas'
        if any(despedida in msg for despedida in self.respostas['despedidas']):
            return 'despedida'
        return 'desconhecido'
    
    def responder(self, mensagem, fluxo_atual = None):
        if fluxo_atual:
            return self.processar_fluxo(mensagem, fluxo_atual)
        intencao = self.detectar_intencoes(mensagem)
        repostas_rapidas = {
            'saudacao': self.responder['repostas_saudacao'],
            'despedida': "obrigado pelo contato!E stamos a disposição. Até mais",
            'suporte': 'Entendo que precisa de suporte. Vou direcionar a uma pessoa de nossa equipe.'
            'consultas': 'Perfeito, sua dúvida seria a agendamentos ou consultas passadas?',
            'desonhecido'>
        },

