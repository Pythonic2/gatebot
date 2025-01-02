from concurrent.futures import ProcessPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import time


# Configurar o WebDriver (apenas uma vez)
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.set_capability("acceptInsecureCerts", True)

    driver = webdriver.Remote(
        command_executor='http://192.168.0.3:4444',
        options=chrome_options
    )
    return driver


# Função que realiza o scraping
def scrape_page(instance_id, url):
    driver = create_driver()
    try:
        print(f"Instância {instance_id}: Acessando {url}")

        start_scrape = time()
        driver.get(url)

        # Esperar o título da página carregar
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "title"))
        )
        title = driver.title
        end_scrape = time()

        scrape_duration = end_scrape - start_scrape
        print(f"Instância {instance_id}: Título -> {title}")
        print(f"Instância {instance_id}: Tempo de scraping -> {scrape_duration:.2f} segundos")

        return {"instance_id": instance_id, "url": url, "title": title, "scrape_duration": scrape_duration}
    except Exception as e:
        print(f"Instância {instance_id}: Erro -> {e}")
        return {"instance_id": instance_id, "url": url, "title": None, "scrape_duration": None}
    finally:
        driver.quit()


def main():
    # URLs para scraping
    urls = [
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.python.org",
        "https://www.selenium.dev",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.reddit.com",
        "https://www.medium.com",
        "https://www.linkedin.com",
        "https://www.microsoft.com"
    ]

    # Limitar para 5 instâncias simultâneas
    MAX_INSTANCES = 5

    start_time = time()

    # Usar ProcessPoolExecutor para multiprocessing
    with ProcessPoolExecutor(max_workers=MAX_INSTANCES) as executor:
        # Mapear URLs para scraping
        results = list(executor.map(scrape_page, range(len(urls)), urls))

    end_time = time()

    # Exibir os resultados
    print("\nResultados:")
    for result in results:
        print(result)

    print(f"\nTempo total de execução: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
