'''Nesta classe config deifinimos todas as funções que vão se relacionar com a db'''
class Config:
    #alocagem das variaveis base, principais do consumo do bot

    EMPRESA_NOME = 'Clinca Life'
    HORARIO_FUNCIONAMENTO = 'Segunda a Sexta 06h as 22h'
    TELEFONE_SUPORTE = '(19) 99912-3456'
    #FLUXOS DO BOT
    fluxos = {
        'inicio': 'Olá! Seja bem vindo à Clinica Life! Como posso te ajudar?\n1 - Suporte\n2 - Consultas\n 3 - Falar com Atendente  ',
        'suporte': 'Descreva o seu problema em poucas palavras:',
        'consultas': 'Deseja marcar consulta, ver agendamentos ou remarcar?',
        'atendente': 'Certo, estou transferindo você para um atendente humano. Em breve retomamos o contato.'
    }

