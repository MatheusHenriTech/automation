from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

servico = Service(ChromeDriverManager().install())

navegador = webdriver.Chrome(service=servico)

navegador.get("https://dlp.hashtagtreinamentos.com/python/minicurso/minicurso-automacao/inscricao?curso=python&origemurl=hashtag_yt_org_minipython_videoselenium&_gl=1*1j0wzyz*_gcl_au*NzI0MDUwMDQ3LjE3Nzg2MTIzNTI.*_ga*MTUyMTA3Mzg1MC4xNzc4NjEyMzUy*_ga_8VXCNB69RS*czE3Nzg2MTIzNTAkbzEkZzEkdDE3Nzg2MTI0MDYkajQkbDAkaDAkZFNuZTZHWWVzZjRXczIzYjFCU3N4Tmo5c244aHMwVGlqV3c.*_fplc*R3RSeHd3TGxyJTJGMDQ1YndPRTVzMERHQXVNYkZVdUNTd1BkV0hMajRxRkt6VzJwSWhnVWF0eEI1dmd3YkowSWtjVyUyQjJWJTJCWGY5ZnZpcHlIV2FzWkRMcSUyQndrTmRFb0xVMmtMektWZ3BCUjFzcXhHeGk5eEpnbjFkNEw0Q05TRHclM0QlM0Q.")
navegador.find_element('xpath', '//*[@id="BotaoPopup1"]').click()
navegador.find_element('xpath', '//*[@id="firstname"]').send_keys("Matheus")
navegador.find_element('xpath', '//*[@id="email"]').send_keys("Matheushenrihds@gmail.com")
navegador.find_element('xpath', '//*[@id="phone"]').send_keys("11961644855")
navegador.find_element('xpath', '//*[@id="_form_1925_submit"]').click()
navegador.find_element('xpath', '//*[@id="botao-minicurso"]').click()

input("Pressione ENTER para fechar o navegador...")
  