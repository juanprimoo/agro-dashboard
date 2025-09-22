export function selectEstado(dados, id_estado) {
    if (!id_estado) return null; // <- retorna null para nível nacional
    return dados.find(e => e.id_estado.toString() === id_estado.toString()) || null;
}

export function calcularNacional(dados) {
    const produtosMap = {};
    dados.forEach((estado) => {
        estado.cultura.slice(1).forEach((cultura) => {
            if (cultura.valor_producao === 0) return;
            if (!produtosMap[cultura.descricao_produto]) {
                produtosMap[cultura.descricao_produto] = {
                    ...cultura
                };
            } else {
                const p = produtosMap[cultura.descricao_produto];
                p.area_destinada += cultura.area_destinada;
                p.area_colhida += cultura.area_colhida;
                p.quantidade_produzida += cultura.quantidade_produzida;
                p.rendimento += cultura.rendimento;
                p.valor_producao += cultura.valor_producao;
            }
        });
    });
    return Object.values(produtosMap);
}

export function maiorRendimento(lista) {
    return lista.reduce((max, item) => (!item.rendimento ? max : (item.rendimento > (max?.rendimento || 0) ? item : max)), null);
}

export function maiorValor(lista) {
    return lista.reduce((max, item) => (!item.valor_producao ? max : (item.valor_producao > (max?.valor_producao || 0) ? item : max)), null);
}