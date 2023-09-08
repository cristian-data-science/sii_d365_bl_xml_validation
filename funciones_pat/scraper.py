import time
#import unittest
from time import sleep
from datetime import date, timedelta
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import os
import pymssql



class funciones_globales():
    
    def __init__(self, driver):
        self.driver = driver

    def login_blue(self, url, userb, passwb):
        self.driver.get(url)
        driver = self.driver

        print("### Iniciando sesión en Blueline ###")
        sleep(1)
        user = driver.find_element(By.XPATH, value= '/html/body/div/div[1]/form/input[2]')
        user.send_keys(userb) 
        #sleep(1)
        passw = driver.find_element(By.XPATH, value= '/html/body/div/div[1]/form/input[3]')
        passw.send_keys(passwb)
        sleep(1)
        subm = driver.find_element(By.XPATH, value= '/html/body/div/div[1]/form/input[4]')
        subm.click()
        sleep(1)


    def dte_emitidos(self, url):
        self.driver.get(url)
        driver = self.driver
        #dte_emitidos = driver.find_element(By.XPATH, value='//*[@id="DTE"]/tbody/tr[1]/td/table')
        #dte_emitidos.click()
      
        ini = date.today() - timedelta(30)
        ini = str(ini)
        fin = date.today()
        fin = str(fin)
        sleep(1)
        ini_box = driver.find_element(By.XPATH, value ='//*[@id="FCHDESDE"]')
        ini_box.click()
        ini_box.send_keys(ini)
        ini_box.send_keys(Keys.ENTER)
        

        final_box = driver.find_element(By.XPATH, value ='//*[@id="FCHHASTA"]')
        final_box.send_keys(fin)
        #final_box.click()

        sleep(1)
        buscar = driver.find_element(By.XPATH, value= '/html/body/fieldset/form/table[3]/tbody/tr[3]/td[1]/button') 
        buscar.click()
        WebDriverWait(self.driver, 60).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        download = driver.find_element(By.XPATH, value= '/html/body/fieldset/form/table[3]/tbody/tr[3]/td[2]/a').click()
        sleep(1)

        nombre_xls = "Reporte.xls"
        nuevo_nombre_csv = "blueline_data.csv"
        if os.path.exists(nombre_xls):
            # Lee el archivo XLS utilizando pandas
            df = pd.read_excel(nombre_xls)

            # Guarda el DataFrame como un archivo CSV
            df.to_csv(nuevo_nombre_csv, index=False)

            # Renombra el archivo CSV
            os.rename(nuevo_nombre_csv, "blueline_data.csv")

            print(f"El archivo {nombre_xls} se ha convertido a {nuevo_nombre_csv} y se ha renombrado.")
        else:
            print(f"El archivo {nombre_xls} no existe.")


    def login_extract_sii(self, url, rut, pass_rut):
        print("### Accediendo al SII y extrayendo los datos ###")
        self.driver.get(url)
        driver = self.driver

        sleep(1)
        user = driver.find_element(By.XPATH, value= '//*[@id="rutcntr"]')
        user.send_keys(rut) 
        passw = driver.find_element(By.XPATH, value= '//*[@id="clave"]')
        passw.send_keys(pass_rut)
        sleep(1)
        subm = driver.find_element(By.XPATH, value= '//*[@id="bt_ingresar"]')
        subm.click()
        sleep(1)

        driver.get('https://www4.sii.cl/consdcvinternetui/#/index')
        sleep(1)

        consulta_mes = driver.find_element(By.XPATH, value='//*[@id="my-wrapper"]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/form/div[3]/button')
        consulta_mes.click()
        venta = driver.find_element(By.XPATH, value='//*[@id="my-wrapper"]/div[2]/div[1]/div[1]/div/div[2]/ul/li[2]/a')
        venta.click()

        # Localiza la tabla por su clase CSS
        tabla = driver.find_element(By.XPATH, "//table[@class='table table-sm ng-scope']")

        # Encuentra todas las filas en el cuerpo de la tabla
        filas = tabla.find_elements(By.XPATH, ".//tbody/tr")

        # Crear una lista de listas para almacenar los datos de la tabla
        datos_tabla = []

        for fila in filas:
            # Encuentra todas las celdas (td) en la fila
            celdas = fila.find_elements(By.TAG_NAME, "td")
            # Obtén el texto de cada celda y agrégalo a la lista de datos
            fila_datos = [celda.text for celda in celdas]
            datos_tabla.append(fila_datos)

        # Crea un DataFrame de Pandas a partir de los datos de la tabla
        dash_sii = pd.DataFrame(datos_tabla, columns=["Tipo Documento", "Total Documentos", "Monto Exento", "Monto Neto", "Monto IVA", "Monto Total"])
        print(dash_sii)

        # Obtén el directorio actual de trabajo
        directorio_actual = os.getcwd()

        # Lista todos los archivos en el directorio actual
        archivos = os.listdir(directorio_actual)

        # Itera sobre la lista de archivos y elimina los que tengan extensión .csv
        for archivo in archivos:
            if archivo.endswith(".csv"):
                archivo_completo = os.path.join(directorio_actual, archivo)
                os.remove(archivo_completo)
                print(f"Archivo eliminado: {archivo_completo}")

        sleep(1)

        file_download = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[4]/div[1]/div[2]/button')
        file_download.click()

        sleep(5)

        descargas_folder = "./"
        # Obtiene la lista de archivos en la carpeta de descargas
        archivos_en_carpeta = os.listdir(descargas_folder)

        # Encuentra el último archivo descargado
        archivo_descargado = max(archivos_en_carpeta, key=os.path.getctime)

        # Especifica el nuevo nombre del archivo
        nuevo_nombre = "sii_data.csv"

        # Ruta completa del archivo descargado
        archivo_descargado_completo = os.path.join(descargas_folder, archivo_descargado)

        # Ruta completa con el nuevo nombre
        archivo_nuevo = os.path.join(descargas_folder, nuevo_nombre)

        # Renombra el archivo descargado con el nuevo nombre
        os.rename(archivo_descargado_completo, archivo_nuevo)
        dash_sii.to_csv('dash_sii.csv', encoding='utf-8')




    def clean_cross_data(self):
        print("### Preprocesando la data ###")    
        
        sii_data = pd.read_csv('sii_data.csv', delimiter=';', index_col=None)

        sii_data = sii_data.drop_duplicates()


        nombres_columna = ['Tipo Doc', 'Tipo Venta', 'Rut cliente', 'Razon Social', 'Folio', 'Fecha Docto', 'Fecha Recepcion',
                            'Fecha Acuse Recibo', 'Fecha Reclamo', 'Monto Exento', 'Monto Neto', 'Monto IVA', 'Monto total',
                            'IVA Retenido Total', 'IVA Retenido Parcial', 'IVA no retenido', 'IVA propio', 'IVA Terceros',
                            'RUT Emisor Liquid. Factura', 'Neto Comision Liquid. Factura', 'Exento Comision Liquid. Factura',
                            'IVA Comision Liquid. Factura', 'IVA fuera de plazo', 'Tipo Docto. Referencia', 'Folio Docto. Referencia',
                            'Num. Ident. Receptor Extranjero', 'Nacionalidad Receptor Extranjero', 'Credito empresa constructora',
                            'Impto. Zona Franca (Ley 18211)', 'Garantia Dep. Envases', 'Indicador Venta sin Costo',
                            'Indicador Servicio Periodico', 'Monto No facturable', 'Total Monto Periodo', 'Venta Pasajes Transporte Nacional',
                            'Venta Pasajes Transporte Internacional', 'Numero Interno', 'Codigo Sucursal', 'NCE o NDE sobre Fact. de Compra',
                            'Codigo Otro Imp.', 'Valor Otro Imp.', 'Tasa Otro Imp.', 'Nro']

        sii_data.columns = nombres_columna
        sii_data = sii_data[['Tipo Doc', 'Folio', 'Rut cliente', 'Fecha Docto', 'Monto Neto', 'Monto total']]

        sii_data['Tipo Doc'] = sii_data['Tipo Doc'].astype(str)
        sii_data['Folio'] = sii_data['Folio'].astype(str)
        sii_data['factura'] = sii_data['Tipo Doc'] + '-' + sii_data['Folio']

        sii_data.to_csv("sii_data.csv")
        
       
    





        

    def sql_cross(self, server, username, password, database):
        print("### Cruzando datos de BlueLine contra ERP ###")
        conn = pymssql.connect(server, username, password, database)
        cursor = conn.cursor(as_dict=True)

        cursor.execute("""
                        SELECT 
                            SALESORDERNUMBER, 
                            INVOICENUMBER, 
                            INVOICEDATE, 
                            TOTALTAXAMOUNT, 
                            TOTALINVOICEAMOUNT, 
                            INVOICECUSTOMERACCOUNTNUMBER AS RUT_CLIENTE,
                            ABS(TOTALINVOICEAMOUNT - TOTALTAXAMOUNT) AS NETOABS
                        FROM SalesInvoiceHeaderV2Staging 
                        WHERE 
                        INVOICENUMBER NOT LIKE '39%' and
                        INVOICEDATE BETWEEN GETDATE() - 60 AND GETDATE()
                        """)
        df_sales_invoice = pd.DataFrame(cursor.fetchall())

        df_sales_invoice.to_csv("sql_data.csv", encoding='utf-8')
        cursor.close()
        conn.close()

    
















        """val = "next"
        x=0
        pagina = 1
        while val == "next" :
            try:

                table = driver.find_elements(By.XPATH, value='//*[@id="ExportarExcel"]/tbody')
                datos = [linea.text for linea in table]
                print(f"################# página: {pagina} ######################")
                print(datos)
                
                next_button = driver.find_elements(By.XPATH, value='/html/body/div[1]/a[*]')
                next_button[x].click()
                pagina = pagina + 1
                x=1
                    #print(len(n))
                #sleep(2)
           
            except IndexError as e:
                print(e)
                print("index error controlado")
                print("No hay página siguiente")
                val = "No_next" """