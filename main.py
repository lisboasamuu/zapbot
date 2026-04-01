from chatbot.core import ChatBot

def main():
    chatbot = ChatBot()
    print("="*80)
    print(f'             🩺❤️  Atendimento Virtual - Clinica Life')
    print("               Digite 'sair' para encerrar o atendimento")
    print("="*80)
    print()

    # Inicia a conversa com uma saudação
    resposta_inicial = chatbot.responder('Olá')
    print(f'🩺❤️  Atendimento Virtual: {resposta_inicial}')
    
    while True:
        try:
            mensagem = input("\nVocê: ").strip()
            
            # Verifica se o usuário quer sair
            if mensagem.lower() in ['sair', 'exit', 'quit', 'encerrar']:
                print(f'🩺❤️  Atendimento Virtual: Obrigado pelo contato. Até logo!')
                break
            
            # Se a mensagem não estiver vazia, processa
            if mensagem:
                resposta = chatbot.responder(mensagem)
                print(f'🩺❤️  Atendimento Virtual: {resposta}')
                
                # Verifica se o bot redirecionou para suporte humano
                if 'Vou direcionar a uma pessoa de nossa equipe' in resposta:
                    print("\n👨‍⚕️ Um de nossos atendentes irá assumir a conversa. Aguarde um momento, por favor.")
                    break
                    
                # Verifica se a conversa foi encerrada naturalmente
                if 'Até mais' in resposta or 'até logo' in resposta.lower():
                    break
                    
        except KeyboardInterrupt:
            print(f'\n🩺❤️  Atendimento Virtual: Obrigado pelo contato. Até logo!')
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            print("Por favor, tente novamente ou digite 'sair' para encerrar.")

if __name__ == "__main__":
    main()