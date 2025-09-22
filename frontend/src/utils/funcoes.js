export function formatarMoeda(valor) {
    return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL"}).format(valor);
}

export function formatarArea(valor, unidade = "ha") {
    return `${valor} ${unidade}`;
}

export function formatarInteiro(valor) {
    return Math.round(valor || 0);
}

export function getEstados() {
  return estados;
}

export function getEstadoPorId(id) {
  return estados.find(e => e.id.toString() === id.toString()) || null;
}