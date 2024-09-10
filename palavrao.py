const { createBot, createProvider, createFlow, addKeyword, JsonDB } = require('@builderbot/bot')
const { BaileysProvider } = require('@builderbot/bot')

// Lista de palavrões
const palavroes = ['pau', 'pica', 'caralho'];

// Função que verifica se a mensagem contém um palavrão
const containsPalavrao = (message) => {
    return palavroes.some(palavrao => message.toLowerCase().includes(palavrao));
};

// Fluxo para contar palavrões e salvar no banco de dados
const palavroesFlow = addKeyword(palavroes).addAction(async (ctx, { flowDynamic, provider, db }) => {
    const groupId = ctx.groupId || ctx.from; // ID do grupo
    const senderName = ctx.pushName; // Nome do usuário
    const message = ctx.body; // Mensagem recebida

    if (containsPalavrao(message)) {
        // Busca o grupo no banco de dados
        let groupData = db.get(groupId) || {};
        
        // Busca o usuário dentro do grupo no banco de dados
        const userData = groupData[senderName] || { count: 0 };

        // Incrementa a contagem de palavrões
        userData.count += 1;
        
        // Atualiza os dados do grupo e do usuário
        groupData[senderName] = userData;
        db.set(groupId, groupData);

        await flowDynamic(`Calma ${senderName}, você já falou palavrão ${userData.count} vezes!`);
    }
});

// Inicialização do bot
const main = async () => {
    const adapterDB = new JsonDB(); // Usando JsonDB para persistir dados
    const adapterFlow = createFlow([welcomeFlow, palavroesFlow]);
    const adapterProvider = createProvider(BaileysProvider);

    adapterProvider.initHttpServer(3000);

    await createBot({
        flow: adapterFlow,
        provider: adapterProvider,
        database: adapterDB,
    });
};

main();
