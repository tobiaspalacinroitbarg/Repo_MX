# Import
import pandas as pd
from cargar import insertar_informe_base

# Diccionario
diccionario_columnas:dict[dict[str,str]]={"org":{'Categoria__c':'categoria','CLUNI__c':'cluni','BillingStreet':'domicilio','Entidad_Federativa__c':'entidad_fed','Fecha_de_constituci_n__c':'F_constit','Representantes_legales__c':'rep_legales','Tipo_de_fundaci_n__c':'tipo','Fecha_de_inscripci_n_CLUNI__c':'F_insc_cluni','Fecha_de_oficio__c':'f_oficio','Figura_Jur_dica__c':'figura_jur_cluni','Municipio__c':'localidad','Misi_n__c':'mision','Name':'r_social','RFC__c':'rfc','Rubro_Autorizado__c':'rubro_aut','Subcategoria__c':'subcategoria','Tel_fono_s__c':'telefono','Ultimo_a_o_Informe_de_Transparencia__c':'ult_anio_itr','Ultimo_a_o_RDA__c':'ult_anio_rda','Ultimo_a_o_Directorio_SAT__c':'ult_anio_sat','Visi_n__c':'vision','Website':'web','Acreditamiento__c':'oficio','BillingPostalCode':'codigo_postal','Correos_electr_nicos__c':'correo_electronico','Representantes_legales__c':'rep_legales'},"itr_ctrl_donat":{'Informe_de_transparencia__c':'id_itr','Id_de_donativo_en_especie__c':'id_donat_esp','Bienes_recibidos__c':'bienes_rec','Cantidad_recibida__c':'q_rec','Cant_cuotas_de_recuperaci_n__c':'q_cuotas_recup','Monto_de_Cuotas_de_recuperaci_n__c':'mto_cuotas_recup','Cantidad_en_destrucci_n__c':'cant_destruc','Remanente__c':'remanente'},"itr_donat_otorgados":{'Beneficiario__c':'benef','Monto_total__c':'mto_total','RFC_del_donante__c':'rfc_donante','RFC_de_la_donataria__c':'rfc_donataria','Informe_de_transparencia__c':'id_itr','Monto_efectivo__c':'mto_efe','Monto_especie__c':'mto_esp'},"itr_gastos":{'Monto_total__c':'mto_total','Concepto__c':'concepto','Especifique_concepto_de_actividad__c':'detalle_concepto','Informe_de_transparencia__c':'id_itr','Monto_nacional_operaci_n__c':'mto_nac_ope','Monto_nacional_administrativo__c':'mto_nac_adm','Monto_extranjero_operaci_n__c':'mto_ext_ope','Monto_extranjero_administrativo__c':'mto_ext_adm'},"itr":{'Activo__c':'activo','Categoria_principal__c':'categoria_ppal','Socio_o_Asociado__c':'socios_asoc','Autorizaci_n_extranjero__c':'aut_ext','Capital__c':'capital','Actividades_legislativas__c':'act_legislativas','Entidad_federativa__c':'entidad_fed','Estatus__c':'estatus','Gastos_administrativos__c':'gastos_adm','Gastos_operativos__c':'gastos_ope','Sitio_web__c':'web','Gastos_representaci_n__c':'gastos_rep','Id':'id','RFC_c_c':'rfc','Misi_n__c':'mision','A_o_de_autorizaci_n__c':'anio_autorizacion','Pasivo__c':'pasivo','Patrimonio_c__c':'patrimonio','A_o_del_informe__c':'anio_informe','Monto_total_plantilla_laboral__c':'mto_plant_laboral','Situaci_n_Fiscal__c':'sit_fiscal','Plantilla_de_voluntarios__c':'plant_voluntarios','Plantilla_laboral__c':'plant_laboral','Visi_n__c':'vision','Rubros_autorizados__c':'rubros_aut'},"itr_ing_donat_rec":{'Tipo_de_ingreso__c':'tipo_ingreso','Concepto_otros_ingresos__c':'concepto','Donativo_en_especie__c':'donat_esp','Monto__c':'monto','Informe_de_transparencia__c':'id_itr','Tipo_de_donante__c':'tipo_donante'},"itr_inv_finan":{'Informe_de_transparencia__c':'id_itr','Concepto__c':'concepto','Monto_extranjero__c':'mto_ext','Monto_nacional__c':'mto_nac'},"itr_nec_atend":{'Concepto__c':'concepto','Necesidades_atendidas__c':'num_benef','Entidad_federativa__c':'entidad_fed','Municipio__c':'municipio','Informe_de_transparencia__c':'id_itr','Sector_beneficiado__c':'sect_benef','Monto__c':'monto'},"itr_org_gob":{'Informe_de_transparencia__c':'id_itr','Nombre_integrante__c':'nombre','Puesto__c':'puesto','Monto_salario__c':'salario'},"itr_sect_benef":{'Informe_de_transparencia__c':'id_itr','ID_del_donativo_en_especie__c':'id_donat_esp','Sector_beneficiado__c':'sect_benef','Cantidad__c':'cant'},"itr_transm_patr":{'Informe_de_transparencia__c':'id_itr','Monto_efectivo__c':'mto_efe','Monto_especie__c':'mto_esp','Raz_n_social_destinatario__c':'raz_soc_dest','RFC_del_donante__c':'rfc_donante','RFC_de_la_donataria__c':'rfc_donataria'},"rda":{'A_o_del_reporte__c':'anio_reporte','Donativos_en_efectivo_extranjeros__c':'donat_ef_ext','Donativos_en_efectivo_locales__c':'donat_ef_local','Donativos_en_especie_extranjeros__c':'donat_esp_ext','Donativos_en_especie_locales__c':'donat_esp_loc','Organizaci_n__c':'rfc','Arrendamiento_de_Bienes__c':'ing_arrend','Dividendos__c':'ing_div','Intereses_devengados__c':'ing_inter_dev','Otros_Ingresos_Generados__c':'ing_otros','Regal_as__c':'ing_regalias','Sueldos_Salarios_y_Gastos_Relacionados__c':'sueldos_salarios_gastos','Aportaciones_al_SAT_Infonavit_y_jub__c':'aport_infonavit_jub','Cuotas_del_IMSS__c':'cuotas_imss','Gastos_de_Administraci_n__c':'gastos_adm_leg','Gasto_de_Operaci_n__c':'gastos_ope_leg'},"dir_sat":{'Organizaci_n__c':'rfc','Tel_fono_s__c':'telefono','Correos_electr_nicos__c':'correo_electronico','Representantes_Legales__c':'rep_legales','Domicilio_fiscal__c':'domicilio','Entidad_federativa__c':'entidad_fed','Rubro_autorizado_c':'rubro_aut','Fecha_de_inscripci_n__c':'f_inscr','Raz_n_social__c':'r_social','Figura_juridica__c':'fig_jur_cluni','Edad__c':'edad','Fecha_de_oficio__c':'f_oficio','A_o_del_directorio__c':'anio_directorio'}}

