# a interação inicial do bot vai ser através do terminal, sendo assim importamos o sistema operacional para este primeiro caso.
import json
import os
from datetime import datetime, timedelta  # vamos utiliza-las para ensinar ao python as diferentes formas de representar data
from data.config import Config  # Trazemos o config pra ca para que as configurações do db interaja direto com o código 
import re

class ChatBot:
    '''definimos o funcionamento padrão do bot'''
    def __init__(self):
        self.config = Config()  # ADICIONE ESTA LINHA
        self.respostas = self.carregar_respostas()
        self.contexto = {}
        self.fluxo_atual = None  # 'suporte', 'consultas', 'atendente'
        self.passo_consultas = None  # Controla os passos do fluxo de consultas
        self.dados_agendamento = {}
        
    def carregar_respostas(self):
        # Tenta diferentes caminhos para encontrar o arquivo respostas.json
        possiveis_caminhos = [
            os.path.join(os.path.dirname(__file__), '..', 'data', 'respostas.json'),
            os.path.join(os.path.dirname(__file__), 'data', 'respostas.json'),
            'data/respostas.json',
            'respostas.json'
        ]
        
        for path in possiveis_caminhos:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except FileNotFoundError:
                continue
        
        print(f"Erro: Arquivo respostas.json não encontrado")
        return {
            "saudacoes": ["Oi", "olá", "bom dia", "boa tarde", "boa noite", "hello"],
            "respostas_saudacoes": ["Olá! Seja bem vindo a Clinica Life. Como posso te ajudar hoje?"],
            "suporte_keywords": ["problema", "remédio", "medicação", "ajuda", "receita", "exame", "hora", "endereço", "local", "localização", "médico", "falar", "atendente", "suporte"],
            "consultas_keywords": ["remarcar", "agendar", "data", "dia", "horas", "hora", "reagendar", "cancelar", "consulta", "consultas", "agendamento"],
            "despedidas": ["obrigado", "valeu", "obg", "vlw", "tchau", "até mais"]
        }
        
    def normalizar_texto(self, texto):
        return texto.lower().strip()
    
    def detectar_intencoes(self, mensagem):
        msg = self.normalizar_texto(mensagem)
        
        # Verifica se é uma despedida primeiro
        if any(despedida in msg for despedida in self.respostas.get('despedidas', [])):
            return 'despedida'
        
        # Verifica se é saudação
        if any(saudacao in msg for saudacao in self.respostas.get('saudacoes', [])):
            return 'saudacao'
        
        # Verifica se é suporte
        if any(keyword in msg for keyword in self.respostas.get('suporte_keywords', [])):
            return 'suporte'
        
        # Verifica se é consultas
        if any(consultas in msg for consultas in self.respostas.get('consultas_keywords', [])):
            return 'consultas'
        
        # Verifica opções numéricas
        if msg == '1':
            return 'suporte'
        if msg == '2':
            return 'consultas'
        if msg == '3':
            return 'atendente'
        
        return 'desconhecido'
    
    def processar_suporte(self, mensagem):
        """Processa o fluxo de suporte"""
        if not self.fluxo_atual:
            self.fluxo_atual = 'suporte'
            # Usa o config se disponível, senão usa mensagem padrão
            if hasattr(self, 'config') and hasattr(self.config, 'fluxos'):
                return self.config.fluxos.get('suporte', 'Descreva o seu problema em poucas palavras:')
            return 'Descreva o seu problema em poucas palavras:'
        else:
            # Aqui você pode salvar o problema do usuário em um banco de dados
            print(f"[LOG] Problema do usuário: {mensagem}")  # Log para debug
            self.fluxo_atual = None
            return "Obrigado por reportar! Nossa equipe entrará em contato em breve. Algo mais que possamos ajudar?"
    
    def processar_atendente(self, mensagem):
        """Processa o fluxo de atendente"""
        self.fluxo_atual = None
        if hasattr(self, 'config') and hasattr(self.config, 'fluxos'):
            return self.config.fluxos.get('atendente', 'Certo, estou transferindo você para um atendente humano. Em breve retomamos o contato.')
        return 'Certo, estou transferindo você para um atendente humano. Em breve retomamos o contato.'
    
    def extrair_data_da_mensagem(self, mensagem):
        """
        Extrai a data da mensagem do usuário de forma inteligente
        Retorna a data no formato DD/MM/YYYY ou None se não encontrar
        """
        msg_lower = mensagem.lower()
        
        # Padrão para encontrar datas no formato DD/MM/AAAA ou DD/MM
        padrao_data_completa = r'\b(\d{1,2})[/-](\d{1,2})(?:[/-](\d{4}))?\b'
        match = re.search(padrao_data_completa, mensagem)
        
        if match:
            dia = int(match.group(1))
            mes = int(match.group(2))
            ano = match.group(3)
            
            if ano:
                ano = int(ano)
            else:
                # Se não tem ano, usa o ano atual
                ano = datetime.now().year
                
            # Valida se é uma data válida
            try:
                data_validada = datetime(ano, mes, dia)
                return data_validada.strftime('%d/%m/%Y')
            except ValueError:
                pass
        
        # Padrão para encontrar "dia 15", "dia 15/04", etc.
        padrao_dia = r'dia\s+(\d{1,2})(?:\s*[/-]\s*(\d{1,2}))?'
        match = re.search(padrao_dia, msg_lower)
        
        if match:
            dia = int(match.group(1))
            
            if match.group(2):  # Tem mês
                mes = int(match.group(2))
                ano = datetime.now().year
                try:
                    data_validada = datetime(ano, mes, dia)
                    return data_validada.strftime('%d/%m/%Y')
                except ValueError:
                    pass
            else:
                # Só tem o dia, vamos procurar no próximo mês
                # Por simplicidade, vamos considerar que é nos próximos dias
                hoje = datetime.now()
                # Encontra o próximo dia do mês que seja >= hoje
                for dias_a_frente in range(1, 31):
                    data_candidata = hoje + timedelta(days=dias_a_frente)
                    if data_candidata.day == dia:
                        return data_candidata.strftime('%d/%m/%Y')
        
        # Padrão para encontrar "15 de abril", "15 de abr", etc.
        meses = {
            'janeiro': 1, 'jan': 1, 'fevereiro': 2, 'fev': 2,
            'março': 3, 'mar': 3, 'abril': 4, 'abr': 4,
            'maio': 5, 'junho': 6, 'jun': 6, 'julho': 7, 'jul': 7,
            'agosto': 8, 'ago': 8, 'setembro': 9, 'set': 9,
            'outubro': 10, 'out': 10, 'novembro': 11, 'nov': 11,
            'dezembro': 12, 'dez': 12
        }
        
        padrao_data_texto = r'(\d{1,2})\s+de\s+([a-záéíóúãõç]+)'
        match = re.search(padrao_data_texto, msg_lower)
        
        if match:
            dia = int(match.group(1))
            mes_nome = match.group(2)
            
            if mes_nome in meses:
                mes = meses[mes_nome]
                ano = datetime.now().year
                try:
                    data_validada = datetime(ano, mes, dia)
                    return data_validada.strftime('%d/%m/%Y')
                except ValueError:
                    pass
        
        return None

    def extrair_horario_da_mensagem(self, mensagem):
        """
        Extrai o horário da mensagem do usuário de forma inteligente
        Retorna o horário no formato HH:MM ou None se não encontrar
        """
        msg_lower = mensagem.lower()
        
        # Padrão para encontrar horários no formato HH:MM ou HH:MM AM/PM
        padrao_horario = r'\b(\d{1,2})[:](\d{2})\b'
        match = re.search(padrao_horario, mensagem)
        
        if match:
            hora = int(match.group(1))
            minuto = int(match.group(2))
            
            # Verifica se é um horário válido
            if 0 <= hora <= 23 and 0 <= minuto <= 59:
                return f"{hora:02d}:{minuto:02d}"
        
        # Padrão para encontrar "as 9", "as 9h", "9 horas", etc.
        padrao_hora_simples = r'(?:às?\s+|a\s+)?(\d{1,2})(?:\s*h(?:\s*horas?)?)?'
        match = re.search(padrao_hora_simples, msg_lower)
        
        if match:
            hora = int(match.group(1))
            
            # Verifica se é um horário válido
            if 0 <= hora <= 23:
                # Verifica se tem indicação AM/PM
                if 'pm' in msg_lower or 'p.m' in msg_lower:
                    if hora != 12:
                        hora += 12
                elif 'am' in msg_lower or 'a.m' in msg_lower:
                    if hora == 12:
                        hora = 0
                
                return f"{hora:02d}:00"
        
        # Padrão para encontrar "meio-dia", "meio dia", "12h"
        if any(p in msg_lower for p in ['meio-dia', 'meio dia', '12h', '12 horas']):
            return "12:00"
        
        # Padrão para encontrar "meia-noite", "meia noite", "0h"
        if any(p in msg_lower for p in ['meia-noite', 'meia noite', '0h', '0 horas']):
            return "00:00"
        
        return None

    def validar_data_disponivel(self, data_str):
        """
        Verifica se a data está disponível para agendamento
        Retorna a data formatada se disponível, None se não
        """
        datas_disponiveis = ['15/04/2026', '16/04/2026', '17/04/2026']
        
        # Tenta encontrar a data na lista de disponíveis
        for data_disponivel in datas_disponiveis:
            if data_str == data_disponivel:
                return data_disponivel
        
        # Se não encontrou exatamente, tenta comparar apenas dia e mês
        try:
            # Extrai dia e mês da data informada
            partes_data = data_str.split('/')
            if len(partes_data) >= 2:
                dia_informado = partes_data[0]
                mes_informado = partes_data[1]
                
                for data_disponivel in datas_disponiveis:
                    partes_disponivel = data_disponivel.split('/')
                    if len(partes_disponivel) >= 2:
                        if partes_disponivel[0] == dia_informado and partes_disponivel[1] == mes_informado:
                            return data_disponivel
        except:
            pass
        
        return None

    def validar_horario_disponivel(self, horario_str):
        """
        Verifica se o horário está disponível para agendamento
        Retorna o horário formatado se disponível, None se não
        """
        horarios_disponiveis = ['08:00', '09:00', '10:00', '14:00', '15:00', '16:00']
        
        # Tenta encontrar o horário na lista de disponíveis
        if horario_str in horarios_disponiveis:
            return horario_str
        
        # Se não encontrou, tenta arredondar para o horário mais próximo
        try:
            hora, minuto = map(int, horario_str.split(':'))
            
            # Arredonda os minutos para 00
            horario_arredondado = f"{hora:02d}:00"
            
            if horario_arredondado in horarios_disponiveis:
                return horario_arredondado
        except:
            pass
        
        return None

    def processar_consultas(self, mensagem):
        """Processa o fluxo de consultas passo a passo"""
        
        # Inicia o fluxo de consultas se não estiver ativo
        if not self.passo_consultas:
            self.fluxo_atual = 'consultas'
            self.passo_consultas = 'aguardando_acao'
            if hasattr(self, 'config') and hasattr(self.config, 'fluxos'):
                return self.config.fluxos.get('consultas', 'Deseja marcar consulta, ver agendamentos ou remarcar?')
            return 'Deseja marcar consulta, ver agendamentos ou remarcar?'
        
        # Passo 1: Aguardando o usuário dizer o que quer fazer
        if self.passo_consultas == 'aguardando_acao':
            msg_lower = mensagem.lower()
            
            if any(p in msg_lower for p in ('marcar', 'agendar', 'agendamento')):
                self.passo_consultas = 'aguardando_especialidade'
                return "Perfeito! Vou te ajudar a agendar. Qual especialidade você procura?"
            
            elif any(p in msg_lower for p in ('ver', 'meus', 'visualizar', 'listar')):
                self.passo_consultas = None
                self.fluxo_atual = None
                return "Aqui estão seus agendamentos:\n- Cardiologia - 15/04/2026 às 09:00\n- Dermatologia - 20/04/2026 às 14:00\n\nDeseja fazer mais alguma coisa?"
            
            elif any(p in msg_lower for p in ('remarcar', 'reagendar', 'cancelar')):
                self.passo_consultas = None
                self.fluxo_atual = None
                return "Para remarcar ou cancelar, por favor, entre em contato pelo telefone: 0800 123 4567\n\nPosso ajudar em mais alguma coisa?"
            
            else:
                return "Não entendi. Por favor, escolha uma opção:\n- Marcar consulta\n- Ver meus agendamentos\n- Remarcar consulta"
        
        # Passo 2: Aguardando a especialidade
        elif self.passo_consultas == 'aguardando_especialidade':
            especialidades_disponiveis = ['cardiologia', 'dermatologia', 'ortopedia', 'pediatria', 'ginecologia']
            
            especialidade_encontrada = None
            for esp in especialidades_disponiveis:
                if esp in mensagem.lower():
                    especialidade_encontrada = esp
                    break
            
            if especialidade_encontrada:
                self.dados_agendamento['especialidade'] = especialidade_encontrada
                self.passo_consultas = 'aguardando_data'
                return f"Ótimo! Para {especialidade_encontrada.title()} temos disponibilidade nos seguintes dias:\n- 15/04/2026\n- 16/04/2026\n- 17/04/2026\n\nQual dia você prefere? (Ex: 15/04, dia 15, 15 de abril)"
            else:
                return f"Especialidade não reconhecida. Por favor, escolha uma das especialidades disponíveis:\n- Cardiologia\n- Dermatologia\n- Ortopedia\n- Pediatria\n- Ginecologia"
        
        # Passo 3: Aguardando a data (VERSÃO MELHORADA)
        elif self.passo_consultas == 'aguardando_data':
            # Extrai a data da mensagem do usuário
            data_extraida = self.extrair_data_da_mensagem(mensagem)
            
            if data_extraida:
                # Valida se a data está disponível
                data_valida = self.validar_data_disponivel(data_extraida)
                
                if data_valida:
                    self.dados_agendamento['data'] = data_valida
                    self.passo_consultas = 'aguardando_horario'
                    return f"Ótimo! Para o dia {data_valida} temos os seguintes horários disponíveis:\n08:00, 09:00, 10:00, 14:00, 15:00, 16:00\n\nQual horário você prefere? (Ex: 9h, 09:00, as 9, 9 da manhã)"
                else:
                    return f"Desculpe, não temos disponibilidade para {data_extraida}. Por favor, escolha um dos dias disponíveis:\n- 15/04/2026\n- 16/04/2026\n- 17/04/2026"
            else:
                return f"Não consegui entender a data. Por favor, escolha um dos dias disponíveis:\n- 15/04/2026\n- 16/04/2026\n- 17/04/2026\n\nVocê pode digitar como: '15/04', 'dia 15', '15 de abril'"
        
        # Passo 4: Aguardando o horário (VERSÃO MELHORADA)
        elif self.passo_consultas == 'aguardando_horario':
            # Extrai o horário da mensagem do usuário
            horario_extraido = self.extrair_horario_da_mensagem(mensagem)
            
            if horario_extraido:
                # Valida se o horário está disponível
                horario_valido = self.validar_horario_disponivel(horario_extraido)
                
                if horario_valido:
                    self.dados_agendamento['horario'] = horario_valido
                    self.passo_consultas = None
                    self.fluxo_atual = None
                    
                    # Confirma o agendamento
                    confirmacao = f"✅ **Agendamento Confirmado!**\n\n"
                    confirmacao += f"Especialidade: {self.dados_agendamento['especialidade'].title()}\n"
                    confirmacao += f"Data: {self.dados_agendamento['data']}\n"
                    confirmacao += f"Horário: {horario_valido}\n\n"
                    confirmacao += f"Um lembrete será enviado por WhatsApp. Algo mais que possamos ajudar?"
                    
                    # Limpa os dados do agendamento
                    self.dados_agendamento = {}
                    
                    return confirmacao
                else:
                    return f"Desculpe, o horário {horario_extraido} não está disponível. Por favor, escolha um dos horários válidos:\n08:00, 09:00, 10:00, 14:00, 15:00, 16:00"
            else:
                return f"Não consegui entender o horário. Por favor, escolha um dos horários disponíveis:\n08:00, 09:00, 10:00, 14:00, 15:00, 16:00\n\nVocê pode digitar como: '9h', '09:00', 'as 9', '9 da manhã'"
        
        return None
            
    def responder(self, mensagem):
        """Método principal de resposta do bot"""
        
        # Se estamos em um fluxo ativo, processa o fluxo específico
        if self.fluxo_atual:
            if self.fluxo_atual == 'suporte':
                return self.processar_suporte(mensagem)
            elif self.fluxo_atual == 'atendente':
                return self.processar_atendente(mensagem)
            elif self.fluxo_atual == 'consultas':
                return self.processar_consultas(mensagem)
        
        # Se não está em fluxo, detecta a intenção
        intencao = self.detectar_intencoes(mensagem)
        
        # Processa cada intenção
        if intencao == 'saudacao':
            return self.respostas.get('respostas_saudacoes', ['Olá! Como posso ajudar?'])[0]
        
        elif intencao == 'despedida':
            return "Obrigado pelo contato! Estamos à disposição. Até mais!"
        
        elif intencao == 'suporte':
            return self.processar_suporte(mensagem)
        
        elif intencao == 'consultas':
            return self.processar_consultas(mensagem)
        
        elif intencao == 'atendente':
            return self.processar_atendente(mensagem)
        
        else:  # desconhecido
            if hasattr(self, 'config') and hasattr(self.config, 'fluxos'):
                return self.config.fluxos.get('inicio', 'Olá! Como posso ajudar?\n1 - Suporte\n2 - Consultas\n3 - Falar com Atendente')
            return 'Olá! Como posso ajudar?\n1 - Suporte\n2 - Consultas\n3 - Falar com Atendente'