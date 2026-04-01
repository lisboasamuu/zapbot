# zapbot
# 🏥 Clínica Life - Chatbot Inteligente

## 📋 Sobre o Projeto

O **Clínica Life Bot** é um chatbot desenvolvido em Python para automatizar o atendimento de uma clínica médica fictícia. Esta é a versão inicial do projeto, construída como base para evoluir para um sistema completo de atendimento via WhatsApp.

### 🎯 Objetivo
- Automatizar o primeiro contato com pacientes
- Agilizar informações sobre consultas, horários e suporte
- Criar uma base escalável para integração com WhatsApp
- Proporcionar uma experiência de atendimento moderna e eficiente

---

## 🚀 Funcionalidades (Versão 1.2)

### ✅ Implementadas
- **Detecção de Intenções**: Identifica automaticamente se o usuário quer:
  - Saudação inicial
  - Suporte técnico
  - Informações sobre consultas
  - Encerrar atendimento
  - Marcar, Agendar e verificar Consultas

- **Respostas Contextuais**: O bot responde de acordo com a intenção identificada

- **Interface via Terminal**: Atendimento funcional diretamente pelo console

- **Sistema de Menus**: Navegação simples por opções numeradas

- **Arquitetura Modular**: Código organizado para facilitar evoluções futuras

### 🔮 Planejadas para próximas versões
- [ ] Banco de dados SQLite para histórico
- [ ] Agendamento real de consultas
- [ ] Integração com WhatsApp
- [ ] API REST para webhooks
- [ ] Painel administrativo

---

## 📁 Nota Versão 1.2
Antes, o bot apenas procurava no input do usuário a data e hora específica da enviada. Por exemplo, quando o bot dizia "horário disponível 09:00h" e o usuário retornava "pode ser as 9" o bot não reconhecia e voltava erro. Sendo assim, utilizamos expressões regulares para ensinarmos ao pythona as diversas formatações de data e hora.