# Lista de tablas
tablas:list[str] = ["dir_sat","org","itr","itr_ctrl_donat","itr_donat_otorgados","itr_gastos","itr_ing_donat_rec","itr_inv_finan","itr_nec_atend","itr_org_gob","itr_sect_benef","itr_transm_patr","rda","dir_sat"]

for tabla in tablas:
    # Leer DataFrame
    df:pd.DataFrame = pd.read_excel(f"./bases_a_subir/base_vieja/{tabla}.xlsx")
    # Quedarse solo con esas columnas
    df = df[[column for column in df.columns if column in list(diccionario_columnas[tabla].keys())]]  
    # Renombrar in
    df = df.rename(diccionario_columnas[tabla], axis='columns')
    # Convertir NaN y otros valores que dan errores en caso de coincidir tabla
    if tabla == "org":
        df["F_constit"] = df['F_constit'].where(pd.notna(df["F_constit"]),None)
        df["F_insc_cluni"] = df['F_insc_cluni'].where(pd.notna(df["F_insc_cluni"]),None)
        df["ult_anio_rda"] = df["ult_anio_rda"].fillna(0)
        df["ult_anio_sat"] = df["ult_anio_sat"].fillna(0)
        df["ult_anio_itr"] = df["ult_anio_itr"].fillna(0)
    elif tabla == "itr":
        df.loc[df["aut_ext"]=="Si","aut_ext"] = True
        df.loc[df["aut_ext"]=="No","aut_ext"] = False
        df["aut_ext"].fillna(False,inplace=True)
        df["plant_voluntarios"].fillna(0,inplace=True)
        df["anio_autorizacion"].fillna(0,inplace=True)
    elif tabla.split("_")[0] == "itr":
        if tabla== 'itr_inv_finan':
            df["mto_nac"] = df["mto_nac"].round().astype(int)
            df["mto_ext"] = df["mto_ext"].round().astype(int)
        elif tabla == "itr_nec_atend":
            df["monto"].fillna(0,inplace=True)
            df["monto"] = df["monto"].round().astype(int)
    elif tabla == 'dir_sat':
        df['anio_directorio'].fillna(0,inplace=True)
        df['edad'].fillna(0,inplace=True)
        
    # Cargar
    insertar_informe_base(df, tabla)
    # Print
    print(f"({tabla})")
