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
     try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
     except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {path}")
        return {}
        
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
            return self.processar_fluxos(mensagem, fluxo_atual)
        intencao = self.detectar_intencoes(mensagem)
        respostas_rapidas = {
            'saudacao': self.respostas["respostas_saudacoes"], 
            'despedida': "Obrigado pelo contato! Estamos a disposição. Até mais",
            'suporte': 'Entendo que precisa de suporte. Vou direcionar a uma pessoa de nossa equipe\nAguarde um momento, por favor.',
            'consultas': 'Perfeito, sua dúvida seria a agendamentos ou consultas passadas?',
            'desconhecido': 'Não entendi muito bem. Você pode escolher uma das opções abaixo:\n1 - Suporte\n2 - Falar com atendente\n3- Sair'  
        }
        #retornar quais as intenções, as quais estritamente devem esta dentro do respostas rapidas
        return respostas_rapidas.get(intencao, "Como posso te ajudar hoje?")
    def processar_fluxos(self, mensagem, fluxo):  
        return f"Processando fluxo {fluxo}: {mensagem}"
    #Após a leitura da mensagem, o nosso bot irá buscar o fluxo adequado
