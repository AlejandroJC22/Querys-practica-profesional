import pandas as pd

arch1 = pd.read_csv('DATA FUENTE.txt', sep=',', header = 0, dtype=str, low_memory=False)
arch2 = pd.read_csv('DATA SIEBEL.txt', sep=',', header = 0, dtype=str, low_memory=False)

arch1['CODIGO'] = arch1['CODIGO'].str.strip()
arch2['CODIGO'] = arch2['CODIGO'].str.strip()

arch1['NUMERO_PRODUCTO'] = arch1['NUMERO_PRODUCTO'].str.strip()
arch2['NUMERO_PRODUCTO'] = arch2['NUMERO_PRODUCTO'].str.strip()

arch1['ESTADO'] = arch1['ESTADO'].str.strip()
arch2['ESTADO'] = arch2['ESTADO'].str.strip()

no_siebel = pd.merge(arch1, arch2, how = 'left', on = ['CODIGO','NUMERO_PRODUCTO','ESTADO'], indicator = True)
productos_no_siebel = no_siebel[no_siebel['_merge'] == 'left_only']

conteo_no_siebel = productos_no_siebel.shape[0]

estado_diferente = pd.merge(arch1, arch2, how = 'inner', on = ['CODIGO','NOMBRE','NUMERO_PRODUCTO'],  suffixes = ('_MDM','_SIEBEL'))
productos_estado_diferente = estado_diferente[estado_diferente['ESTADO_MDM'] != estado_diferente['ESTADO_SIEBEL']]

conteo_estado_diferente = productos_estado_diferente.shape[0]

nombre_diferente = pd.merge(arch1, arch2, how = 'inner', on = ['CODIGO','NUMERO_PRODUCTO','ESTADO'],  suffixes = ('_MDM','_SIEBEL'))
productos_nombre_diferente = nombre_diferente[nombre_diferente['NOMBRE_MDM'] != nombre_diferente['NOMBRE_SIEBEL']]

codigo_diferente = pd.merge(arch1, arch2, how = 'inner', on = ['NOMBRE','NUMERO_PRODUCTO','ESTADO'],  suffixes = ('_MDM','_SIEBEL'))
productos_codigo_diferente = codigo_diferente[codigo_diferente['CODIGO_MDM'] != codigo_diferente['CODIGO_SIEBEL']]

conteo_codigo_diferente = productos_codigo_diferente.shape[0]


with pd.ExcelWriter('RESULTADOS.xlsx') as writer:
    pd.DataFrame({
        'Total productos no siebel': [conteo_no_siebel],
        'Total productos con estado diferente': [conteo_estado_diferente],
         'Total productos con diferente codigo': [conteo_codigo_diferente]
        }).to_excel(writer, sheet_name='RESUMEN', index=False)

    productos_no_siebel[['CODIGO','NUMERO_PRODUCTO','ESTADO']].to_excel(writer, sheet_name = 'No siebel', index=False)

    productos_estado_diferente[['CODIGO','NOMBRE','NUMERO_PRODUCTO','ESTADO_MDM','ESTADO_SIEBEL']].to_excel(writer, sheet_name = 'Estado diferente', index=False)

    productos_nombre_diferente[['CODIGO','NOMBRE_MDM','NOMBRE_SIEBEL','NUMERO_PRODUCTO','ESTADO']].to_excel(writer, sheet_name = 'Nombre diferente', index=False)

    productos_codigo_diferente[['CODIGO_MDM','CODIGO_SIEBEL','NOMBRE','NUMERO_PRODUCTO','ESTADO']].to_excel(writer, sheet_name = 'Codigo diferente', index=False)
    
    
print('Resultados obtenidos. Operación terminada')
