# Gera a chave hash para a senha 'bot'
HASHED_PASSWORD=$(tor --hash-password bot | tail -n 1)

# Verifica se o comando foi executado com sucesso
if [ $? -eq 0 ]; then
    # Adiciona as configurações ao arquivo torrc
    {
        echo "ControlPort 9051"
        echo "CookieAuthentication 1"
        echo "HashedControlPassword $HASHED_PASSWORD"
    } | sudo tee -a /etc/tor/torrc > /dev/null

    echo "As configurações foram adicionadas ao arquivo /etc/tor/torrc com sucesso."
else
    echo "Falha ao gerar a chave hash."
    exit 1
fi
