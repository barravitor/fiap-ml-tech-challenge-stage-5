# app/schemas/job_register_schemas.py
from typing import Optional
from pydantic import BaseModel, Field

class BasicInformationSchema(BaseModel):
    job_title: str = Field(..., example="Desenvolvedor Web Pleno / Sênior", description="Titulo da vaga")
    job_external_id: int = Field(..., example=1, description="ID real da vaga")
    # "data_requicisao": "04-05-2021",
    # "limite_esperado_para_contratacao": "00-00-0000",
    # "vaga_sap": "Não",
    # "cliente": "Mann and Sons",
    # "solicitante_cliente": "Cauê Fogaça",
    # "empresa_divisao": "Decision São Paulo",
    # "requisitante": "Maria Laura Nogueira",
    # "analista_responsavel": "Raquel Vieira",
    # "tipo_contratacao": "CLT Full",
    # "prazo_contratacao": "",
    # "objetivo_vaga": "",
    # "prioridade_vaga": "",
    # "origem_vaga": "",
    # "superior_imediato": "Superior Imediato:",
    # "nome": "",
    # "telefone": ""

class ProfileSchema(BaseModel):
    country: str
    state: str
    city: str
    neighborhood: Optional[str] = None
    # "regiao": "",
    # "local_trabalho": "2000",
    # "vaga_especifica_para_pcd": "Não",
    # "faixa_etaria": "De: Até:",
    # "horario_trabalho": "",
    # "nivel profissional": "Sênior",
    # "nivel_academico": "Ensino Superior Completo",
    # "nivel_ingles": "Básico",
    # "nivel_espanhol": "Nenhum",
    # "outro_idioma": "",
    # "areas_atuacao": "TI - Desenvolvimento/Programação-",
    # "principais_atividades": "Graduated or with course of programming logic, with experience in development in ASP, .NET, JAVA, HTML, CSS and also knowlege with Data bases (MySQL, Oracle and SQL+)",
    # "competencia_tecnicas_e_comportamentais": "Desenvolvedor Web (Microsoft .Net).\nconhecimentos Java e PHP desejável.",
    # "habilidades_comportamentais_necessarias": "A mais urgente é de consultor Web (programador backend), se possível enviar candidatos urgente para ela, gostaríamos de selecionar e já fazer o hiring desta posição até sexta agora dia 07/05/2021 ...\n\nTrata-se de uma vaga de substituição interna da TCS por isso que a vaga poderá ser clt tanto por nos como direto pela TCS",
    # "demais_observacoes": "contratação CLT full pela Decision locação remota na Siemens - projeto e as do AMS Tempo de alocação: 5 meses e depois será absorvido pela TCS - Maio a Sep full time horário comercial (8h por dia)",
    # "viagens_requeridas": "Não"

# class beneficios(BaseModel):
#     "valor_venda": "168 -",
#     "valor_compra_1": "Fechado",
#     "valor_compra_2": ""

class JobSchema(BaseModel):
    id: Optional[int]
    basicInformation: BasicInformationSchema
    profile: ProfileSchema

    class Config:
        from_attributes = True