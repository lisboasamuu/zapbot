from chatbot.core import ChatBot

def main():
    chatbot = ChatBot()
    print("="*80)
    print(f'             🩺❤️  Atendimento Virtual - Clinica Life')
    print("               Digite 'sair' para encerrar o atendimento")
    print("="*80)
    print()

    print(chatbot.responder('Olá, como posso te ajudar?'))
    while True:
        try:
            mensagem = input("\nDigite: ").strip()
            if mensagem.lower() in ['sair', 'exit', 'quit', 'encerrar']:
                print(f'🩺❤️  Atendimento Virtual: Obrigado pelo contato. Até logo!')
                break
            if mensagem:
                resposta = chatbot.responder(mensagem)
                print(f'🩺❤️  Atendimento Virtual: {resposta}')
        except KeyboardInterrupt:
            print(f'🩺❤️  Atendimento Virtual: Obrigado pelo contato. Até logo!')
            break
        except Exception as e:
            print(f"❌ erro {e}")
        if any(despedida in mensagem for despedida in ("obrigado", "valeu", "obg", "vlw", "tchau", "até mais")):
            break
        if resposta == 'Entendo que precisa de suporte. Vou direcionar a uma pessoa de nossa equipe\nAguarde um momento, por favor.':
            print("\nUm de nossos atendentes irá assumir a conversa. Aguarde um momento, por favor.")
            break

if __name__ == "__main__":
    main()