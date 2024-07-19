import pandas as pd

# Función para asegurar que el formato de duración sea correcto
def format_duration(duration):
    if pd.isna(duration) or duration == "":
        return "00:00:00"
    parts = duration.split(":")
    if len(parts) == 2:
        return f"00:{parts[0]:0>2}:{parts[1]:0>2}"
    elif len(parts) == 3:
        return f"{parts[0]:0>2}:{parts[1]:0>2}:{parts[2]:0>2}"
    else:
        return "00:00:00"

# Cargar los archivos CSV
kixie_file_path = 'kixie.csv'
vonage_file_path = 'vonage.csv'

kixie_df = pd.read_csv(kixie_file_path)
vonage_df = pd.read_csv(vonage_file_path)

# Formatear las columnas 'Date' en kixie_df
kixie_df['Date'] = pd.to_datetime(kixie_df['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')

# Asegurar que la columna 'Duration' esté en el formato correcto
kixie_df['Duration'] = kixie_df['Duration'].apply(format_duration)

# Agregar una columna formateada 'date_time_formated' en vonage_df y renombrar columnas
vonage_df['date_time_formated'] = pd.to_datetime(vonage_df['Date/Time']).dt.strftime('%Y-%m-%d %H:%M:%S')
vonage_df = vonage_df.rename(columns={
    'Call ID': 'call_id',
    'To': 'tto',
    'From': 'tfrom',
    'Date/Time': 'date_time'
})

# Guardar los dataframes modificados en un archivo Excel con pestañas separadas
output_file_path = 'calls_formatted.xlsx'
with pd.ExcelWriter(output_file_path) as writer:
    kixie_df.to_excel(writer, sheet_name='kixie', index=False)
    vonage_df.to_excel(writer, sheet_name='vonage', index=False)

print(output_file_path)
