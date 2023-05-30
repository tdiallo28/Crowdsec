import platform
import requests

def get_cve(keyword):
  api_endpoint = "https://services.nvd.nist.gov/rest/json/cves/1.0?keyword="

  try:
    res = requests.get(api_endpoint + keyword)
    res.raise_for_status()

    result = res.json()

    if "result" in result:
      return result['result']['CVE_Items']
    else:
     return [] 

  except Exception as e:
    print(f"Une erreur est survenue lors de la requête : {e}")
    return []

  
def send_email(subject, content):
  smtp = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
  smtp.starttls()

  if SMTP_LOGIN:
    smtp.login(SMTP_LOGIN, SMTP_PASS)

  msg = MIMEMultipart()
  msg["From"] = SMTP_FROM
  msg["To"] = SMTP_TO
  msg["Subject"] = subject
  msg.attach(MIMEText(content, 'html'))

  smtp.send_message(msg)

  del msg
  smtp.quit()

if __name__ == "__main__":
  os = platform.system()

  if os == "Windows":
    os_version = f"{os} {platform.version()}"
  elif os == "Darwin":
    os_version = f"Mac {platform.mac_ver()[0]}"
  elif os == "Linux":
    linux_distrib = platform.linux_distribution()
    os_version = f"{linux_distrib[0]} {linux_distrib[1]}"

  print(f"Recherche des CVE pour {os_version} ...")
  cve_items = get_cve(os_version)

  if len(cve_items) > 0:
    content = f"{len(cve_items)} CVE trouvées pour {os_version} :"

    for cve in cve_items:
      content += f"\n\n- CVE_ID: {cve['cve']['CVE_data_meta']['ID']}"
      content += f"\n- Score CvssV3: {cve['impact']['baseMetricV3']['cvssV3']['baseScore']}"
      content += f"\n- Description: {cve['cve']['description']['description_data'][0]['value']}"
  
    print(content)
    # send_email("Récapitulatif CVE", content)
  else:
    print(f"Aucune CVE trouvée pour {os_version} !")
    # send_email("Récapitulatif CVE", "Aucune CVE trouvée pour {os_version} !")
