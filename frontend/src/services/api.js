export async function getDadosLavourasPermanentes() {
    const res = await fetch("http://localhost:8000/permanentesEstado/permanentes")
    if (!res.ok) throw new Error("Falha ao buscar dados")
    return await res.json()
}