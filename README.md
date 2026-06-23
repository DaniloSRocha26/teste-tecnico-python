# Desafio b2bflow - Estágio Python

Script que busca contatos no Supabase e envia pra cada um, via Z-API, a mensagem:

> Olá, `<nome_contato>` tudo bem com você?

## 1 - Setup da tabela no Supabase

1. Crie um projeto no Supabase (free tier serve).
2. Crie uma tabela `contatos` com essas colunas:
   - `id` e `created_at` (deixa no padrão)
   - `nome` (text)
   - `telefone` (text) - formato `5511999999999`, ou seja código do país + DDD + número, sem espaço, sem `+`, sem nada. É o formato que a Z-API espera.
3. Cadastre de 1 a 3 contatos pra teste.
4. Importante: O Supabase tem uma configuração padrão de bloquear as leituras via API (RLS). Então vá em **Authentication → Policies** e crie uma policy de `SELECT` para liberar a leitura pra `anon key` na tabela `contatos`. Sem isso a API vai devolver `[]`, sem nenhum erro.
5. Pegue a **Project URL** e a **anon/public key** em **Project Settings → API** para o próximo passo.

## 2 - Variáveis de ambiente (.env)

Copie o `.env.example` pra `.env`:

```bash
cp .env.example .env
```

E preencha:

- `SUPABASE_URL` - a URL do projeto, sem o `/rest/v1/` no final
- `SUPABASE_KEY` - a anon/public key
- `ZAPI_INSTANCE_ID` - ID da instância da Z-API
- `ZAPI_TOKEN` - token de envio da instância
- `ZAPI_CLIENT_TOKEN` - esse é o "Token de Segurança da Conta", que fica em outro lugar do painel da Z-API (não confundir com o token da instância). Sem ele a API responde com erro 400 dizendo que o client-token não tá configurado.

O `.env` nunca irá pro git (já está no `.gitignore`).

## 3 - Como rodar

```bash
python -m venv venv
venv\Scripts\activate        # Para Windows
source venv/bin/activate     # Para Linux/Mac

pip install -r requirements.txt

python main.py
```

Pronto, ele irá buscar os contatos no Supabase e vai disparar as mensagens pela Z-API, logando o resultado de cada envio no terminal.
