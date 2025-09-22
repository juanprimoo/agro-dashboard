import sidrapy
import pandas as pd

def get_lavouras_permanentes_por_estado():
   
    data = sidrapy.get_table(
        table_code="1613",
        territorial_level="3",
        ibge_territorial_code="all",
        classifications={"82": "all"},
        period="last 1",
        header="n",
        format="pandas",
    )

    data = data.rename(
        columns={
            "NN": "nivel_territorial",
            "MC": "codigo_unidade_medida",
            "MN": "unidade_medida",
            "V": "valor",
            "D1C": "codigo_estado",
            "D1N": "estado",
            "D2C": "ano",
            "D3C": "id_produto",
            "D3N": "descricao_produto",
            "D4C": "variavel_codigo",
            "D4N": "variavel_descricao",
        }
    )

    data = data[
        [
            "codigo_estado",
            "estado",
            "ano",
            "id_produto",
            "descricao_produto",
            "variavel_codigo",
            "valor",
            "unidade_medida",
        ]
    ]

    def parse_valor(v):
        try:
            return float(str(v).replace(",", "."))
        except:
            return 0

    data["valor"] = data["valor"].apply(parse_valor)

    pivot = data.pivot_table(
        index=["codigo_estado", "estado", "ano", "id_produto", "descricao_produto"],
        columns="variavel_codigo",
        values="valor",
        aggfunc="first",
    ).reset_index()

    pivot = pivot.rename(
        columns={
            "2313": "area_destinada",
            "216": "area_colhida",
            "214": "quantidade_produzida",
            "112": "rendimento",
            "215": "valor_producao",
        }
    )

    pivot = pivot.fillna(0)

    pivot["unidade_medida"] = pivot["id_produto"].map(
        data.drop_duplicates(subset=["id_produto"]).set_index("id_produto")[
            "unidade_medida"
        ]
    )
   
   
    resultado_final = []
    for (uf_id, uf_nome, ano), grupo in pivot.groupby(
        ["codigo_estado", "estado", "ano"]
    ):
        culturas = grupo[
            [
                "id_produto",
                "descricao_produto",
                "area_destinada",
                "area_colhida",
                "quantidade_produzida",
                "rendimento",
                "valor_producao",
                "unidade_medida",
            ]
        ].to_dict(orient="records")

        total_valor = grupo["valor_producao"].sum()

        estado_dict = {
            "id_estado": uf_id,
            "estado": uf_nome,
            "ano": ano,
            "total": {"valor_producao": total_valor},
            "cultura": culturas,
        }
        resultado_final.append(estado_dict)

    return resultado_final
